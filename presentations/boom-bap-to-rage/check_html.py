"""Check offline structure and evidence mapping; does not validate history."""
import json
import re
import subprocess
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[1]
VOID = set('area base br col embed hr img input link meta param source track wbr'.split())

class Check(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids=[]; self.links=[]; self.stack=[]; self.errors=[]
        self.slides=[]; self.cites={}; self.active=None; self.script=False
        self.js=[]; self.dependencies=[]
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if a.get('id'): self.ids.append(a['id'])
        if tag=='a' and a.get('href'): self.links.append(a['href'])
        if tag=='section' and 'slide' in a.get('class','').split():
            self.active=a['id']; self.slides.append(self.active); self.cites[self.active]=set()
        if a.get('data-source') and self.active:
            self.cites[self.active].add(a['data-source'].upper())
        if tag in ('script','img','iframe','audio','video','source') and a.get('src'):
            self.dependencies.append(a['src'])
        if tag=='link' and a.get('href'): self.dependencies.append(a['href'])
        if tag=='script': self.script=True
        if tag not in VOID: self.stack.append(tag)
    def handle_endtag(self, tag):
        if tag=='section': self.active=None
        if tag=='script': self.script=False
        if not self.stack or self.stack[-1]!=tag: self.errors.append('Unbalanced closing tag: '+tag)
        else: self.stack.pop()
    def handle_data(self, data):
        if self.script: self.js.append(data)

def main():
    parser=Check(); parser.feed((BASE/'index.html').read_text(encoding='utf-8'))
    errors=parser.errors
    if parser.stack: errors.append('Unclosed tags: '+str(parser.stack))
    errors += ['Duplicate ID: '+i for i,n in Counter(parser.ids).items() if n>1]
    local=0
    for link in parser.links+parser.dependencies:
        p=urlsplit(link)
        if p.scheme or p.netloc: continue
        if not p.path:
            if p.fragment and unquote(p.fragment) not in parser.ids: errors.append('Missing HTML anchor: '+link)
        else:
            local+=1; target=(BASE/unquote(p.path)).resolve()
            if not target.is_relative_to(ROOT) or not target.is_file(): errors.append('Missing/outside file: '+link)
    for dep in parser.dependencies:
        if urlsplit(dep).scheme or dep.startswith('//'): errors.append('Network-dependent resource: '+dep)
    outline=(BASE/'outline.md').read_text(encoding='utf-8')
    evidence=(BASE/'evidence-map.md').read_text(encoding='utf-8')
    outline_ids=re.findall(r'^## (slide-\d+)｜',outline,re.M)
    evidence_ids=list(dict.fromkeys(re.findall(r'^\| (slide-\d+) \|',evidence,re.M)))
    if parser.slides!=outline_ids: errors.append('Outline slide order mismatch')
    if parser.slides!=evidence_ids: errors.append('Evidence slide order mismatch')
    for sid,cites in parser.cites.items():
        rows='\n'.join(x for x in evidence.splitlines() if x.startswith('| '+sid+' |'))
        missing=cites-set(re.findall(r'S\d{3}',rows))
        if missing: errors.append(f'Unmapped citations {sid}: {sorted(missing)}')
    for path,anchor in re.findall(r'\]\(\.\./\.\./(wiki/[^)#]+)#([^)]+)\)',outline+'\n'+evidence):
        target=ROOT/path
        if not target.is_file(): errors.append('Missing evidence file: '+path)
        elif f'id="{anchor}"' not in target.read_text(encoding='utf-8'): errors.append('Missing evidence anchor: '+path+'#'+anchor)
    try:
        result=subprocess.run(['node','--check'],input='\n'.join(parser.js),text=True,capture_output=True,encoding='utf-8')
        if result.returncode: errors.append('JavaScript syntax: '+result.stderr)
        syntax=result.returncode==0
    except FileNotFoundError:
        syntax=None; errors.append('Node unavailable')
    report=dict(slides=len(parser.slides),unique_ids=len(set(parser.ids)),citations=sum(len(x) for x in parser.cites.values()),local_paths_checked=local,auto_loaded_resources=parser.dependencies,javascript_syntax_passed=syntax,errors=errors,limits='Structure only; D1 content and D3 browser checks are separate.')
    print(json.dumps(report,ensure_ascii=False,indent=2))
    return bool(errors)

if __name__=='__main__': raise SystemExit(main())
