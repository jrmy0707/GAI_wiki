"""Check local Wiki structure; this does not validate historical truth or URLs online."""

import json
import re
from collections import Counter
from pathlib import Path
from urllib.parse import parse_qsl, unquote, urlencode, urlsplit, urlunsplit


ROOT = Path(__file__).resolve().parents[1]
LINK = re.compile(r"\[[^\]\n]+\]\(([^)\n]+)\)")
FIELDS = (
    "source_id title author publisher published_date updated_date original_url "
    "read_url acquired_date source_type source_origin supplement_reason raw_file "
    "read_scope missing_scope acquisition_status ingest_status check_status last_processed"
).split()
STATES = ("pending", "blocked", "partial", "complete")


def metadata(text):
    if not text.startswith("---\n"):
        return {}
    block = text.split("\n---", 1)[0][4:]
    return {
        key.strip(): value.strip()
        for line in block.splitlines()
        if ":" in line
        for key, _, value in [line.partition(":")]
    }


def anchors(text):
    result = set(re.findall(r'<a\s+id="([^"]+)"\s*></a>', text))
    # GitHub-style headings are supplementary; evidence uses explicit stable IDs.
    for heading in re.findall(r"^#{1,6}\s+(.+)$", text, re.M):
        heading = re.sub(r"[^\w\-\s]", "", heading.lower())
        result.add(heading.replace(" ", "-"))
    return result


def canonical_url(value):
    parts = urlsplit(value)
    query = [(k, v) for k, v in parse_qsl(parts.query) if not k.startswith("utm_")]
    return urlunsplit((parts.scheme.lower(), parts.netloc.lower(),
                       parts.path.rstrip("/"), urlencode(sorted(query)), ""))


def main():
    errors = []
    paths = sorted(
        path for path in ROOT.rglob("*.md")
        if not any(part.startswith(".") for part in path.relative_to(ROOT).parts)
    )
    texts = {path: path.read_text(encoding="utf-8-sig") for path in paths}
    targets_by_page = {}
    local_count = fragment_count = 0
    for path, text in texts.items():
        targets_by_page[path] = set()
        for match in LINK.finditer(text):
            target = match.group(1).strip().strip("<>")
            parts = urlsplit(target)
            if parts.scheme or parts.netloc:
                continue
            local_count += 1
            resolved = (path.parent / unquote(parts.path)).resolve() if parts.path else path
            targets_by_page[path].add(resolved)
            label = str(path.relative_to(ROOT))
            if not resolved.is_relative_to(ROOT) or not resolved.is_file():
                errors.append(f"Missing or outside-project target: {label} -> {target}")
            elif parts.fragment:
                fragment_count += 1
                if resolved not in texts or unquote(parts.fragment) not in anchors(texts[resolved]):
                    errors.append(f"Missing anchor: {label} -> {target}")
        explicit = re.findall(r'<a\s+id="([^"]+)"\s*></a>', text)
        if len(explicit) != len(set(explicit)):
            errors.append(f"Duplicate explicit anchor: {path.relative_to(ROOT)}")

    index = ROOT / "wiki/index.md"
    indexed = targets_by_page.get(index, set())
    wiki_pages = [path for path in texts if path.is_relative_to(ROOT / "wiki") and path != index]
    for path in wiki_pages:
        if path not in indexed:
            errors.append(f"Unindexed Wiki page: {path.relative_to(ROOT)}")

    source_pages = sorted((ROOT / "wiki/sources").glob("*.md"))
    source_ids, source_urls = set(), set()
    counts = Counter({state: 0 for state in STATES})
    substantive = [path for path in wiki_pages if not path.is_relative_to(ROOT / "wiki/sources")]
    for path in source_pages:
        data = metadata(texts[path])
        for field in FIELDS:
            if not data.get(field):
                errors.append(f"Missing source field: {path.name} -> {field}")
        source_id = data.get("source_id", "")
        if not re.fullmatch(r"S\d{3,}", source_id) or source_id in source_ids:
            errors.append(f"Invalid or duplicate source ID: {path.name} -> {source_id}")
        source_ids.add(source_id)
        read_url = data.get("read_url", "")
        normalized = canonical_url(read_url)
        if not read_url.startswith("https://") or normalized in source_urls:
            errors.append(f"Invalid or duplicate canonical source URL: {path.name}")
        source_urls.add(normalized)
        state = data.get("ingest_status", "")
        if state not in STATES:
            errors.append(f"Invalid ingest status: {path.name} -> {state}")
        else:
            counts[state] += 1
        raw = (path.parent / data.get("raw_file", "")).resolve()
        if not raw.is_relative_to(ROOT / "raw") or not raw.is_file():
            errors.append(f"Missing raw record: {path.name}")
        if state == "complete":
            if data.get("check_status") not in ("AI 已檢查", "AI 已檢查但有待查事項", "使用者已複核"):
                errors.append(f"Complete source lacks check status: {source_id}")
            if not any(path in targets_by_page.get(page, set()) for page in substantive):
                errors.append(f"Complete source unused in substantive page: {source_id}")
            for log in ("ingestion_log.md", "quality_report.md"):
                if source_id not in texts.get(ROOT / "logs" / log, ""):
                    errors.append(f"Complete source absent from {log}: {source_id}")

    for page in substantive:
        for label in ("重要主張表", "來源分歧", "待查問題", "最近更新", "檢查狀態"):
            if label not in texts[page]:
                errors.append(f"Missing substantive-page label: {page.name} -> {label}")
    index_text = texts.get(index, "")
    for state in STATES:
        row = re.search(rf"^\| {state} \| ([*\d]+) \|$", index_text, re.M)
        if not row or int(row.group(1).strip("*")) != counts[state]:
            errors.append(f"Index status count mismatch: {state}")
    readme = texts.get(ROOT / "README.md", "")
    match = re.search(r"complete 獨立來源 \| \*\*(\d+) / 5", readme)
    if not match or int(match.group(1)) != counts["complete"]:
        errors.append("README complete count mismatch")

    print(json.dumps({
        "markdown_files": len(paths), "local_links_checked": local_count,
        "fragment_links_checked": fragment_count,
        "wiki_pages_indexed": len(wiki_pages), "source_notes": len(source_pages),
        "source_status_counts": dict(counts), "errors": errors,
        "limits": "Checks structure only; does not prove source independence or historical truth."
    }, ensure_ascii=False, indent=2))
    return bool(errors)


if __name__ == "__main__":
    raise SystemExit(main())
