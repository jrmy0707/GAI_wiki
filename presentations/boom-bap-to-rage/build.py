"""Author the offline HTML and its aligned research documents with stdlib only."""
from pathlib import Path
import html
import json
import re

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
REVISION_DATE = '2026-11-17'

def cite(*ids):
    return ' '.join(f'<a class="cite" href="#source-{s.lower()}" data-source="{s.lower()}" aria-label="開啟來源 {s}">{s}</a>' for s in ids)

def claim(text, kind, wiki, c, refs, limit):
    return dict(text=text, kind=kind, wiki=wiki, c=c, refs=refs, limit=limit)

def row(label, text):
    return f'<div class="line"><h3>{label}</h3><p>{text}</p></div>'

slides = [
dict(id='slide-01', title='從 Boom Bap 到 Rage', goals=['L01','L04'], tag='美國嘻哈曲風的演變與世代交替', theme='dark cover',
     point='以聲音、創作與傳播方式理解世代變化，保留並行與交叉。', reason='封面不新增歷史定論。', visual='大字標題與三種曲風名稱，無發展箭頭。',
     body='<h1>從 Boom Bap<br>到 <em>Rage</em></h1><p class="cover-sub">美國嘻哈曲風的演變與世代交替</p><p class="cover-note">1990 年代至 2020 年代的選例<br>聲音、創作與傳播方式，交錯著改變</p>', claims=[]),
dict(id='slide-02', title='理解嘻哈的三個角度', goals=['L03','L04'], tag='閱讀方式', theme='paper',
     point='曲風、地域與平台是可以交叉使用的不同觀察角度。', reason='Atlanta 和 SoundCloud 為後文提供分類座標。', visual='三條平行文字列，以類別與例子形成對照。',
     body=row('聲音／曲風', 'Boom bap、Trap、Rage：鼓怎麼打，音色與人聲怎麼安排。'+cite('S001','S004','S007'))+
          row('地域／場景', 'Atlanta 是城市；當地的創作者、合作與活動，可以容納多種聲音。'+cite('S003'))+
          row('平台／社群', 'SoundCloud 是發布音樂的平台；「SoundCloud 世代」在此指平台與場景的歷史。'+cite('S005'))+
          '<p class="aside">同一首作品可同時有曲風、地方與平台背景。這是本簡報的閱讀框架。</p>',
     claims=[claim('曲風、地域與平台分開分析。','綜合解讀','wiki/history/overview.md','C02',[('S001','E01'),('S003','E03'),('S003','E05')],'分類框架，非影響鏈。'),claim('聲音類別的入門並置。','綜合解讀／教學框架','wiki/history/overview.md','C07',[('S001','E01'),('S004','E02'),('S007','E01')],'各自聲音由後文說明，並置不證影響。'),claim('SoundCloud 世代採平台／場景分類。','作者觀點／Wiki 解讀','wiki/history/soundcloud-generation.md','C01',[('S005','E01')],'不是固定音色或現行服務規則。')]),
dict(id='slide-03', title='Boom bap：鼓聲的衝擊', goals=['L01','L02'], tag='聲音線索 01', theme='paper',
     point='大鼓、小鼓的突出衝擊與粗礪感，是本文受訪者重視的線索。', reason='DJ Premier、Diamond D 提供製作觀；KRS-One 專輯說明創作宣言。', visual='左側大字 BOOM／BAP，右側說明；底部一項作品。',
     body='<div class="sound-layout"><div class="sound-words" aria-label="KRS-One 以 Boom 解釋大鼓，Bap 解釋小鼓">BOOM<span>大鼓</span>BAP<span>小鼓</span></div><div>'+row('鼓聲突出', '製作人 DJ Premier、Diamond D 強調粗礪、有衝擊力的鼓聲。左側是 KRS-One 對名稱的解釋。'+cite('S001'))+row('取樣', '錄下聲音片段，供之後重播與創作；也可借用既有錄音材料。'+cite('S010','S001'))+'</div></div>'+
          '<p class="example"><strong>KRS-One《Return of the Boom Bap》（1993）</strong><br>饒舌歌手 KRS-One 藉名稱重申早期製作精神。'+cite('S001')+'</p><p class="aside">聲音描述與創作意圖來自同篇報導的受訪者，不能當作每首作品必備的標準。</p>',
     claims=[claim('受訪者重視鼓的衝擊與粗礪感，KRS-One 對照大鼓／小鼓。','當事人自述','wiki/styles/boom-bap.md','C01',[('S001','E01')],'同一報導，非通用必要條件。'),claim('取樣的基本解釋。','原廠說明／白話轉述','wiki/styles/boom-bap.md','C05',[('S010','E01'),('S001','E01')],'不限定來源只能是舊唱片。'),claim('1993 年作品及宣言。','報導記載／當事人自述','wiki/styles/boom-bap.md','C02',[('S001','E02')],'未獨立核原始發行資料，非起源年。')]),
dict(id='slide-04', title='Atlanta：地方場景的多種聲音', goals=['L03','L04'], tag='南方背景的一個城市案例', theme='dark',
     point='地方合作、生活經驗和活動場域，是理解聲音形成的具體條件。', reason='Outkast、Goodie Mob、Organized Noize 用於說明製作社群；不是南方完整名單。', visual='平行的合作／生活／活動三列，不以城市等同曲風。',
     body=row('創作者的合作', '1990 年代，Dungeon Family 社群連結了饒舌團體 Outkast、Goodie Mob 與製作團隊 Organized Noize。'+cite('S003'))+
          row('作品中的地方經驗', '記者 Jewel Wicker 將音樂的聲音層次與黑人勞動階級經驗放在一起，解讀這些作品。'+cite('S003'))+
          row('交流的場域', 'Wicker 也把地方活動、夜生活與外地聲音交流放進歷史敘事。'+cite('S003'))+
          '<p class="aside">這是 Wicker 的地域史視角。Atlanta 是南方的一個案例，不能涵蓋整個南方。</p>',
     claims=[claim('Dungeon Family 合作及地方作品解讀。','報導記載／作者觀點','wiki/history/atlanta-hip-hop.md','C02',[('S003','E03')],'非完整製作名單或整個南方。'),claim('活動、交流與夜生活的場域。','作者觀點／報導記載','wiki/history/atlanta-hip-hop.md','C04',[('S003','E04')],'不是單一因果模型。')]),
dict(id='slide-05', title='Trap：低頻與節奏的編排', goals=['L01','L02'], tag='聲音線索 02', theme='paper',
     point='從低頻鼓聲、踩鈸／小鼓編排與人聲節奏比較 Trap。', reason='採 Universal Production Music 的入門聲音概述，不加入無錄音依據的參數。', visual='808 大字加兩列節奏／人聲說明。',
     body='<div class="sound-layout"><div class="sound-words number">808<span>轟鳴的低頻鼓聲</span></div><div>'+row('808 是什麼', '這裡指轟鳴的低頻鼓聲，用語源自 Roland TR-808 鼓機。作品可以使用相關聲音，不代表每首都用這台硬體。'+cite('S004'))+row('鼓與人聲分開看', '概述也列出較精簡的伴奏、踩鈸（hi-hat）與小鼓的節奏編排。Flow 指人聲的節奏安排，可和鼓的編排分開聽。'+cite('S004'))+'</div></div>'+
          '<p class="aside">以上依 Universal Production Music 的文字概述。鼓的細分與人聲節奏是不同層次；這些線索並非每首歌都必備。</p>',
     claims=[claim('Trap 聲音線索、808 詞義與人聲／鼓層次。','作者概述／Wiki 白話整理','wiki/styles/trap.md','C02',[('S004','E02')],'不當成固定標準、硬體判定或技巧發明史。')]),
dict(id='slide-06', title='Trap：生活題材與草根流通', goals=['L03','L04'], tag='聲音之外的形成條件', theme='paper',
     point='題材用語、作品名稱、聲音分類與流通方式需要分開。', reason='T.I. 與 Trap Muzik 示範作品節點；mixtape 示範傳播渠道。', visual='題材／流通兩個水平段落，底部作品年份。',
     body=row('名稱的生活背景', 'Universal Production Music 將名稱連到 Atlanta 毒品交易場所與相關生活題材，再區分題材用法和後來的聲音分類。'+cite('S004'))+
          row('Mixtape 的流通', '文中描述藝人自行製作與散布歌曲合集（mixtape）的草根渠道。音樂如何到達聽眾，也是這段歷史的一部分。'+cite('S004'))+
          '<p class="example"><strong>T.I.《Trap Muzik》（2003）</strong><br>饒舌歌手 T.I. 的這張專輯，提供作品命名與流通的具體案例。'+cite('S004')+'</p><p class="aside">2003 是文章記載的作品年份。首次用語、唯一發明者及簽約因果仍待查。</p>',
     claims=[claim('Trap 名稱與生活題材的關係。','機構作者概述／待查','wiki/styles/trap.md','C01',[('S004','E01')],'保留轉引限制，不選唯一詞源。'),claim('Mixtape 草根流通。','機構作者觀點','wiki/styles/trap.md','C04',[('S004','E03')],'不直接推成簽約或商業因果。'),claim('T.I. 2003 年作品。','文章記載','wiki/styles/trap.md','C03',[('S004','E03')],'非曲風誕生年，原始發行待獨立核對。')]),
dict(id='slide-07', title='SoundCloud 世代：平台與場景', goals=['L02','L03','L04'], tag='2010 年代的平台視角', theme='dark',
     point='發布方式的改變可以與多種聲音共存。', reason='South Florida 與 Bryson Tiller 對照平台內的聲音差異。', visual='左側發布方式，右側並列不同聲音；無單一曲風徽章。',
     body=row('發布方式', '評論者 Alphonse Pierre 在 2019 年把較低的上傳門檻、一次發布一首歌與藝人的能見度連在一起。'+cite('S005'))+
          row('同一平台，多種聲音', '他的選例包括 South Florida 的粗糙、失真聲音，也包括歌手 Bryson Tiller 結合歌唱與饒舌的表達。'+cite('S005'))+
          row('跨平台的流通', 'Pierre 也討論社群、影音與串流之間的曝光。這是他的產業解讀，尚不能證明某種演算法必然帶來成功。'+cite('S005'))+
          '<p class="aside">「SoundCloud 世代」在本簡報是平台／場景分類，沒有所有人共享的固定音色或起止日。</p>',
     claims=[claim('低門檻、逐曲發布與能見度。','作者觀點','wiki/history/soundcloud-generation.md','C01',[('S005','E01')],'以 2019 年評論為界，非現行功能說明。'),claim('South Florida 與 Bryson Tiller 的差異。','作者比較／Wiki 解讀','wiki/history/soundcloud-generation.md','C02',[('S005','E02')],'不是每位使用者共同聲音。'),claim('跨平台曝光敘事。','作者觀點／待查','wiki/history/soundcloud-generation.md','C04',[('S005','E05')],'未核流量與合約，相關性不證因果。')]),
dict(id='slide-08', title='Rage：密集反覆的電子音色', goals=['L01','L02','L03'], tag='聲音線索 03', theme='lime',
     point='S007 將 Rage 描述為密集、反覆的合成器與 Trap 鼓組的組合。', reason='先以聲音辨識，再於下一頁交代作品及角色。', visual='RAGE 字樣與上下兩個聲音層，展示疊合關係。',
     body='<div class="rage-word" aria-hidden="true">RAGE</div>'+row('旋律與音色層', '合成器是以電子訊號與音色處理產生聲音的樂器，也能使用取樣。'+cite('S010'))+
          row('與 Trap 鼓組疊合', 'Gabriel Bras Nevares 的專題以密集、反覆、明亮的合成器疊上 Trap 鼓組，描述 2020 年代初的 Rage 聲音。'+cite('S007'))+
          '<p class="aside">這是作者的概括，部分定義轉引分類網站。強烈的音色與激烈吼叫可以分開；吼叫不是所有 Rage 作品的必要條件。'+cite('S007')+'</p>',
     claims=[claim('合成器的基本解釋，也能使用取樣。','原廠說明／白話轉述','wiki/styles/rage.md','C07',[('S010','E02')],'不推定逐曲機型。'),claim('合成器與 Trap 鼓組的聲音描述，吼叫非必要。','作者概括／Wiki 對照','wiki/styles/rage.md','C01',[('S007','E01'),('S007','E04')],'轉引未獨立核原分類頁，未聆聽。'),claim('2020 年代初為作者觀察範圍。','作者觀點','wiki/styles/rage.md','C02',[('S007','E02')],'非唯一誕生年或地點。')]),
dict(id='slide-09', title='Rage 的兩個作品選例', goals=['L01','L02','L03'], tag='作品的角色與日期', theme='dark',
     point='作品可示範聲音與歷史角色，發行日不能代證命名或影響。', reason='兩作品分別示範作者的推廣判斷、聲音模板及可核對發行資料。', visual='兩個大型作品段落，日期與角色分欄。',
     body='<div class="work"><p class="year">2020</p><div><h3>Playboi Carti《Whole Lotta Red》</h3><p>饒舌歌手 Carti 的這張專輯，被 Nevares 選作 Rage 影響與推廣的重要案例。這個歷史角色是作者判斷。'+cite('S007')+'</p></div></div>'+
          '<div class="work"><p class="year">2021</p><div><h3>Trippie Redd、Playboi Carti〈Miss The Rage〉</h3><p>兩位饒舌歌手的單曲，被作者用來說明名稱與聲音模板；Apple Music 目錄記錄發行日為 2021-05-07。'+cite('S007','S008')+'</p></div></div>'+
          '<p class="aside">這些日期不證明風格在當天誕生或名稱首次使用。來源提供的是文字描述，未完成錄音聆聽。</p>',
     claims=[claim('Whole Lotta Red 的 2020 年及角色。','日期：文中記載；角色：作者觀點','wiki/styles/rage.md','C03',[('S007','E03')],'不將影響判斷升為共識。'),claim('Miss The Rage 的日期、命名與模板。','日期：平台資料；角色：作者觀點','wiki/styles/rage.md','C04',[('S007','E04'),('S008','E01')],'正式發行不證明最早用語，未填預告日。')]),
dict(id='slide-10', title='三種聲音的比較', goals=['L01','L02'], tag='整理已經出現的線索', theme='paper',
     point='三種聲音可以從鼓、材料與人聲條件比較，邊界保持彈性。', reason='將前文例證集中比較，不新增獨立聲學判定。', visual='可讀的三列比較表。',
     body='<div class="table-wrap"><table class="compare"><caption class="sr-only">依文字來源比較曲風的鼓聲與音色線索</caption><thead><tr><th scope="col">曲風</th><th scope="col">鼓聲與節奏</th><th scope="col">材料／表達線索</th></tr></thead><tbody>'+
          '<tr><th scope="row">Boom bap '+cite('S001')+'</th><td>突出大鼓、小鼓的衝擊</td><td>粗礪感與取樣材料</td></tr>'+
          '<tr><th scope="row">Trap '+cite('S004')+'</th><td>808 低頻、踩鈸與小鼓編排</td><td>較精簡的伴奏、人聲節奏安排</td></tr>'+
          '<tr><th scope="row">Rage '+cite('S007')+'</th><td>延用 Trap 鼓組的描述</td><td>密集反覆的合成器；吼叫非必要</td></tr></tbody></table></div>'+
          '<p class="aside">這是前文文字來源的並讀。取樣與合成器可以共用，以上不構成互斥分類或固定配方。'+cite('S010')+'</p>',
     claims=[claim('Boom bap 比較列。','當事人自述','wiki/styles/boom-bap.md','C01',[('S001','E01')],'非必要條件。'),claim('Trap 比較列。','作者概述','wiki/styles/trap.md','C02',[('S004','E02')],'非發明史。'),claim('Rage 比較列。','作者概括／Wiki 對照','wiki/styles/rage.md','C01',[('S007','E01'),('S007','E04')],'不代表全部作品。'),claim('合成器與取樣可共用。','原廠說明／白話轉述','wiki/styles/rage.md','C07',[('S010','E02')],'不是二元年代劃分。')]),
dict(id='slide-11', title='作品節點與觀察時期', goals=['L03','L04'], tag='不同列可以並讀', theme='paper',
     point='作品年份和評論觀察期不等同形成期，時間相鄰不表示因果。', reason='年份取前文作品；SoundCloud 用評論對 2010 年代的回顧。', visual='多軌時間表，分開作品事件與來源觀察期，不畫替代箭頭。',
     body='<div class="table-wrap"><table class="milestones"><caption class="sr-only">選例定位表，空格不表示該風格不存在</caption><thead><tr><th scope="col">資料線索</th><th scope="col">1990 年代</th><th scope="col">2000 年代</th><th scope="col">2010 年代</th><th scope="col">2020 年代</th></tr></thead><tbody>'+
          '<tr><th scope="row">作品事件</th><td><b>1993</b><br>KRS-One 專輯 '+cite('S001')+'</td><td><b>2003</b><br>T.I. 專輯 '+cite('S004')+'</td><td class="blank">未選例</td><td><b>2020／2021</b><br>Rage 作品選例 '+cite('S007','S008')+'</td></tr>'+
          '<tr><th scope="row">平台觀察期</th><td class="blank">未選例</td><td class="blank">未選例</td><td>Pierre 回顧的<br>SoundCloud 世代 '+cite('S005')+'</td><td class="blank">本列未界定</td></tr></tbody></table></div>'+
          '<p class="aside">表格只定位這份簡報的例子，不標記曲風起止。空格表示未選例；無法據此宣布某種聲音消失。</p>',
     claims=[claim('1993 專輯年份。','報導記載','wiki/styles/boom-bap.md','C02',[('S001','E02')],'原始發行待核。'),claim('2003 專輯年份。','文章記載','wiki/styles/trap.md','C03',[('S004','E03')],'非起源年。'),claim('2020 年 Rage 選例。','文章記載','wiki/styles/rage.md','C03',[('S007','E03')],'年份只定位作品。'),claim('2021 年 Rage 選例。','平台資料','wiki/styles/rage.md','C04',[('S008','E01')],'正式發行不證命名。'),claim('SoundCloud 分期界線。','作者觀點／Wiki 限定','wiki/history/soundcloud-generation.md','C06',[('S005','E06')],'不宣告平台或相關創作終止。')]),
dict(id='slide-12', title='世代交替：三種變化的比較', goals=['L02','L03','L04'], tag='本簡報的操作框架', theme='dark',
     point='世代交替比較審美、創作與傳播，而非舊曲風必然退場。', reason='從前文具體案例綜合，另用 Carti 評論提醒逐作品分類。', visual='三條平行軌道，Trap 鼓組在 Rage 中的延用呈現元素交叉。',
     body=row('審美與創作', '可比較鼓的衝擊、取樣材料、人聲節奏，以及電子音色的組合。Rage 的描述仍包含 Trap 鼓組，顯示元素可以延用與交叉。'+cite('S001','S004','S007'))+
          row('音樂到達聽眾的方式', 'Mixtape 的草根流通、SoundCloud 的逐曲發布與跨平台曝光，提供不同的傳播觀察角度。'+cite('S004','S005'))+
          row('作品、藝人與世代', 'Sheldon Pearce 的 2025 年評論從人聲與跨風格作品理解 Carti。藝人的創作路徑，不能用單一風格或平台分期概括。'+cite('S009'))+
          '<p class="aside">以上是 Wiki 的綜合解讀，容許並存與融合。這份材料沒有證明各種聲音依序消失，也沒有量化市場主導。</p>',
     claims=[claim('用聲音、創作與傳播比較世代變化。','綜合解讀／教學框架','wiki/history/overview.md','C07',[('S001','E01'),('S004','E02'),('S004','E03'),('S005','E01'),('S007','E01')],'非市場替代或完整續存年表。'),claim('作品、藝人與場景分期不必同步。','作者觀點／綜合解讀','wiki/history/overview.md','C06',[('S009','E01'),('S009','E02'),('S005','E06')],'不把 Carti 全目錄歸 Rage。')]),
dict(id='slide-13', title='下一次聽到一首饒舌歌', goals=['L01','L02','L03','L04'], tag='把這些角度帶回音樂', theme='lime',
     point='以聲音線索與具體形成條件進行比較，保留分類彈性。', reason='僅回顧前文，不新增歷史事實或聆聽結果。', visual='聲音回顧與兩個聆聽問題；右上角來源按鈕為延伸入口。',
     body='<div class="recap"><p><b>聽鼓聲</b><br>Boom bap 的大鼓、小鼓衝擊<br>Trap 的 808 低頻與節奏編排</p><p><b>聽音色</b><br>Rage 的密集反覆合成器<br>也保留 Trap 鼓組的線索</p></div>'+
          '<p class="closing">這首歌怎麼做？<br>它從哪個場景、經哪些渠道傳來？</p>'+
          '<p class="aside">以上回顧前文的文字來源。曲風分類可以重疊，作品也需要逐一理解。'+cite('S001','S004','S007','S009')+'</p>',
     claims=[claim('回顧聲音比較與分類彈性。','綜合解讀／教學回顧','wiki/history/overview.md','C07',[('S001','E01'),('S004','E02'),('S007','E01')],'不新增聆聽或音訊分析。'),claim('逐作品理解分類。','作者觀點／Wiki 限定','wiki/styles/rage.md','C06',[('S009','E01')],'不概括全目錄。')]),
]

additional_slides = [
dict(id='slide-14', title='1995：Outkast 的頒獎發言', goals=['L03','L04'], tag='地域聲音與能見度', theme='dark',
     point='地域歷史也包含誰獲得認可；頒獎事件與作者賦予的意義要分開。', reason='延續前頁 Outkast 的團體介紹，使用一個具體媒體事件說明南方聲音的能見度。', visual='具名短引語與事件說明，不畫成曲風起源或市場替代箭頭。',
     body='<blockquote class="event-quote">The South got<br>something to say.</blockquote><p class="quote-translation">意譯：南方也有話要說。</p>'+
          '<p class="example"><strong>Outkast 在 Source Awards 頒獎典禮的發言</strong><br>Jewel Wicker 的報導記載 1995 年領獎事件，並轉引團員 André 3000 的這句話。'+cite('S003')+'</p>'+
          '<p class="aside">Wicker 將它視為南方能見度的象徵節點。這個選例說明地域認可，不能證明 Atlanta 已成市場中心；本 Wiki 未觀看原始頒獎錄影。</p>',
     claims=[claim('1995 年 Source Awards 的 Outkast 領獎及 André 3000 發言，與作者賦予的象徵意義。','事件：報導記載；發言：轉引；意義：作者觀點','wiki/history/atlanta-hip-hop.md','C03',[('S003','E02')],'單一報導，未看原始錄影；不證市場中心或風格起源。')]),
dict(id='slide-15', title='Carti：人聲的重音與語氣', goals=['L02','L04'], tag='聲音線索的另一個層次', theme='paper',
     point='人聲的強調、語氣與字音長短，也是作者比較作品的聲音層次。', reason='以 S009 對 MUSIC 的評論補具體人聲觀察，同時示範逐作品分類。', visual='三個具體觀察詞與兩條說明，沿用現有平行列版型。',
     body='<p class="vocal-words">重音　語氣　音節</p>'+
          row('人聲怎麼表達', '評論者 Sheldon Pearce 以重音、語氣與音節伸縮分析 Carti：哪些字音被強調，聲音如何轉折，字音如何拉長或縮短。'+cite('S009'))+
          row('以作品為單位', 'Pearce 的 2025 年評論以《MUSIC》為入口，從跨風格角度理解作品。不能因 Carti 參與 Rage，就把整張專輯或全部作品都歸為 Rage。'+cite('S009'))+
          '<p class="aside">這是評論者的分析，補充先前的鼓組與合成器比較；本簡報未完成錄音聆聽，也沒有核對軟體設定或逐曲製作名單。</p>',
     claims=[claim('以重音、語氣及音節處理理解 Carti 人聲。','作者觀點／Wiki 白話轉述','wiki/styles/rage.md','C06',[('S009','E01')],'不宣稱自行聆聽、測量音訊或證明技術設定。'),claim('MUSIC 的跨風格評論與逐作品分類限制。','作者觀點／Wiki 分類限定','wiki/history/overview.md','C06',[('S009','E01')],'不將整張專輯或全目錄歸為 Rage，不推成世代共同終點。')])
]
for predecessor, added in zip(['slide-04','slide-09'], additional_slides):
    slides.insert(next(i for i,s in enumerate(slides) if s['id']==predecessor)+1, added)

glossary = [
 ('取樣','slide-03','錄下聲音片段，供之後重播與創作。','wiki/styles/boom-bap.md','C05','S010','E01'),
 ('808','slide-05','本頁指轟鳴的低頻鼓聲；用語連到 TR-808，不推定每首都用同一硬體。','wiki/styles/trap.md','C02','S004','E02'),
 ('踩鈸／hi-hat','slide-05','鼓組中的踩鈸聲；與小鼓、人聲節奏分開比較。','wiki/styles/trap.md','C02','S004','E02'),
 ('Flow','slide-05','人聲的節奏安排。','wiki/styles/trap.md','C02','S004','E02'),
 ('Mixtape','slide-06','此處指藝人自行製作與散布的歌曲合集。','wiki/styles/trap.md','C04','S004','E03'),
 ('合成器','slide-08','以電子訊號及音色處理產生聲音的樂器，也可使用取樣。','wiki/styles/rage.md','C07','S010','E02'),
 ('重音／語氣／音節伸縮','slide-15','本頁以字音的強調、聲音轉折與字音長短，白話說明評論的人聲觀察。','wiki/styles/rage.md','C06','S009','E01')
]

limits = {
 'S001':'含具名受訪者的報導。聲音與意圖多為自述；歷史核心仍主要依同一篇報導。',
 'S003':'NPR 報導，實讀 Wyoming Public Media 同篇轉載；GPB 原頁未成功取得。地域史解讀不等於市場排名。',
 'S004':'帶音樂庫推廣的機構概述。部分引語的 NPR 原始全文未取得，首次用語與製作名單保留待查。',
 'S005':'2019 年產業評論。分期、平台因果與商業權力屬作者觀點，不作今日現況。',
 'S007':'曲風專題／評論，部分定義轉引 RYM，原分類頁未讀。原發布日未知，命名與影響保留作者歸屬。',
 'S008':'只核對單曲核心目錄及 2021-05-07 作品發行日。日期不證明命名或起源，未播放音訊。',
 'S009':'NPR 音樂評論，實讀 KNKX 正文。人聲與跨作品比較屬作者觀點，不能概括全目錄。',
 'S010':'原廠教育術語表，只讀五個相關完整詞條；支持詞義，不證明特定作品使用某款器材。'
}
used = sorted(limits)
sources = {}
for sid in used:
    path = next((ROOT/'wiki/sources').glob(sid.lower()+'-*.md'))
    block = path.read_text(encoding='utf-8').split('\n---',1)[0][4:]
    data = dict(line.split(': ',1) for line in block.splitlines() if ': ' in line)
    data['path'] = path.relative_to(ROOT).as_posix()
    sources[sid] = data

css = r'''
:root {color-scheme:light; --ink:#182018; --paper:#f1efe5; --lime:#d2f47a; --muted:#546052; --line:#b4b8a7}
*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font-family:"Microsoft JhengHei","PingFang TC","Noto Sans TC",sans-serif;line-height:1.55}
button,select{font:inherit}button,a,select{-webkit-tap-highlight-color:transparent}button{cursor:pointer}a{color:inherit;text-underline-offset:4px}a:hover{text-decoration-thickness:2px}button:focus-visible,a:focus-visible,select:focus-visible,[tabindex]:focus-visible{outline:3px solid #b65711;outline-offset:4px}
.topbar{height:64px;display:flex;align-items:center;justify-content:space-between;padding:0 3.5vw;background:var(--paper);border-bottom:1px solid var(--line);font-size:16px}.brand{font-weight:700;letter-spacing:.12em}.top-actions{display:flex;align-items:center;gap:25px}.top-actions button{border:0;background:none;padding:8px}.edition{font-size:14px;color:var(--muted)}
.slide{max-width:1920px;margin:auto;min-height:calc(100dvh - 132px);padding:clamp(26px,3.1vw,60px) clamp(30px,5.3vw,102px);display:flex;flex-direction:column;gap:20px}.slide[hidden]{display:none}.tag{margin:0;font-size:16px;letter-spacing:.14em;font-weight:700}.slide h2{font-size:clamp(32px,3.5vw,62px);line-height:1.2;margin:2px 0 12px;letter-spacing:-.025em;font-weight:700}.slide-content{display:flex;flex:1;flex-direction:column;gap:22px}.line{display:grid;grid-template-columns:minmax(180px,23%) 1fr;gap:30px;border-top:1px solid var(--line);padding-top:18px}.line h3{margin:0;font-size:clamp(22px,1.9vw,33px);font-weight:700}.line p{margin:0;font-size:clamp(21px,1.8vw,30px);line-height:1.65}.cite{font-size:14px;display:inline-block;font-weight:600;padding:0 3px;vertical-align:baseline;white-space:nowrap}.aside{font-size:clamp(17px,1.22vw,21px);line-height:1.65;color:var(--muted);margin:auto 0 0;max-width:1500px}.example{font-size:clamp(20px,1.65vw,28px);margin:4px 0 0;border-left:4px solid currentColor;padding-left:22px;line-height:1.6}.dark{background:#18221c;color:#f1efe5;--line:#59665c;--muted:#c3cbbe}.lime{background:var(--lime);--line:#879b57;--muted:#38462a}.dark .tag,.dark em{color:var(--lime)}.paper .tag{color:#596438}.cover .slide-content{justify-content:center;gap:26px}.cover h1{font-size:clamp(64px,7vw,128px);line-height:1.07;letter-spacing:-.04em;margin:0;font-weight:800}.cover em{font-style:normal}.cover-sub{font-size:clamp(24px,2.1vw,38px);margin:0}.cover-note{font-size:21px;line-height:1.7;color:#c3cbbe;margin:5px 0 0}.cover .tag{font-size:15px}.cover .slide-content{padding:12px 0 10px}
.sound-layout{display:grid;grid-template-columns:29% 1fr;gap:50px;align-items:start}.sound-layout>div:last-child{display:flex;flex-direction:column;gap:28px}.sound-layout .line{grid-template-columns:1fr;gap:6px}.sound-words{font-size:clamp(48px,6.1vw,112px);font-weight:850;line-height:1.06;letter-spacing:-.06em}.sound-words span{display:block;font-size:20px;letter-spacing:0;font-weight:500;margin:6px 0 18px}.sound-words.number{font-size:clamp(80px,9vw,170px)}.rage-word{font-size:clamp(48px,5.6vw,102px);letter-spacing:-.06em;line-height:1;font-weight:900;margin-bottom:0}.work{display:grid;grid-template-columns:18% 1fr;gap:28px;border-top:1px solid var(--line);padding-top:20px}.work .year{font-size:clamp(40px,4.3vw,78px);line-height:1.1;margin:0;font-weight:800;color:var(--lime)}.work h3{font-size:clamp(22px,2vw,34px);margin:0 0 10px;line-height:1.4}.work p{font-size:clamp(20px,1.7vw,29px);margin:0;line-height:1.6}
.table-wrap{width:100%;overflow-x:auto}table{width:100%;border-collapse:collapse;line-height:1.5}th,td{border-bottom:1px solid var(--line);text-align:left;padding:23px 20px;vertical-align:top}thead th{font-size:18px;font-weight:500;color:var(--muted);border-top:1px solid var(--line)}.compare{font-size:clamp(21px,1.9vw,32px)}.compare th:first-child{width:24%;padding-left:0}.compare .cite{display:block;width:max-content}.milestones{font-size:clamp(18px,1.5vw,26px)}.milestones th,.milestones td{padding:24px 14px}.milestones th:first-child{width:15%;padding-left:0}.milestones td{width:21%}.milestones b{font-size:1.2em}.milestones .cite{font-size:13px}.blank{color:var(--muted);font-size:17px}.recap{display:grid;grid-template-columns:1fr 1fr;gap:70px;border-top:1px solid var(--line);padding-top:22px}.recap p{font-size:clamp(22px,2vw,34px);line-height:1.75;margin:0}.closing{font-size:clamp(30px,3vw,52px);line-height:1.5;margin:12px 0}.end-links{margin:0}.end-links button{border:1px solid var(--ink);background:none;padding:10px 20px;font-size:18px}
.navigation{height:68px;border-top:1px solid var(--line);display:flex;align-items:center;justify-content:space-between;padding:0 3.5vw;background:var(--paper);gap:20px}.nav-left,.nav-right{display:flex;align-items:center;gap:18px}.navigation button{border:1px solid #a5ad9c;background:none;min-width:78px;padding:7px 14px;font-size:17px}.navigation button:disabled{opacity:.4;cursor:default}.navigation select{max-width:min(34vw,430px);font-size:16px;border:0;background:none;padding:8px;color:var(--ink)}.keys{font-size:14px;color:var(--muted)}#page-number{font-variant-numeric:tabular-nums;min-width:68px;text-align:center;font-size:17px}.progress{height:3px;background:#a6b59f;position:fixed;left:0;right:0;bottom:0;pointer-events:none}.progress span{display:block;height:100%;background:#223b20;width:0}
dialog{color:var(--ink);background:var(--paper);width:min(1020px,94vw);max-height:90dvh;border:1px solid #88947e;padding:0;overflow:auto}dialog::backdrop{background:#07110caa}.dialog-top{position:sticky;top:0;background:var(--paper);display:flex;align-items:center;justify-content:space-between;padding:20px 30px;border-bottom:1px solid var(--line);z-index:1}.dialog-top h2{font-size:26px;margin:0}.dialog-top button{font-size:18px;background:none;border:1px solid #88947e;padding:5px 14px}.source-intro{padding:8px 30px;font-size:17px}.source-record{padding:24px 30px;border-top:1px solid var(--line);scroll-margin-top:90px}.source-record h3{font-size:24px;line-height:1.5;margin:0 0 10px}.source-record p{font-size:18px;margin:8px 0;line-height:1.65;overflow-wrap:anywhere}.source-record .source-links{font-size:17px;display:flex;flex-wrap:wrap;gap:18px}.source-record:target{outline:2px solid #8b9c68}.research{padding:25px 30px;border-top:1px solid var(--line);font-size:17px}.research a{margin-right:20px}.sr-only{position:absolute;width:1px;height:1px;overflow:hidden;clip-path:inset(50%);white-space:nowrap}.no-js{padding:16px 4vw;font-size:18px}
body:not(.enhanced) .navigation,body:not(.enhanced) .progress{display:none}body:not(.enhanced) dialog{display:block;position:static;max-height:none;margin:20px auto}body:not(.enhanced) .top-actions button{display:none}
.compare th,.compare td{padding-top:16px;padding-bottom:16px}
#slide-03 .slide-content{gap:14px}
.event-quote{font-size:clamp(44px,4.8vw,82px);font-weight:750;line-height:1.15;letter-spacing:-.03em;margin:0 0 4px;color:var(--lime)}
.quote-translation{font-size:clamp(21px,1.7vw,28px);margin:0}
.vocal-words{font-size:clamp(30px,3.2vw,55px);font-weight:700;line-height:1.25;margin:0}
@media(max-width:900px){.slide{padding:25px 28px;gap:18px}.slide h2{font-size:34px}.line{grid-template-columns:1fr;gap:7px}.line p{font-size:21px}.sound-layout{grid-template-columns:1fr;gap:20px}.sound-words{font-size:58px;display:flex;align-items:baseline;gap:10px}.sound-words span{font-size:17px}.sound-words.number{font-size:72px}.work{grid-template-columns:90px 1fr}.recap{gap:25px}.topbar .edition,.keys{display:none}.navigation{padding:0 20px;gap:8px}.nav-left,.nav-right{gap:8px}.navigation select{max-width:34vw;font-size:14px}.navigation button{min-width:50px;font-size:15px;padding:7px}.cover h1{font-size:72px}.compare,.milestones{min-width:700px}.aside{font-size:17px}}
@media(max-width:540px){.slide h2{font-size:29px}.cover h1{font-size:60px}.recap{grid-template-columns:1fr;gap:20px}.work{grid-template-columns:1fr;gap:7px}.work .year{font-size:36px}.navigation select{max-width:25vw}.brand{font-size:13px}.top-actions{gap:10px}.topbar{padding:0 20px}.topbar button{font-size:14px}.sound-words{flex-wrap:wrap}.cover-sub{font-size:23px}.closing{font-size:30px}}
@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
@media print{@page{size:A4 landscape;margin:0}.topbar,.navigation,.progress,.end-links{display:none!important}.slide,.slide[hidden]{display:flex!important;min-height:210mm;height:auto;width:297mm;break-after:page;padding:15mm;background:#fff;color:#182018;--line:#aab09e;--muted:#4d5846;print-color-adjust:exact}.slide-content{gap:5mm}.slide h2{font-size:28pt}.slide p,.line p,.work p,.compare,.recap p{font-size:17pt}.slide h3,.work h3{font-size:19pt}.aside{font-size:12pt!important}.cover h1{font-size:70pt}.dark em,.work .year{color:#415c20}.cite{font-size:10pt}dialog{display:block;position:static;max-height:none;width:auto;border:0;margin:0}.dialog-top{position:static}.dialog-top button{display:none}.source-record{break-inside:avoid}.source-record p{font-size:12pt}.research{font-size:12pt}}
'''

js = r'''
(() => {
 'use strict';
 const slides = Array.from(document.querySelectorAll('.slide'));
 const number = document.getElementById('page-number');
 const prev = document.getElementById('previous');
 const next = document.getElementById('next');
 const jump = document.getElementById('jump');
 const dialog = document.getElementById('references');
 let index = 0;
 let origin = null;
 function show(n, updateHash = true) {
   index = Math.max(0, Math.min(slides.length - 1, n));
   const active = document.activeElement;
   const focusWasOnSlide = active && active.closest('.slide');
   slides.forEach((s, i) => { s.hidden = i !== index; });
   number.textContent = `${String(index + 1).padStart(2, '0')} / ${slides.length}`;
   prev.disabled = index === 0;
   next.disabled = index === slides.length - 1;
   jump.value = slides[index].id;
   document.getElementById('progress-value').style.width = `${(index + 1) / slides.length * 100}%`;
   if (updateHash) history.replaceState(null, '', '#' + slides[index].id);
   if (focusWasOnSlide) slides[index].querySelector('h1,h2').focus({ preventScroll: true });
   window.scrollTo(0, 0);
 }
 function fromHash() {
   const found = slides.findIndex(s => '#' + s.id === location.hash);
   show(found < 0 ? 0 : found, false);
 }
 prev.addEventListener('click', () => show(index - 1));
 next.addEventListener('click', () => show(index + 1));
 jump.addEventListener('change', () => show(slides.findIndex(s => s.id === jump.value)));
 document.addEventListener('keydown', event => {
   if (dialog.open || event.altKey || event.ctrlKey || event.metaKey || event.shiftKey || event.target.closest('input,select,textarea,button,a')) return;
   if (event.key === 'ArrowRight') { event.preventDefault(); show(index + 1); }
   if (event.key === 'ArrowLeft') { event.preventDefault(); show(index - 1); }
   if (event.key === 'Home') { event.preventDefault(); show(0); }
   if (event.key === 'End') { event.preventDefault(); show(slides.length - 1); }
 });
 function openSources(source, trigger) {
   origin = trigger;
   dialog.showModal();
   const target = source ? document.getElementById('source-' + source) : document.getElementById('references-title');
   if (source) target.querySelector('h3').focus({ preventScroll: true });
   else document.getElementById('close-sources').focus({ preventScroll: true });
   if (source) target.scrollIntoView({ block: 'start', behavior:'instant' });
   else dialog.scrollTop = 0;
 }
 document.querySelectorAll('[data-source]').forEach(a => a.addEventListener('click', e => { e.preventDefault(); openSources(a.dataset.source, a); }));
 document.querySelectorAll('[data-open-sources]').forEach(b => b.addEventListener('click', () => openSources(null, b)));
 document.getElementById('close-sources').addEventListener('click', () => dialog.close());
 dialog.addEventListener('close', () => { if (origin) origin.focus({ preventScroll: true }); });
 window.addEventListener('hashchange', fromHash);
 document.body.classList.add('enhanced');
 fromHash();
})();
'''

parts = []
for i, s in enumerate(slides):
    heading = '' if i == 0 else f'<h2 id="{s["id"]}-title" tabindex="-1">{html.escape(s["title"])}</h2>'
    label = 'aria-label="從 Boom Bap 到 Rage"' if i == 0 else f'aria-labelledby="{s["id"]}-title"'
    body = s['body'].replace('<h1>', '<h1 tabindex="-1">')
    parts.append(f'<section class="slide {s["theme"]}" id="{s["id"]}" {label} data-goals="{" ".join(s["goals"])}"><p class="tag">{html.escape(s["tag"])}</p>{heading}<div class="slide-content">{body}</div></section>')

records = []
def date(value):
    return '未知' if value == 'unknown' else html.escape(value)
for sid, d in sources.items():
    author = d['author'].replace('; individual author unknown','；個人作者未知').replace('; individual catalog editor unknown','；個人目錄編輯未知')
    extra = '作品發行：2021-05-07。' if sid == 'S008' else ''
    records.append(f'''<article class="source-record" id="source-{sid.lower()}"><h3 tabindex="-1">{sid} · {html.escape(d['title'])}</h3>
<p>{html.escape(author)}<br>{html.escape(d['publisher'])}</p><p>發布：{date(d['published_date'])}　更新：{date(d['updated_date'])}。{extra}</p>
<p>{limits[sid]}</p><div class="source-links"><a href="{html.escape(d['read_url'])}" target="_blank" rel="noopener noreferrer">實際讀取網址（需網路）</a><a href="{html.escape(d['original_url'])}" target="_blank" rel="noopener noreferrer">原始網址（需網路）</a><a href="../../{d['path']}" target="_blank">Wiki 來源筆記</a></div></article>''')

options = ''.join(f'<option value="{s["id"]}">{i+1:02d}　{html.escape(s["title"])}</option>' for i,s in enumerate(slides))
doc = f'''<!doctype html>
<html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="以繁體中文比較 Boom bap、Trap 與 Rage 的聲音、地域背景及傳播方式。"><title>從 Boom Bap 到 Rage｜嘻哈風格發展</title><style>{css}</style></head>
<body><header class="topbar"><span class="brand">嘻哈風格發展</span><div class="top-actions"><span class="edition">LLM WIKI　2026.11</span><button type="button" data-open-sources>來源與延伸閱讀</button></div></header>
<noscript><p class="no-js">目前以連續閱讀模式呈現所有頁面與來源。啟用 JavaScript 後可使用翻頁導覽。</p></noscript>
<main id="deck">{''.join(parts)}</main>
<footer class="navigation" aria-label="簡報導覽"><div class="nav-left"><label class="sr-only" for="jump">跳至投影片</label><select id="jump">{options}</select></div><span class="keys">左右鍵翻頁　Home／End 到首末頁</span><div class="nav-right"><button type="button" id="previous" aria-label="上一頁">上一頁</button><span id="page-number" aria-live="polite" aria-atomic="true">01 / {len(slides)}</span><button type="button" id="next" aria-label="下一頁">下一頁</button></div></footer>
<div class="progress" aria-hidden="true"><span id="progress-value"></span></div>
<dialog id="references" aria-labelledby="references-title"><div class="dialog-top"><h2 id="references-title">來源與延伸閱讀</h2><button type="button" id="close-sources">關閉</button></div><div class="source-intro"><p>聲音敘述依文字來源，未完成錄音聆聽或音訊分析。重要觀點保留作者歸屬；作品年份、起源與影響分開理解。以下資訊可離線閱讀，外部連結需要網路。</p><p>延伸聆聽可由 S008 的〈Miss The Rage〉目錄進入；目錄與播放器不影響主文理解。簡報更新日期：{REVISION_DATE}；來源取得日期依 Wiki 筆記。</p></div>{''.join(records)}<div class="research"><a href="outline.md">逐頁大綱</a><a href="evidence-map.md">證據對照</a><a href="../../wiki/index.md">Wiki 索引</a></div></dialog>
<script>{js}</script></body></html>'''
HERE.mkdir(parents=True, exist_ok=True)
(HERE/'index.html').write_text(doc, encoding='utf-8')

def plain(s):
    return re.sub(r'\s+', ' ', html.unescape(re.sub('<[^>]+>',' ',s))).strip()

outline = ['# 逐頁大綱','', f'日期：{REVISION_DATE}（Asia/Taipei）。{len(slides)} 頁；依內容密度決定，未設定報告時長。', '',
           '核心目標：L01 基本聲音概念、L02 聲音差異、L03 形成條件、L04 世代變化及並行交叉。', '',
           '視覺：以文字、比較表及多軌事件表教學，不使用外部圖片、音訊或 CDN。時間表只定位選例。', '',
           '入口：[HTML](index.html)、[證據對照](evidence-map.md)、[檢查紀錄](review-log.md)。','',
           '新增 slide-14 接於 slide-04 之後，slide-15 接於 slide-09 之後；其餘 ID 保留，導覽頁碼依實際順序計算。', '',
           '## 必要術語與首次出現', '', '| 術語 | 首次出現頁面 ID | 給新手的白話解釋 | Wiki 主張與來源 E 定位 | 處理狀態 |', '| --- | --- | --- | --- | --- |']
for term,sid,explain,wiki,c,source,e in glossary:
    outline.append(f'| {term} | {sid} | {explain} | [{wiki}＋{c}](../../{wiki}#{c.lower()})、[{source}＋{e}](../../{sources[source]["path"]}#{e.lower()}) | 已與本次 HTML 首次解釋對照 |')
outline += ['', '## 大綱階段的學習目標核對', '',
            '- L01：slide-03／05／08 描述三種聲音，slide-10 並列比較；分類限制就近說明。',
            '- L02：slide-03 的鼓與取樣、05 的低頻與 flow、08 的合成器、15 的人聲，以及 09 的作品用途可互相比較。',
            '- L03：slide-04 的合作與地方場域、14 的媒體認可、06 的 mixtape、07 的平台發布，提供具體形成／流通條件；觀點保持作者歸屬。',
            '- L04：slide-11 區分作品節點與觀察時期，12 整理並行、延續與融合，15 以逐作品分類示範藝人與曲風不必重合。',
            '- 以上是大綱的 AI 教學檢核，不等同真人測試，也不取代本次全份 D1–D3。', '']
evidence = ['# 逐頁證據對照','', f'日期：{REVISION_DATE}。Wiki 主張 → 來源 E → raw P／原頁。C、E 不另創虛構定位。', '',
            '跨條目操作框架已先寫回 overview C07。封面為題名與範圍，沒有獨立歷史主張。聲音表述依文字來源，未宣稱聆聽。', '',
            '| 頁面 ID | 簡報主張 | 主張性質 | Wiki 路徑＋C 編號 | 來源 ID＋E 定位 | 限制與採用表述 |','| --- | --- | --- | --- | --- | --- |']
for s in slides:
    outline += [f'## {s["id"]}｜{s["title"]}', '', f'- 學習目標：{"、".join(s["goals"])}。', f'- 一件事：{s["point"]}', f'- 說明及內容：{plain(s["body"])}', f'- 例證選用理由：{s["reason"]}', f'- 視覺安排：{s["visual"]}', '- 證據：'+('；'.join(f'[{c["wiki"]}＋{c["c"]}](../../{c["wiki"]}#{c["c"].lower()})' for c in s['claims']) if s['claims'] else '封面題名／範圍，不作歷史定論。'), '']
    if not s['claims']:
        evidence.append(f'| {s["id"]} | 封面題名與範圍 | 編排 | 不適用 | 不適用 | 非歷史定論。 |')
    for c in s['claims']:
        refs = '、'.join(f'[{sid}＋{eid}](../../{sources[sid]["path"]}#{eid.lower()})' for sid,eid in c['refs'])
        evidence.append(f'| {s["id"]} | {c["text"]} | {c["kind"]} | [{c["wiki"]}＋{c["c"]}](../../{c["wiki"]}#{c["c"].lower()}) | {refs} | {c["limit"]} |')
evidence += ['', '## 採用來源與範圍', '', 'S001、S003、S004、S005、S007、S008、S009、S010，共 8 份來源用於簡報。S002（器材位元深度）與 S006（認證制度）未納教學版面。完整來源 metadata、取得範圍與 raw 連結沿用各筆記，不因簡報再計篇數。', '', '首版（2026-11-16）曾重開 S001、S004、S007，並補查術語來源 S010。本次（2026-11-17）採讀既有 Wiki、來源筆記及 raw；新增頁只使用現有 Atlanta C03、Rage C06 與 overview C06，沒有新增來源、重新聽取錄音或擴大外部日期／起源搜尋。', '', 'slide-11 的 2020 年作品另對照 [Rage C03](../../wiki/styles/rage.md#c03)與 [S007 E03](../../wiki/sources/s007-rise-of-rage-music.md#e03)。']
(HERE/'outline.md').write_text('\n'.join(outline)+'\n',encoding='utf-8')
(HERE/'evidence-map.md').write_text('\n'.join(evidence)+'\n',encoding='utf-8')
print(json.dumps({'slides':len(slides),'sources':used,'claims':sum(len(s['claims']) for s in slides),'html_bytes':(HERE/'index.html').stat().st_size},ensure_ascii=False))
