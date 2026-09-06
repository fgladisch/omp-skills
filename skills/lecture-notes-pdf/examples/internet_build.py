"""Pastel worksheet builder: 인터넷과 메타버스 1주차 3종 PDF."""
import os
import subprocess
import unicodedata
from pathlib import Path
from noteitmarkdown.print_layout import LecturePrintLayout

VAULT = Path("/Volumes/Dongmin_ssd/Obsidian Vault/인터넷과 메타버스")
SRC = VAULT / "1주차/1주차 강의노트"
OUT = VAULT / "1주차 본수업"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

LAYOUT = LecturePrintLayout(
    SRC / "figures",
    Path("/tmp/internet-figure-slices"),
)
figrow = LAYOUT.figrow
figstack = LAYOUT.figstack
figure_group = LAYOUT.figure_group
fig = LAYOUT.fig


def to_pdf(name: str, body: str) -> Path:
    OUT.mkdir(parents=True, exist_ok=True)
    html = LAYOUT.document(body)
    tmp = Path("/tmp") / (Path(name).stem + ".tmp.html")
    tmp.write_text(html, encoding="utf-8")
    pdf = OUT / name
    if pdf.exists():
        try:
            pdf.unlink()
        except FileNotFoundError:
            # exFAT lookup is normalization-insensitive but unlink is not:
            # resolve the exact on-disk name before deleting.
            for entry in os.listdir(OUT):
                if unicodedata.normalize("NFC", entry) == name:
                    Path(OUT / entry).unlink()
                    break
    r = subprocess.run(
        [CHROME, "--headless=new", "--no-pdf-header-footer", "--disable-gpu",
         "--font-render-hinting=none", f"--print-to-pdf={pdf}",
         tmp.resolve().as_uri()],
        capture_output=True, text=True, timeout=240)
    if r.returncode != 0:
        raise SystemExit(f"chrome fail {r.returncode}: {r.stderr[-1500:]}")
    return pdf


# ---------------- 1. 본강의노트+요약 ----------------
def build_notes() -> str:
    frow_early = figrow(
        "page-008-figure-cf57b8.png", "page-009-figure-07372e.png",
        "page-010-figure-77e7f8.png",
        caps=["인터넷 진화의 정점 (p.8)", "1:N 전달 구조 (p.9)",
              "정보의 물리적 한계 (p.10)"],
    )
    frow13 = figrow(
        "page-013-figure-a206bd.png", "page-013-figure-d9abcd.png",
        "page-013-figure-77951c.png", "page-013-figure-921cba.png",
        caps=["초기 네트워크 기록 1 (p.13)", "초기 네트워크 기록 2 (p.13)",
              "초기 네트워크 기록 3 (p.13)", "초기 네트워크 기록 4 (p.13)"],
    )
    frow21a = figrow(
        "page-021-figure-0ece3f.png", "page-021-figure-44cd65.png",
        "page-021-figure-638533.png", "page-021-figure-3b2986.png",
        caps=["WorldWideWeb (p.21)", "Mosaic (p.21)",
              "Netscape (p.21)", "IE (p.21)"],
    )
    frow21b = figrow(
        "page-021-figure-ba39d6.png", "page-021-figure-8175c8.png",
        "page-021-figure-6bc7a5.png", "page-021-figure-08c96f.png",
        caps=["Firefox (p.21)", "Safari (p.21)",
              "Chrome (p.21)", "Edge (p.21)"],
    )
    frow_portal = (
        figrow("page-022-figure-3e627a.png", caps=["포털 관문 (p.22)"])
        + figrow("page-023-figure-c0e47a.png", "page-024-figure-d6d762.png",
                 caps=["검색 점유율 90.8% (p.23)", "플랫폼 통합 (p.24)"])
    )
    frow_naver = figrow(
        "page-025-figure-dfe89d.png", "page-025-figure-300722.png",
        caps=["네이버 관문 예시 1 (p.25)", "네이버 관문 예시 2 (p.25)"],
    )
    frow_o2o = figrow(
        "page-027-figure-d574eb.png", "page-027-figure-ec4ad5.png",
        caps=["앱 O2O 연결 1 (p.27)", "앱 O2O 연결 2 (p.27)"],
    )
    frow_sns = figrow(
        "page-028-figure-02d82d.png", "page-029-figure-4f1369.png",
        caps=["관계망 전이 (p.28)", "UGC 1인 미디어 (p.29)"],
    )
    frow_web12 = figrow(
        "page-030-figure-9b6da0.png", "page-030-figure-86ecdd.png",
        caps=["Web 1.0 읽기 (p.30)", "Web 2.0 읽고 쓰기 (p.30)"],
        tall=True,
    )
    frow_dx = figrow(
        "page-032-figure-b6d568.png", "page-032-figure-4dfee9.png",
        "page-032-figure-5c3223.png",
        caps=["한계비용 제로 (p.32)", "네트워크 효과 (p.32)",
              "디지털 전환 (p.32)"],
    )
    return f"""
<div class='headband'><span>인터넷과 메타버스 · 1주차</span><span>인터넷에서 메타버스로</span></div>
<div class='cover'>
  <div class='chap'>Chapter 1 · 인터넷의 발전과 메타버스 입문</div>
  <h1>연결에서 머무는 공간까지</h1>
  <div class='sub'>분산·패킷·웹·포털·모바일에서 소유와 가상 경제로 · 본수업용 강의노트 + 1p 요약</div>
</div>
<div class='goals'>
<div class='gt'>학습 목표</div>
<ol>
<li>분산 네트워크와 패킷·TCP/IP 약속을 설명할 수 있다.</li>
<li>WWW·브라우저·포털·플랫폼 흐름을 연표로 정리할 수 있다.</li>
<li>모바일 O2O·Web 소유와 메타버스 경제를 구분할 수 있다.</li>
</ol>
</div>

<h2 class='sec'><span class='n'>0</span> 강의 안내 — 개념·사례로 읽는 한 학기</h2>
<div class='card'>
<b>목표 (p.3·p.4):</b> 인터넷 발전 과정에서 <span class='hl'>VR·AR·MR 확장현실</span>과 메타버스의 개념·구조를 이해한다.
메타버스를 <span class='hl'>인터넷 발전의 연장선에 있는 디지털 환경</span>으로 보고, 기술 기반·활용·사회 영향·한계와 <span class='hl'>AI 도입 변화</span>를 함께 다룬다.
특정 플랫폼 실습이 아니라 <span class='hl'>개념 이해와 사례 분석</span> 중심이며, 전공과 접목 가능성을 탐색한다.
<br><b>방식 (p.5):</b> 이론 중심 강의식 + 사례 분석·질의응답 병행, 기말 보고서로 종합, 수업자료는 매주 PDF 제공.
<table class='kv'>
<tr><th>평가</th><th>비중</th><th>형식</th></tr>
<tr><td>출석</td><td><span class='hl'>20</span></td><td>전자출결 중심</td></tr>
<tr><td>중간고사</td><td><span class='hl'>40</span></td><td>지필 · PPT 범위 기반</td></tr>
<tr><td>기말 보고서</td><td><span class='hl'>40</span></td><td>주제 지정 · AI 활용 가능</td></tr>
</table>
수업 내 온라인 활동 참여 권장 · 문의 <span class='hl'>tailer20@naver.com</span>
</div>
<div class='tip'><span class='t'>✎ 펜 메모 (p.6) —</span> “→ 대부분 PPT 기반”</div>

<h2 class='sec'><span class='n'>1</span> 인터넷 이전 — 소수가 만들고 다수가 받던 시절</h2>
<div class='card'>
메타버스는 <span class='hl'>인터넷 진화의 정점인 기술적 결집체</span>다. 텍스트에서 공간으로 바뀌는 인터페이스 역사를 따라가면 미래 가상 경제 구조가 보인다 (p.8).<br>
이전 정보 환경은 <span class='hl'>1:N 구조</span> — 신문·TV·라디오처럼 소수 공급자가 다수에게 전달하고, 편집권자가 정보를 통제하며, 수용자 선택·피드백이 제한됐다 (p.9).<br>
정보는 <span class='hl'>종이·필름 등 물리적 매체에 귀속</span>됐다. 도서관·아카이브 같은 물리적 보관 공간이 필수였고, 확산 속도는 물류 속도에 비례했다 (p.10).
</div>
{figure_group('인터넷 이전 정보 환경 (p.8 · p.10)', frow_early)}
<div class='warn'><span class='t'>맥락 —</span>
<b>도서관은 상징적 의미로 변했다.</b> 종이 논문을 뽑아 보는 일은 정독 의지에 가깝고, 평소 탐색은 온라인 바로 읽기로 바뀌었다. (강의녹음 11분대)</div>
<div class='tip'><span class='t'>✎ 펜 메모 (p.10) —</span> “⇒ 도서관은 상징적인 의미로 변할”</div>

<h2 class='sec'><span class='n'>2</span> 분산 네트워크와 ARPANET — 끊겨도 살아남는 연결</h2>
<div class='card'>
<span class='hl'>냉전 시대 핵전쟁 대비 통신망 유지 목적</span>으로 탄생했다. 중앙 서버가 파괴돼도 유지되는 <span class='hl'>분산 네트워크</span>를 지향했고,
<span class='hl'>1969년 미국 4개 대학 노드 최초 연결</span> 후 실험을 이어가 <span class='hl'>1990년대까지 유지</span>됐다 (p.11).
</div>
<div class='tip'><span class='t'>✎ 펜 메모 (p.11) —</span> “~ 1990년대까지 유지”</div>
{fig('page-012-figure-087734.png', 'ARPANET 연결 컴퓨터 IBM 360/95 (p.12)')}
{figure_group('초기 네트워크 기록 (p.13)', frow13)}
<div class='warn'><span class='t'>예습 헷갈림 ① —</span>
<b>군사적 기원 = 전쟁용으로만 쓰였다? ✗</b> 통신 유지·분산 연결 실험이 핵심이다. <b>중앙 집중과 분산</b>, <b>1969년</b> 연도를 구분하자.</div>

<h2 class='sec'><span class='n'>3</span> 패킷 교환과 TCP/IP — 서로 다른 컴퓨터의 공통 약속</h2>
<div class='card'>
<b>패킷 교환 (p.14·p.15):</b> 데이터를 작은 <span class='hl'>패킷 단위로 분할</span>해 보내고, <span class='hl'>다중 경로 전송</span>으로 효율·복구력을 확보한다.
현대 인터넷 전송의 핵심 기초다. 메일 본문·첨부처럼 덩어리 정보를 <span class='hl'>쪼개고 번호를 붙여</span> 순서가 뒤섞여도 다시 조립한다.
<div class='flow'>
<span class='step'>분할</span><span class='arr'>→</span>
<span class='step'>번호 부여</span><span class='arr'>→</span>
<span class='step'>분산 전송</span><span class='arr'>→</span>
<span class='step'>재조립</span>
</div>
<b>TCP/IP 등장 (p.16):</b> <span class='hl'>1983년 이기종 컴퓨터 간 표준 규약</span>. <span class='hl'>TCP = 정확한 전달</span>, <span class='hl'>IP = 주소 할당</span>으로 역할을 나눠 전 세계 망을 하나로 묶었다.
당시 대륙 간 연결은 <span class='hl'>전화선·모뎀</span> 기반이었고, 이후 광섬유 데이터망으로 확장됐다.<br>
<b>개방성 (p.17):</b> 특정 기업 소유가 아닌 <span class='hl'>공공 규약</span>이라 지키기만 하면 누구나 참여 가능한 <span class='hl'>허가 없는 혁신</span>이 열렸다. 메타버스 상호운용성 논의의 역사적 모태다.
</div>
<div class='formula'><div class='ft'>이 절의 흐름</div>
<div class='flow'>
<span class='step'>분산</span><span class='arr'>→</span>
<span class='step'>패킷</span><span class='arr'>→</span>
<span class='step'>TCP/IP</span><span class='arr'>→</span>
<span class='step'>개방성</span>
</div>
</div>
<div class='warn'><span class='t'>예습 헷갈림 ② —</span>
<b>TCP/IP 세부 구조를 외워야 한다? ✗</b> 헤더·프레임 명칭 암기가 아니라 <b>정확한 전달과 주소 할당의 분담</b>, <b>1983년 표준화</b>가 시험 핵심이다.</div>

<h2 class='sec'><span class='n'>4</span> WWW와 브라우저 — 주소만 알면 찾아가는 웹</h2>
<div class='card'>
<span class='hl'>팀 버너스 리의 HTTP·HTML 기반 정보 공유 시스템</span> (p.18). <span class='hl'>하이퍼텍스트</span>로 문서 사이를 자유롭게 이동하고,
<span class='hl'>URL 주소만으로 정보에 접근</span>한다. 최초 웹브라우저(WorldWideWeb)까지 직접 만들었다.
</div>
{fig('page-018-figure-22d658.png', 'WWW 정보 공유 시스템 (p.18)')}
{fig('page-019-figure-a9f60a.png', '하이퍼텍스트와 주소 체계 (p.19)')}
<div class='card'>
<span class='hl'>Mosaic·Netscape의 그래픽 UI 혁명</span> (p.20). 텍스트 위주에서 <span class='hl'>이미지까지 담은 시각 미디어</span>로 바뀌면서 일반 대중이 유입됐다.
Mosaic 제작진이 Netscape로 이어졌고, 디스켓 1장 수준의 가벼운 배포가 설치 장벽을 낮췄다.
</div>
<div class='tip'><span class='t'>✎ 펜 메모 (p.20) —</span> “이미지 정보를 쉽게 읽을 수 있게 됨”</div>
{fig('page-020-figure-1eda3c.png', '그래픽 웹의 시작 Mosaic·Netscape (p.20)')}
{figure_group('브라우저 연표 전반 (p.21)', frow21a)}
{figure_group('브라우저 연표 후반 (p.21)', frow21b)}
<div class='card'>
연표: <span class='hl'>1990 WorldWideWeb → 1993 Mosaic → 1994 Netscape → 1996 IE·Opera → 2002 Mozilla → 2003 Safari → 2004 Firefox → 2008 Chrome → 2015 Edge</span> (p.21).<br>
MS가 IE를 OS 기본 탑재·기업 압박으로 독점했고, 이후 반독점 논란과 Opera·Firefox·Safari·Chrome 경쟁으로 재편됐다.
</div>
<div class='warn'><span class='t'>예습 헷갈림 ③ —</span>
<b>월드와이드웹 = 인터넷 자체? ✗</b> 인터넷은 연결망, WWW는 그 위에서 주소·하이퍼텍스트로 문서를 공유하는 방식이다.</div>

<h2 class='sec'><span class='n'>5</span> 포털·플랫폼·데이터 — 모이는 곳이 시장이 된다</h2>
<div class='card'>
<span class='hl'>포털 시대 (p.22):</span> 야후·구글 같은 분류 서비스가 <span class='hl'>관문</span>이 됐다. 접속 시 가장 먼저 방문하는 출발점이자 탐색 비용을 낮춘 통로다.
</div>
{figure_group('포털과 플랫폼 (p.22 · p.24)', frow_portal)}
<div class='card'>
검색 점유율은 <span class='hl'>Google 90.8% vs 2위 Bing 4.03%</span> 수준으로 제시됐다 (p.23). Yandex·Yahoo Japan·Baidu 같은 지역 강자도 함께 기억하자.<br>
<span class='hl'>거대 플랫폼 (p.24):</span> 쇼핑·커뮤니티·결제가 통합됐다. 전자상거래가 기존 산업 구조를 재편했고, <span class='hl'>사용자 활동이 데이터로 변환</span>되는 시점이 열렸다.
모든 서비스의 연결점은 <span class='hl'>돈</span>이다. 사람이 모이면 거래·광고·수수료가 붙는다.<br>
<span class='hl'>네이버 예시 (p.25):</span> 메일·카페·블로그·스토어·뉴스·증권·지도·웹툰·멤버십·간편결제를 한 관문에 묶어 이탈을 막고, 관심사·활동 기록을 추천·광고로 연결한다.
</div>
{figure_group('네이버 관문 예시 (p.25)', frow_naver)}
<div class='warn'><span class='t'>예습 헷갈림 ④ —</span>
<b>포털 = 검색창? ✗</b> 검색을 포함한 <b>관문·광장</b>이다. <b>모이는 사람 수</b>가 값이며, 기록이 쌓여 다음 추천·거래를 만든다.</div>

<h2 class='sec'><span class='n'>6</span> 모바일·앱·소셜·생산 — 주머니 속 상시 연결</h2>
<div class='card'>
<span class='hl'>모바일 인터넷 (p.26):</span> <span class='hl'>2007년 아이폰</span>으로 이동성을 확보했다. 장소 제약 없는 <span class='hl'>상시 연결(Always-on)</span> 시대가 열리고 이용 시간과 데이터가 폭발했다.
컴퓨터 앞에서만 쓰던 연결이 걸어 다니며·기다리며 쓰는 생활이 됐다.
</div>
{fig('page-026-figure-714736.png', '주머니 속 혁명 모바일 인터넷 (p.26)')}
<div class='card'>
<span class='hl'>앱·O2O (p.27):</span> 브라우저 없는 전용 경험, <span class='hl'>GPS 기반 위치 서비스</span>와 배달·택시 같은 현실 산업이 결합했다. <span class='hl'>현실 공간과 디지털 정보가 실시간으로 일치</span>하기 시작했다.
배달의민족·콜택시→지도 호출 전환이 대표 사례다.
</div>
{figure_group('앱 O2O 연결 (p.27)', frow_o2o)}
<div class='card'>
<span class='hl'>SNS (p.28):</span> 사회적 관계망을 디지털로 전이했다. <span class='hl'>친구·팔로우 기반 인적 네트워크 자산화</span>, 현실·디지털 정체성의 공존·상호작용이 핵심이다.
X·Meta 같은 대형 사업자는 광고 등으로 수익화했다.<br>
<span class='hl'>UGC (p.29):</span> 사용자 직접 제작 콘텐츠가 주류가 됐다. 누구나 미디어가 되는 <span class='hl'>1인 미디어</span> 시대이자 메타버스 월드 제작 문화의 동력이다.<br>
<span class='hl'>Web 1.0 vs 2.0 (p.30):</span> 1.0 = <span class='hl'>읽기 중심 정적 포털</span>, 2.0 = <span class='hl'>참여·공유·개방의 읽고 쓰기</span>. 지금 주류는 사용자가 직접 생산하는 모델이다.
</div>
{figure_group('관계망과 사용자 생산 (p.28 · p.29)', frow_sns)}
{figure_group('Web 읽기에서 쓰기로 (p.30)', frow_web12)}
<div class='warn'><span class='t'>예습 헷갈림 ⑤ —</span>
<b>O2O = 앱 주문? ✗</b> 온라인 연결이 오프라인 행동으로 이어지는 <b>흐름 전체</b>다. <b>위치 + 시간 + 결제 + 기록</b>이 함께 돈다.</div>

<h2 class='sec'><span class='n'>7</span> 소유·Web 3.0·DX·메타버스 — 복사되는 세상에서 내 것 증명하기</h2>
<div class='card'>
<span class='hl'>Web 3.0과 소유 (p.31):</span> 개인에게 데이터 주권이 돌아가는 지향, <span class='hl'>블록체인으로 중앙 서버 없는 신뢰</span>를 만들고 가상 자산 소유로 메타버스 경제 기반을 형성한다.
단, 팀 버너스 리의 원래 web 3.0은 <span class='hl'>시맨틱웹(의미·데이터 연결)</span>이므로 대중적 소유 개념과 구분하자.<br>
비트코인 같은 가상자산이 개인 소유·수익 개념을 열었고, 한때 메타버스 붐과 묶였다.
</div>
{figure_group('산업 구조의 특징 (p.32)', frow_dx)}
<div class='card'>
<span class='hl'>산업 구조 특징 (p.32):</span> 정보 무한 복제·전송의 <span class='hl'>한계비용 제로</span>, 사용자 증가가 가치 상승으로 이어지는 <span class='hl'>네트워크 효과</span>,
오프라인 산업 전반의 <span class='hl'>디지털 전환(DX)</span>이 함께 간다. 음악·미디어 1개를 만들면 무제한 복제·수익 기회로 이어진다.<br>
<span class='hl'>기술 흐름 (p.33):</span> 인터페이스는 <span class='hl'>텍스트 → 영상 → 3D 실감 공간</span>, 통신은 <span class='hl'>5G/6G 대용량 전송</span>이 받친다.
보는 인터넷에서 <span class='hl'>머무는 공간으로서의 인터넷</span>으로 이동한다.
</div>
{fig('page-033-figure-e0a63c.png', '메타버스로 이어지는 기술 흐름 (p.33)')}
<div class='card'>
<span class='hl'>연결의 확장 (p.34):</span> 물리적 한계를 넘는 연결 범위가 계속 넓어진다. <span class='hl'>AI 도입으로 정보 이용 개념이 바뀌고</span>,
지향할 가상 세계 모델에 대한 고찰이 필요하다. AI가 차세대 인터넷 흐름의 한 축을 맡고 있다.
</div>
{fig('page-034-figure-6d4b8a.png', '연결 범위 확장과 AI 변화 (p.34)')}
<div class='warn'><span class='t'>예습 헷갈림 ⑥ —</span>
<b>블록체인 = 메타버스? ✗</b> 블록체인은 <b>소유를 증명하는 기술</b>, 메타버스는 그 위에서 <b>거래가 일어나는 가상 경제 공간</b>이다.</div>

<section class='summary-page'>
<h2 class='sec'>개념의 핵심 TIP — 한 장 정리</h2>
<div class='summary-grid'>
<div class='sum-box'>
<span class='st'>📡 분산·패킷</span><br>중앙 파괴 대비 · 1969년 4개 · 쪼개고 번호 붙여 재조립</div>
<div class='sum-box'>
<span class='st'>🤝 TCP/IP·개방성</span><br>1983년 표준 · TCP 전달 + IP 주소 · 허가 없는 혁신</div>
<div class='sum-box'>
<span class='st'>🌐 웹·브라우저</span><br>버너스리 HTTP·HTML·URL · Mosaic 그래픽 · IE→Chrome</div>
</div>
<div class='summary-grid'>
<div class='sum-box'>
<span class='st'>🚪 포털·플랫폼</span><br>관문이 시장 · Google 90.8% · 활동이 데이터·돈</div>
<div class='sum-box'>
<span class='st'>📱 모바일·소셜</span><br>2007 상시연결 · O2O 현실일치 · 관계 자산·UGC</div>
<div class='sum-box'>
<span class='st'>🔑 소유·메타버스</span><br>Web1 읽기→Web2 쓰기→소유 증명 · 머무는 공간</div>
</div>
<div class='card'><b>한 줄 핵심:</b>
<span class='hl'>메타버스는 유행 기술이 아니라 인터넷 발전의 연장선에 있는 디지털 환경이다.</span></div>
<div class='footer'><span>인터넷과 메타버스 1주차 · 본수업용 (강의노트 35쪽 + 강의녹음 기반)</span><span>Paperlogy</span></div>
</section>
"""


# ---------------- 2. 복습학습지 ----------------
def build_worksheet() -> str:
    return f"""
<div class='headband'><span>인터넷과 메타버스 · 1주차 복습학습지</span><span>총 400점 · 권장 210분</span></div>
<div class='cover'>
  <div class='chap'>Textbook Review · 인터넷에서 메타버스로</div>
  <h1>개념서 + 문제집</h1>
  <div class='sub'>이름: ______ &nbsp;&nbsp; 날짜: ______ &nbsp;&nbsp; 시작 시각: ______ &nbsp;&nbsp; 종료 시각: ______</div>
</div>
<div class='card'>
<b>사용법 (수학 교과서처럼):</b> 각 단원은 <span class='hl'>① 내 필기 되살리기 → ② 개념 정리 읽기 → ③ 개념 확인 문제 풀기</span> 순서다.
막히면 △ 표시 후 넘어갔다가 검산 시간에 복귀한다. 문항 번호는 해답지와 그대로 이어진다.
<table class='kv'>
<tr><th>단원</th><th>범위</th><th>확인 문제</th><th>권장 시간</th></tr>
<tr><td>Unit 0 · 강의 안내</td><td>p.2~6</td><td>— (읽기)</td><td>10분</td></tr>
<tr><td>Unit 1 · 인터넷 이전</td><td>p.7~10</td><td>17, 23</td><td>10분</td></tr>
<tr><td>Unit 2 · 분산과 ARPANET</td><td>p.11~13</td><td>1, 13</td><td>10분</td></tr>
<tr><td>Unit 3 · 패킷·TCP/IP</td><td>p.14~17</td><td>2, 3, 14, 18, 24, 25, 33, 34, 43</td><td>30분</td></tr>
<tr><td>Unit 4 · WWW·브라우저</td><td>p.18~21</td><td>4, 5, 6, 15, 19, 26, 27, 28, 35, 42</td><td>35분</td></tr>
<tr><td>Unit 5 · 포털·플랫폼</td><td>p.22~25</td><td>7, 8, 20, 21, 29, 36, 44, 45</td><td>30분</td></tr>
<tr><td>Unit 6 · 모바일·소셜</td><td>p.26~30</td><td>9, 10, 11, 16, 30, 31, 37, 38, 46, 47</td><td>35분</td></tr>
<tr><td>Unit 7 · 소유·메타버스</td><td>p.31~34</td><td>12, 22, 32, 39, 48</td><td>20분</td></tr>
<tr><td>종합 · 한 학기 관통</td><td>전체</td><td>40, 41</td><td>15분</td></tr>
<tr><td>검산·오답 정리</td><td>전 문항</td><td>—</td><td>15분</td></tr>
</table>
</div>

<h2 class='sec'>Unit 0 · 강의 안내 — 무엇을 배우는 과목인가 (p.2~6)</h2>
<div class='card'>
이 과목은 인터넷 발전 과정에서 <span class='hl'>VR·AR·MR 확장현실</span>과 메타버스의 개념·구조를 이해하는 것이 목표다 (p.3).
메타버스를 유행 기술이 아니라 <span class='hl'>인터넷 발전의 연장선에 있는 디지털 환경</span>으로 본다.
수업은 <span class='hl'>이론 중심 강의식 + 사례 분석·질의응답</span>, 평가는 <span class='hl'>출석 20 · 중간고사 40 · 기말 보고서 40</span>이다 (p.5·p.6).
중간고사는 PPT 범위 기반 지필, 기말 보고서는 지정 주제로 AI 활용이 가능하다.
</div>
<div class='tip'><span class='t'>✎ 내 필기 되살리기 —</span> p.6 여백에 남은 펜 메모다. p.5 메모는 형광펜이라 제외됐다.
<br>판독문: “→ 대부분 PPT 기반” (p.6)</div>

<h2 class='sec'>Unit 1 · 인터넷 이전 — 소수가 만들고 다수가 받던 시절 (p.7~10)</h2>
<div class='card'>
<b>개념 1 — 1:N 구조:</b> 신문·TV·라디오처럼 <span class='hl'>소수 공급자가 다수에게 일방 전달</span>하고, 편집권자가 정보를 통제한다. 수용자의 선택·피드백은 제한된다 (p.9).<br>
<b>개념 2 — 물리적 한계:</b> 정보가 <span class='hl'>종이·필름에 귀속</span>돼 도서관·아카이브 같은 보관 공간이 필수였고, 확산 속도는 물류 속도에 비례했다 (p.10).<br>
<b>개념 3 — 정점 명제:</b> 메타버스는 <span class='hl'>인터넷 진화의 정점인 기술적 결집체</span>다. 텍스트→공간으로 바뀌는 인터페이스 역사를 따라가면 가상 경제 구조가 보인다 (p.8).
</div>
<div class='tip'><span class='t'>✎ 내 필기 되살리기 —</span> p.10 여백에 남은 펜 메모다.
<br>판독문: “⇒ 도서관은 상징적인 의미로 변할”</div>
<div class='q'><span class='no'>17</span><span class='tag'>빈칸 · 4점</span>(p.9) 인터넷 이전은 ( &nbsp;&nbsp;&nbsp; ) 구조, 소수 공급자의 ( &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; )에 의한 통제, 수용자의 선택·( &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ) 제한이 특징이다.</div>
<div class='q'><span class='no'>23</span><span class='tag'>단답 · 8점</span>(p.9·p.11) 1:N 정보 구조와 분산 네트워크를 한 줄씩 구분하시오.<div class='write'></div></div>

<h2 class='sec'>Unit 2 · 분산 네트워크와 ARPANET — 끊겨도 살아남는 연결 (p.11~13)</h2>
<div class='card'>
<b>개념 1 — 탄생 배경:</b> <span class='hl'>냉전 시대 핵전쟁 대비 통신망 유지 목적</span>, 중앙 서버가 파괴돼도 유지되는 <span class='hl'>분산 네트워크</span> 지향 (p.11).<br>
<b>개념 2 — 연표:</b> <span class='hl'>1969년 미국 4개 대학 노드 최초 연결</span> → 확장 → <span class='hl'>1990년대까지 유지</span>. ARPANET 연결 컴퓨터의 예가 IBM 360/95다 (p.12).<br>
<b>오해 주의:</b> 군사적 기원 = 전쟁용으로만 쓰였다? ✗ 통신 유지·분산 연결 실험이 핵심이다.
</div>
<div class='tip'><span class='t'>✎ 내 필기 되살리기 —</span> p.11 여백에 남은 펜 메모다.
<br>판독문: “~ 1990년대까지 유지”</div>
<div class='q'><span class='no'>1</span><span class='tag'>O/X · 5점</span>ARPANET은 중앙 서버 파괴에도 유지되는 분산 네트워크를 지향했다. (p.11) <span class='ox'>O &nbsp; X</span></div>
<div class='q'><span class='no'>13</span><span class='tag'>빈칸 · 4점</span>(p.11) ( &nbsp;&nbsp;&nbsp;&nbsp; )년 미국 ( &nbsp;&nbsp; )개 대학 연결 → ARPANET 시작 → ( &nbsp;&nbsp;&nbsp;&nbsp; )년대까지 유지.</div>

<h2 class='sec'>Unit 3 · 패킷 교환과 TCP/IP — 서로 다른 컴퓨터의 공통 약속 (p.14~17)</h2>
<div class='card'>
<b>개념 1 — 패킷 교환:</b> 데이터를 작은 <span class='hl'>패킷 단위로 분할 → 번호 부여 → 다중 경로 전송 → 재조립</span>. 순서가 뒤섞여도 번호대로 다시 맞추면 정확한 정보가 복원된다 (p.14·p.15).<br>
<b>개념 2 — TCP/IP:</b> <span class='hl'>1983년 이기종 컴퓨터 간 표준 규약</span>. <span class='hl'>TCP = 정확한 전달</span>, <span class='hl'>IP = 주소 할당</span>으로 역할을 나눴다. 당시 연결은 전화선·모뎀 기반이었다 (p.16).<br>
<b>개념 3 — 개방성:</b> 특정 기업 소유가 아닌 <span class='hl'>공공 규약</span>이라 지키기만 하면 누구나 참여 가능한 <span class='hl'>허가 없는 혁신</span>. 메타버스 상호운용성 논의의 역사적 모태다 (p.17).
<div class='tip'><span class='t'>✎ 내 필기 —</span> 이 단원에는 펜 손글씨가 없다. p.14·p.16·p.17 여백 메모는 형광펜이라 제외됐다. 위 개념 3개를 밑줄 치고 외우자.</div>
<div class='q'><span class='no'>2</span><span class='tag'>O/X · 5점</span>패킷 교환에서는 데이터를 나누지 않고 한 번에 보내야 정확하다. (p.14) <span class='ox'>O &nbsp; X</span></div>
<div class='q'><span class='no'>3</span><span class='tag'>O/X · 5점</span>TCP/IP 표준화는 1983년에 이기종 컴퓨터 연결을 위해 정해졌다. (p.16) <span class='ox'>O &nbsp; X</span></div>
<div class='q'><span class='no'>14</span><span class='tag'>빈칸 · 4점</span>(p.16) TCP는 ( &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ), IP는 ( &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ) 역할을 분담한다.</div>
<div class='q'><span class='no'>18</span><span class='tag'>빈칸 · 4점</span>(녹음) 당시 연결은 ( &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ) 기반이었고, 이후 ( &nbsp;&nbsp;&nbsp; ) 데이터망으로 확장됐다.</div>
<div class='q'><span class='no'>24</span><span class='tag'>단답 · 8점</span>(p.14) 패킷 교환 4단계(분할·번호·전송·재조립)를 순서대로 쓰시오.<div class='write'></div></div>
<div class='q'><span class='no'>25</span><span class='tag'>단답 · 8점</span>(p.17) 허가 없는 혁신이 가능했던 이유를 표준화와 연결해 쓰시오.<div class='write'></div></div>
<div class='q'><span class='no'>33</span><span class='tag'>서술 · 15점</span>(p.14) 패킷 분할·번호·재조립 과정을 쓰고, 순서가 뒤섞여도 정확한 정보가 복원되는 이유를 메일 예시로 설명하시오.<div class='write tall'></div></div>
<div class='q'><span class='no'>34</span><span class='tag'>서술 · 15점</span>(p.16·p.17) TCP/IP 역할 분담과 1983년 표준화 의미를 쓰고, 개방성이 메타버스 상호운용 논의와 어떻게 연결되는지 설명하시오.<div class='write tall'></div></div>
<div class='q'><span class='no'>43</span><span class='tag'>도표 · 15점</span>패킷 교환 개념도(분할·번호·다중경로·재조립)를 그리고 번호의 역할을 화살표로 표시하시오.<div class='write tall'></div></div>

<h2 class='sec'>Unit 4 · WWW와 브라우저 — 주소만 알면 찾아가는 웹 (p.18~21)</h2>
<div class='card'>
<b>개념 1 — WWW 3요소:</b> 팀 버너스 리의 <span class='hl'>HTTP·HTML 기반 정보 공유</span>, <span class='hl'>하이퍼텍스트</span>로 문서 이동, <span class='hl'>URL 주소만으로 접근</span>. 최초 웹브라우저까지 직접 만들었다 (p.18).<br>
<b>개념 2 — 그래픽 혁명:</b> <span class='hl'>Mosaic·Netscape가 이미지를 담은 시각 미디어</span>로 바꾸면서 대중이 유입됐다. 디스켓 1장 수준의 가벼운 배포가 설치 장벽을 낮췄다 (p.20).<br>
<b>개념 3 — 연표:</b> 1990 WWW → 1993 Mosaic → 1994 Netscape → 1996 IE·Opera → 2002 Mozilla → 2003 Safari → 2004 Firefox → 2008 Chrome → 2015 Edge (p.21). IE 독점 → 반독점 논란 → 재편.
<div class='tip'><span class='t'>✎ 내 필기 되살리기 —</span> p.20 여백에 남은 펜 메모다.
<br>판독문: “이미지 정보를 쉽게 읽을 수 있게 됨”</div>
<div class='q'><span class='no'>4</span><span class='tag'>O/X · 5점</span>WWW는 인터넷 연결망 자체와 같은 말이다. (p.18) <span class='ox'>O &nbsp; X</span></div>
<div class='q'><span class='no'>5</span><span class='tag'>O/X · 5점</span>Mosaic은 텍스트만 보여주는 브라우저였다. (p.20) <span class='ox'>O &nbsp; X</span></div>
<div class='q'><span class='no'>6</span><span class='tag'>O/X · 5점</span>IE 독점 이후 브라우저 경쟁은 멈췄다. (p.21) <span class='ox'>O &nbsp; X</span></div>
<div class='q'><span class='no'>15</span><span class='tag'>빈칸 · 4점</span>(p.18) WWW 3요소: ( &nbsp;&nbsp;&nbsp;&nbsp; ) · ( &nbsp;&nbsp;&nbsp;&nbsp; ) · ( &nbsp;&nbsp;&nbsp;&nbsp; ), 연결 방식은 ( &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; )텍스트.</div>
<div class='q'><span class='no'>19</span><span class='tag'>빈칸 · 4점</span>(p.21) ( &nbsp;&nbsp;&nbsp;&nbsp; ) WorldWideWeb → ( &nbsp;&nbsp;&nbsp;&nbsp; ) Mosaic → ( &nbsp;&nbsp;&nbsp;&nbsp; ) Netscape → 1996 IE.</div>
<div class='q'><span class='no'>26</span><span class='tag'>단답 · 8점</span>(p.18) 하이퍼텍스트와 URL이 가져온 사용자 편의 2가지를 쓰시오.<div class='write'></div></div>
<div class='q'><span class='no'>27</span><span class='tag'>단답 · 8점</span>(p.20) Mosaic의 혁명적 의미와 디스켓 배포의 의미를 한 줄씩 쓰시오.<div class='write'></div></div>
<div class='q'><span class='no'>28</span><span class='tag'>단답 · 8점</span>(p.21) IE 독점에서 Chrome 재편까지의 과정을 3단계로 쓰시오.<div class='write'></div></div>
<div class='q'><span class='no'>35</span><span class='tag'>서술 · 15점</span>(p.18·p.20) 버너스리의 3요소와 최초 브라우저를 쓰고, Mosaic·Netscape가 대중 유입의 계기가 된 이유를 설명하시오.<div class='write tall'></div></div>
<div class='q'><span class='no'>42</span><span class='tag'>도표 · 15점</span>브라우저 연표(1990·1993·1994·1996·2008·2015)를 그리고 Mosaic의 의미를 표시하시오.<div class='write tall'></div></div>

<h2 class='sec'>Unit 5 · 포털·플랫폼·데이터 — 모이는 곳이 시장이 된다 (p.22~25)</h2>
<div class='card'>
<b>개념 1 — 포털 관문:</b> 야후·구글 같은 분류 서비스가 <span class='hl'>가장 먼저 방문하는 관문</span>이 돼 탐색 비용을 낮췄다. Yahoo는 사람이 정리하는 목록, Google은 링크 순위 방식이다 (p.22).<br>
<b>개념 2 — 점유율:</b> <span class='hl'>Google 90.8% vs 2위 Bing 4.03%</span> 수준. Yandex·Yahoo Japan·Baidu 같은 지역 강자도 있다 (p.23).<br>
<b>개념 3 — 플랫폼·데이터:</b> <span class='hl'>쇼핑·커뮤니티·결제 통합</span>으로 전자상거래가 재편됐고, <span class='hl'>사용자 활동이 데이터로 변환</span>되는 시점이 열렸다. 네이버는 메일·카페·멤버십·결제를 한 관문에 묶는다 (p.24·p.25). 모든 서비스의 연결점은 돈이다.
</div>
<div class='tip'><span class='t'>✎ 내 필기 —</span> 이 단원 여백 필기는 없다. 위 개념 3개를 밑줄 치고 외우자.</div>
<div class='q'><span class='no'>7</span><span class='tag'>O/X · 5점</span>포털의 값은 화면 크기보다 매일 지나가는 사람 수에서 나온다. (p.22) <span class='ox'>O &nbsp; X</span></div>
<div class='q'><span class='no'>8</span><span class='tag'>O/X · 5점</span>사용자 활동이 가치 있는 데이터로 변환되는 시점이 플랫폼 시대에 열렸다. (p.24) <span class='ox'>O &nbsp; X</span></div>
<div class='q'><span class='no'>20</span><span class='tag'>빈칸 · 4점</span>(p.22) Yahoo는 사람이 정리하는 ( &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ) 방식, Google은 링크로 매기는 ( &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ) 방식이다.</div>
<div class='q'><span class='no'>21</span><span class='tag'>빈칸 · 4점</span>(p.24) 플랫폼 통합 3요소 ( &nbsp;&nbsp;&nbsp; )·( &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; )·( &nbsp;&nbsp; ), 이후 사용자 ( &nbsp;&nbsp;&nbsp; )이 데이터로 변환된다.</div>
<div class='q'><span class='no'>29</span><span class='tag'>단답 · 8점</span>(p.22) 포털이 탐색비용을 낮춘 방식 2가지(Yahoo·Google)를 쓰시오.<div class='write'></div></div>
<div class='q'><span class='no'>36</span><span class='tag'>서술 · 15점</span>(p.22·p.25) 포털 관문이 사람을 모으고 활동이 데이터·돈이 되는 흐름을 야후·구글·네이버 사례로 설명하시오.<div class='write tall'></div></div>
<div class='q'><span class='no'>44</span><span class='tag'>도표 · 15점</span>관문 → 집중 → 쇼핑·결제 → 데이터 → 광고·추천 순환도를 그리고 사람 수=값 관계를 표시하시오.<div class='write tall'></div></div>
<div class='q'><span class='no'>45</span><span class='tag'>적용 · 10점</span>(p.25) 네이버 메인(메일·카페·멤버십·결제)이 사용자를 붙잡는 원리 2가지를 쓰고, 각 기능이 어디에 대응되는지 쓰시오.<div class='write tall'></div></div>

<h2 class='sec'>Unit 6 · 모바일·앱·소셜·생산 — 주머니 속 상시 연결 (p.26~30)</h2>
<div class='card'>
<b>개념 1 — 모바일:</b> <span class='hl'>2007년 아이폰</span>으로 장소 제약 없는 <span class='hl'>상시 연결(Always-on)</span> 시대. 이용 시간·데이터가 폭발했다 (p.26).<br>
<b>개념 2 — 앱·O2O:</b> 브라우저 없는 전용 경험, <span class='hl'>GPS 기반 위치 서비스</span>와 배달·택시의 결합. <span class='hl'>현실 공간과 디지털 정보가 실시간으로 일치</span>한다. O2O는 앱 주문 화면이 아니라 온라인→오프라인 흐름 전체다 (p.27).<br>
<b>개념 3 — SNS·UGC:</b> <span class='hl'>친구·팔로우 기반 인적 네트워크 자산화</span> (p.28), <span class='hl'>사용자 직접 제작 콘텐츠(UGC)</span>의 주류화와 1인 미디어 시대 (p.29).<br>
<b>개념 4 — Web 1.0 vs 2.0:</b> 1.0 = <span class='hl'>읽기 중심 정적 포털</span>, 2.0 = <span class='hl'>참여·공유·개방의 읽고 쓰기</span> (p.30).
<div class='tip'><span class='t'>✎ 내 필기 —</span> 이 단원에는 펜 손글씨가 없다. p.26 여백 메모는 형광펜이라 제외됐다. 위 개념 4개를 밑줄 치고 외우자.</div>
<div class='q'><span class='no'>9</span><span class='tag'>O/X · 5점</span>O2O는 앱 주문 화면만을 가리킨다. (p.27) <span class='ox'>O &nbsp; X</span></div>
<div class='q'><span class='no'>10</span><span class='tag'>O/X · 5점</span>UGC는 사용자가 직접 만드는 콘텐츠가 주류가 된 흐름이다. (p.29) <span class='ox'>O &nbsp; X</span></div>
<div class='q'><span class='no'>11</span><span class='tag'>O/X · 5점</span>Web 2.0은 정보를 읽기만 하는 정적 포털 시대이다. (p.30) <span class='ox'>O &nbsp; X</span></div>
<div class='q'><span class='no'>16</span><span class='tag'>빈칸 · 4점</span>(p.26·p.30) ( &nbsp;&nbsp;&nbsp;&nbsp; )년 아이폰 → 상시 연결 → Web 1.0 ( &nbsp;&nbsp; )에서 Web 2.0 ( &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; )로.</div>
<div class='q'><span class='no'>30</span><span class='tag'>단답 · 8점</span>(p.27) O2O를 정의하고 배달·택시·픽업 중 1개 사례를 쓰시오.<div class='write'></div></div>
<div class='q'><span class='no'>31</span><span class='tag'>단답 · 8점</span>(p.29) UGC와 1인 미디어를 정의하고 예시 1개를 쓰시오.<div class='write'></div></div>
<div class='q'><span class='no'>37</span><span class='tag'>서술 · 15점</span>(p.26) 2007년 아이폰 이후 상시 연결이 이용 시간·데이터 폭발로 이어진 경로를 장소·시간·돈 3축으로 설명하시오.<div class='write tall'></div></div>
<div class='q'><span class='no'>38</span><span class='tag'>서술 · 15점</span>(p.28·p.29) SNS 관계 자산화 과정(전이·축적·자산화)과 UGC 주류화를 쓰고, 메타버스 월드 제작 문화와 어떻게 이어지는지 설명하시오.<div class='write tall'></div></div>
<div class='q'><span class='no'>46</span><span class='tag'>적용 · 10점</span>(p.27) 배달앱 주문→GPS→조리→픽업→별점 흐름을 온라인/오프라인으로 구분해 설계하고, 각 단계 주체를 쓰시오.<div class='write tall'></div></div>
<div class='q'><span class='no'>47</span><span class='tag'>적용 · 10점</span>(p.29) 기업 제작 콘텐츠와 UGC를 가르는 기준 1개를 세우고, 영역별 예시를 2개씩 쓰시오.<div class='write tall'></div></div>

<h2 class='sec'>Unit 7 · 소유·Web 3.0·DX·메타버스 — 복사되는 세상에서 내 것 증명하기 (p.31~34)</h2>
<div class='card'>
<b>개념 1 — Web 3.0과 소유:</b> 개인에게 데이터 주권이 돌아가는 지향, <span class='hl'>블록체인으로 중앙 서버 없는 신뢰</span>, 가상 자산 소유로 메타버스 경제 기반 형성. 단, 버너스 리의 원래 web 3.0은 <span class='hl'>시맨틱웹(의미·데이터 연결)</span>이다 (p.31).<br>
<b>개념 2 — 산업 구조:</b> 정보 무한 복제·전송의 <span class='hl'>한계비용 제로</span>, 사용자 증가가 가치 상승으로 이어지는 <span class='hl'>네트워크 효과</span>, 오프라인 전반의 <span class='hl'>디지털 전환(DX)</span> (p.32).<br>
<b>개념 3 — 기술 흐름:</b> 인터페이스 <span class='hl'>텍스트 → 영상 → 3D 실감 공간</span>, 통신 <span class='hl'>5G/6G 대용량 전송</span>. 보는 인터넷에서 <span class='hl'>머무는 공간으로서의 인터넷</span>으로 (p.33). AI가 정보 이용 개념을 바꾸고 있다 (p.34).<br>
<b>구분:</b> 블록체인은 <b>소유를 증명하는 기술</b>, 메타버스는 그 위에서 <b>거래가 일어나는 가상 경제 공간</b>이다.
</div>
<div class='tip'><span class='t'>✎ 내 필기 —</span> 이 단원 여백 필기는 없다. 위 구분 1줄을 소리 내어 읽고 외우자.</div>
<div class='q'><span class='no'>12</span><span class='tag'>O/X · 5점</span>블록체인과 메타버스는 같은 것을 부르는 다른 이름이다. (p.31) <span class='ox'>O &nbsp; X</span></div>
<div class='q'><span class='no'>22</span><span class='tag'>빈칸 · 4점</span>(p.31) 버너스 리의 원래 web 3.0은 ( &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; )웹, 대중적 web 3.0은 개인 ( &nbsp;&nbsp;&nbsp; )·수익 개념이다.</div>
<div class='q'><span class='no'>32</span><span class='tag'>단답 · 8점</span>(p.31) 버너스 리의 web 3.0 원래 개념과 대중적 web 3.0 개념을 구분하시오.<div class='write'></div></div>
<div class='q'><span class='no'>39</span><span class='tag'>서술 · 15점</span>(p.31·p.32) 블록체인과 메타버스를 혼동하지 않고, 한계비용 제로·네트워크 효과와 연결해 가상 경제 기반을 설명하시오.<div class='write tall'></div></div>
<div class='q'><span class='no'>48</span><span class='tag'>적용 · 10점</span>(p.31) "복사하면 주인이 여럿 아닌가?"라는 친구 질문에 답하는 5줄 설명문을 쓰시오(증명/공간 구분 포함).<div class='write tall'></div></div>

<h2 class='sec'>종합 · 한 학기를 관통하는 명제 (전체 · 권장 15분)</h2>
<div class='q'><span class='no'>40</span><span class='tag'>서술 · 15점</span>(p.3·p.34) "메타버스는 인터넷 연장선의 디지털 환경이다"를 한 학기 관통 명제로 풀고, AI의 현재 위치를 함께 설명하시오.<div class='write tall'></div></div>
<div class='q'><span class='no'>41</span><span class='tag'>도표 · 15점</span>분산 → 패킷 → TCP/IP → WWW → 브라우저 → 포털 → 모바일 → 소유·메타버스 흐름도를 그리고 각 단계 핵심어를 표시하시오.<div class='write tall'></div></div>
<div class='card'><b>검산 15분:</b> O/X·빈칸은 해답지로 즉시 채점하고, 서술·도표는 채점 포인트의 굵은 글씨 키워드가 들어갔는지 밑줄로 확인한다. 빠진 키워드의 강의노트 쪽수를 오답 노트에 적는다.</div>
<div class='footer'><span>인터넷과 메타버스 1주차 복습학습지 · 총 400점 · 권장 210분</span><span>Paperlogy</span></div>
"""


# ---------------- 3. 해답지 ----------------
def build_answers() -> str:
    return """
<div class='headband'><span>인터넷과 메타버스 · 1주차 해답지</span><span>총 400점</span></div>
<div class='cover'>
  <div class='chap'>Answer Key · 인터넷에서 메타버스로</div>
  <h1>복습학습지 해답 + 채점 포인트</h1>
  <div class='sub'>강의노트 35쪽 + 강의녹음 근거 · 부분점수 허용 · 오답은 해당 번호 해설부터 복습</div>
</div>

<h2 class='sec'>A · O / X 해답 (각 5점 · 60점)</h2>
<div class='q'><span class='no'>1</span><b>O</b><div class='ans'>핵전쟁 대비 <b>분산 유지</b>가 목적. 중앙 집중 서술 시 오답.</div></div>
<div class='q'><span class='no'>2</span><b>X</b><div class='ans'><b>작게 쪼개고 번호를 붙여</b> 보내야 다중 경로·복원에 강하다.</div></div>
<div class='q'><span class='no'>3</span><b>O</b><div class='ans'><b>1983년·이기종 연결</b>이 핵심. 연도 오류 시 오답.</div></div>
<div class='q'><span class='no'>4</span><b>X</b><div class='ans'>인터넷은 망, WWW는 <b>주소·하이퍼텍스트 공유 방식</b>이다.</div></div>
<div class='q'><span class='no'>5</span><b>X</b><div class='ans'>Mosaic부터 <b>이미지·그래픽</b>을 담았다. 텍스트만 서술 시 오답.</div></div>
<div class='q'><span class='no'>6</span><b>X</b><div class='ans'>반독점 논란 후 Opera·Firefox·Safari·<b>Chrome 재편</b>이 이어졌다.</div></div>
<div class='q'><span class='no'>7</span><b>O</b><div class='ans'><b>매일 지나가는 사람 수</b>가 값이다. Google 90.8% 수치가 근거.</div></div>
<div class='q'><span class='no'>8</span><b>O</b><div class='ans'>쇼핑·커뮤니티·결제 통합 후 <b>활동이 데이터로 변환</b>됐다.</div></div>
<div class='q'><span class='no'>9</span><b>X</b><div class='ans'>앱 주문만이 아니라 <b>온라인→오프라인 흐름 전체</b>다.</div></div>
<div class='q'><span class='no'>10</span><b>O</b><div class='ans'>UGC = <b>사용자 직접 제작 콘텐츠</b>, 1인 미디어·월드제작의 동력.</div></div>
<div class='q'><span class='no'>11</span><b>X</b><div class='ans'>Web 2.0은 <b>참여·공유·개방의 읽고 쓰기</b>다. 읽기만 서술 시 오답.</div></div>
<div class='q'><span class='no'>12</span><b>X</b><div class='ans'><b>증명 기술 vs 거래 공간</b> 구분이 핵심. 같은 것 서술 시 오답.</div></div>

<h2 class='sec'>B · 빈칸 해답 (각 4점 · 40점)</h2>
<div class='q'><span class='no'>13</span><div class='ans'><b>1969 / 4 / 1990</b> — 숫자 3개 모두 맞아야 정답.</div></div>
<div class='q'><span class='no'>14</span><div class='ans'><b>정확한 전달 / 주소 할당</b> — 순서 바뀌면 오답.</div></div>
<div class='q'><span class='no'>15</span><div class='ans'><b>HTTP / HTML / URL / 하이퍼</b> — 4요소 중 3개 이상 시 정답.</div></div>
<div class='q'><span class='no'>16</span><div class='ans'><b>2007 / 읽기 / 읽고 쓰기</b> — "참여·공유·개방" 언급 시 가산.</div></div>
<div class='q'><span class='no'>17</span><div class='ans'><b>1:N / 편집권자 / 피드백 제한</b> — "소수→다수 일방" 뉘앙스 필수.</div></div>
<div class='q'><span class='no'>18</span><div class='ans'><b>전화선·모뎀 / 광섬유</b> — 당시/이후 대비가 핵심.</div></div>
<div class='q'><span class='no'>19</span><div class='ans'><b>1990 WWW / 1993 Mosaic / 1994 Netscape / 1996 IE</b> — 연도 3개 이상 시 부분점수.</div></div>
<div class='q'><span class='no'>20</span><div class='ans'><b>분류·목록 / 링크 순위(많이 가리키는 페이지 우선)</b> — Yahoo vs Google 대비 필수.</div></div>
<div class='q'><span class='no'>21</span><div class='ans'><b>쇼핑·커뮤니티·결제 / 활동=데이터</b> — 3요소 중 2개 이상 시 정답.</div></div>
<div class='q'><span class='no'>22</span><div class='ans'><b>시맨틱웹(의미·데이터 연결) / 개인 소유·수익</b> — 혼동 서술 시 감점.</div></div>

<h2 class='sec'>C · 단답 모범답안 (각 8점 · 80점)</h2>
<div class='q'><span class='no'>23</span><div class='ans'>1:N = 소수가 다수에게 일방 전달·통제 / 분산 = 중앙 파괴에도 유지되는 다중 연결. "통제 vs 생존" 대비 필수.</div></div>
<div class='q'><span class='no'>24</span><div class='ans'>분할→번호→분산전송→재조립. "번호 기준 복원" 언급 필수.</div></div>
<div class='q'><span class='no'>25</span><div class='ans'>공공 규약 표준화로 누구나 준수만 하면 참여 가능했기 때문. "소유가 아닌 약속" 언급 필수.</div></div>
<div class='q'><span class='no'>26</span><div class='ans'>하이퍼텍스트 = 링크로 문서 이동 / URL = 주소 입력만으로 접근. "클릭 이동" 언급 필수.</div></div>
<div class='q'><span class='no'>27</span><div class='ans'>이미지를 담은 그래픽 웹으로 대중 유입의 계기 / 디스켓 1장 수준의 가벼운 배포. 둘 중 하나만 쓰면 부분점수.</div></div>
<div class='q'><span class='no'>28</span><div class='ans'>IE의 OS 기본탑재·기업 압박 독점 → 반독점 논란 → Opera·Firefox·Safari·Chrome 재편. "독점→경쟁" 흐름 필수.</div></div>
<div class='q'><span class='no'>29</span><div class='ans'>흩어진 웹의 탐색비용을 낮춰 출발점·습관이 된 통로. "관문=입구+습관" 언급 시 정답.</div></div>
<div class='q'><span class='no'>30</span><div class='ans'>O2O = 온라인 연결이 오프라인 행동으로 이어지는 흐름. 사례: 배달·택시 호출·매장 픽업 중 1개. 정의 없이 사례만 쓰면 부분점수.</div></div>
<div class='q'><span class='no'>31</span><div class='ans'>UGC = 사용자가 직접 만드는 콘텐츠 / 1인 미디어·월드제작 문화의 동력. 사진·영상·숏폼 중 예시 1개 필수.</div></div>
<div class='q'><span class='no'>32</span><div class='ans'>원래 = 시맨틱웹(의미·데이터 연결) / 대중적 = 개인 소유·수익 개념. 혼동 서술 시 감점.</div></div>

<h2 class='sec'>D · 서술 채점 포인트 (각 15점 · 120점)</h2>
<div class='q'><span class='no'>33</span><div class='ans'>분할·번호·분산전송·재조립 4단계 (8점) + 번호 기준 재조립 원리, 메일 본문·첨부 예시 (7점). "순서 달라도 번호로 복원" 명시 필수.</div></div>
<div class='q'><span class='no'>34</span><div class='ans'>1983 표준·역할분담 (5점) + 공공규약·허가없는 혁신 (5점) + 메타버스 상호운용 모태 연결 (5점).</div></div>
<div class='q'><span class='no'>35</span><div class='ans'>버너스리 3요소 (5점) + 최초 브라우저 (3점) + Mosaic·Netscape 그래픽·배포 (4점) + 대중 유입 귀결 (3점).</div></div>
<div class='q'><span class='no'>36</span><div class='ans'>관문=탐색비용↓·집중 (5점) + 쇼핑·결제 통합과 활동=데이터 (5점) + 네이버 멤버십·광고 연결 (5점).</div></div>
<div class='q'><span class='no'>37</span><div class='ans'>2007 상시연결 전제 (3점) + 장소·시간 제약 해소 (4점) + 자투리 접속→총량 증가 (4점) + 앱·결제로 돈 되는 행위 연결 (4점).</div></div>
<div class='q'><span class='no'>38</span><div class='ans'>관계 전이·축적·자산화 (6점) + UGC 주류화·1인 미디어 (4점) + 월드제작 동력 연결 (5점).</div></div>
<div class='q'><span class='no'>39</span><div class='ans'>증명/공간 구분 (5점) + 무한복제·한계비용제로 (5점) + 네트워크 효과·DX와 거래 기반 연결 (5점).</div></div>
<div class='q'><span class='no'>40</span><div class='ans'>연장선 정의 (5점) + 연결·약속·폭발 3단 논거 (6점) + AI를 차세대 흐름으로 위치 (4점). "유행 끝" 단정 시 감점.</div></div>

<h2 class='sec'>E · 도표 채점 포인트 (각 15점 · 60점)</h2>
<div class='q'><span class='no'>41</span><div class='ans'>8단계 순서 (8점) + 단계별 핵심어(분산·번호·주소·URL·그래픽·관문·상시·소유) 각 1점 내외.</div></div>
<div class='q'><span class='no'>42</span><div class='ans'>연도 6개 배치 (9점) + Mosaic = 이미지·그래픽 대중화 계기 (6점). IE 독점 언급 시 가산.</div></div>
<div class='q'><span class='no'>43</span><div class='ans'>분할·번호·다중경로·재조립 4요소 (각 3점) + 번호 복원 화살표 (3점). 한 덩어리 전송 그림은 0점.</div></div>
<div class='q'><span class='no'>44</span><div class='ans'>관문→집중→쇼핑결제→데이터→광고·추천 순환 (10점) + 사람 수=값 명시 (5점).</div></div>

<h2 class='sec'>F · 시나리오 채점 포인트 (각 10점 · 40점)</h2>
<div class='q'><span class='no'>45</span><div class='ans'>메일·카페·멤버십·결제 중 2개 이상 연결 (6점) + 기록→추천·광고 귀결 (4점).</div></div>
<div class='q'><span class='no'>46</span><div class='ans'>온라인/오프라인 구분 표기 (5점) + GPS·QR·별점 중 2개 포함 (5점).</div></div>
<div class='q'><span class='no'>47</span><div class='ans'>구분기준 "누가 만들었나" (4점) + 각 영역 예시 2개씩 (6점).</div></div>
<div class='q'><span class='no'>48</span><div class='ans'>증명/공간 구분 문장 (4점) + 복사돼도 소유는 장부로 판정 (3점) + 5줄 완결 (3점).</div></div>
<div class='footer'><span>인터넷과 메타버스 1주차 해답지 · 총 400점</span><span>Paperlogy</span></div>
"""


def main() -> None:
    jobs = [
        ("인터넷과메타버스_1주차_강의노트+요약.pdf", build_notes()),
        ("인터넷과메타버스_1주차_복습학습지.pdf", build_worksheet()),
        ("인터넷과메타버스_1주차_해답지.pdf", build_answers()),
    ]
    for name, body in jobs:
        pdf = to_pdf(name, body)
        print(f"OK {pdf} {pdf.stat().st_size} bytes")


if __name__ == "__main__":
    main()
