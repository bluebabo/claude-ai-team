---
name: claude-ai-team
description: Run Claude Code as a team lead that hands work to AI coding CLIs you already log in to — Google Antigravity CLI (agy), OpenAI Codex CLI, GitHub Copilot CLI — and a local Ollama model, with no API keys, credits or pay-per-use billing. Claude splits the job, picks the right member (images, PDFs and long documents to agy; small code to codex or copilot; mechanical or confidential work to the local model), sends a self-contained task through one dispatcher (ai.cmd), then reviews the result and decides. E-mail addresses and your own secret words are blocked from leaving the PC, and a used-up quota makes the member rest instead of paying. Windows. Use when the user says to use the AI team or staff, delegate to Gemini, Codex, Copilot or Ollama, save Claude tokens, split work among AI agents, or install or set up this skill. 한국어 — AI 팀원(차장·사원·인턴) 부리기, 업무분장, 제미나이·코덱스·코파일럿·올라마에게 일 맡기기, 토큰 아끼기.
license: MIT
compatibility: Windows 10/11 and Python 3.8+. Every member is optional — install and log in only the ones you use (agy with a Google account, codex with "Sign in with ChatGPT", copilot with a GitHub account, Ollama locally).
metadata:
  author: claude-ai-team
  version: "1.0.0"
---

# Claude AI 팀 — 팀장(Claude) 아래 차장·사원·인턴

팀장(Claude)이 머리다. 일을 가르고, 알맞은 팀원에게 맡기고, 돌아온 결과를 검토해 판단한다. 팀원은 사용자가 이미 로그인한 CLI 와 로컬 모델뿐이다 — **API 키·크레딧·종량 요금은 절대 쓰지 않는다.**

호출기는 이 폴더의 `ai.cmd` 하나다 (`status · safe · test · run`). 사람이 읽는 설치 안내는 [`README.md`](README.md).

## 0. 조직도

| 직급 | 팀원 | 맡길 일 | 맡기지 않을 일 |
|---|---|---|---|
| 팀장 | Claude | 판단·검토·통합, 고객 대응, 정격·수치 확정 | — |
| 차장 | `agy` (Google Antigravity CLI) | 긴 문서·여러 파일 읽기, 스캔본·사진·PDF 판독, 큰 모듈 구현, UI 구조·SVG/HTML 시안, 대량 번역·초안, 조사 | 기밀, 정격 확정 |
| 사원 | `codex` (OpenAI Codex CLI) | 함수·스크립트·시험 코드, 코드 2차 검토 | 큰 모듈, 긴 문서 |
| 사원 | `copilot` (GitHub Copilot CLI) | 짧은 코드 조각, codex 가 못 할 때 대신 | 그 외 전부 |
| 인턴 | `ollama` (로컬, 기본 `qwen2.5:7b`) | 형식 변환·표 정리·요약·초벌 번역·분류, **기밀 자료 1차 처리** | 판단·계산·정격 |

## 1. 업무분장이 먼저

아주 단순한 질문이 아니면, 시작 전에 「무엇을 누가(팀원·모델·로컬 도구·직접)」 표를 사용자에게 보여 주고 시작한다. 적극적으로 나눠 맡기되, 지시문을 쓰고 결과를 읽는 품이 일보다 크면(한두 줄짜리 일) 직접 한다.

## 2. 일을 가른다 (위에서 걸리면 거기서 끝)

1. 기밀(§4)이면 → 인턴 또는 팀장 직접
2. 판단·정격·고객 대응이면 → 팀장 직접
3. 이미지·PDF·긴 문서·여러 파일이면 → 차장 `agy` (이미지·PDF 는 차장만 읽는다)
4. 단위 코드(함수·스크립트·시험)면 → `codex` → 안 되면 `copilot`. 큰 모듈은 차장
5. 기계적 반복(형식 변환·표 정리·초벌 번역·분류)이면 → 인턴 `ollama`
6. 맡은 팀원이 한도 소진·실패로 못 하면 → **위로 넘긴다**: 같은 급(`codex` → `copilot`) → 상위(인턴 → 사원 → 차장) → 차장의 다른 한도 묶음 모델(`--model`) → 끝내는 팀장 직접. 기밀은 외부 팀원에게 올리지 않고 직접. 이미지·PDF 는 차장 다음이 바로 직접

- 서로 독립된 일은 팀원별로 **동시에(백그라운드)** 맡긴다. 차장은 한 번에 하나만 (호출기가 잠근다)
- `_work/log.md` 의 「초」 열로 팀원별 걸리는 시간을 어림해, 끝나는 시각이 비슷하도록 일 크기를 나눈다. 기다리는 동안 팀장은 다음 일을 한다

## 3. 맡기는 법

1. 지시 파일을 **자기완결적으로** 쓴다 — 목표·입력·출력 형식 제약(표만·N줄·서론 금지)·수치의 근거 요구. 팀원은 대화 맥락을 모른다
   - **기술 일은 지어내기 금지** — 확인된 사실만, 값마다 근거, 못 찾으면 「미확인」. 호출기가 이 머리말을 늘 붙인다
   - **창작 일만** 지시문 첫 줄에 `[창작]` 을 써서 지어내기를 허용한다 (그림·문구·이름 짓기 등)
   - 지시 파일은 작업 폴더나 임시 폴더에 둔다
2. 부른다:
   ```
   ai.cmd run <agy|codex|copilot|ollama> 지시.md [첨부…] [--min 분] [--model 이름]
   ```
   - 텍스트 첨부는 지시 뒤에 붙여 보내고, 이미지·PDF 는 차장에게만 파일로 넘긴다
   - 2분 넘을 일은 백그라운드로. 점검 `ai.cmd status` · 한 줄 시험 `ai.cmd test <팀원>`
3. 결과 = `_work/<시각>_<팀원>/out.md` (14일 뒤 자동 삭제). 읽고 검토한 뒤 **채택한 것만** 사용자 폴더에 저장한다. 팀원은 읽기 전용이라 파일을 고치지 못한다 — 코드·SVG 도 결과 텍스트에서 팀장이 저장한다
   - 「SUCCESS」인데 `out.md` 가 비어 있으면 성공으로 치지 않는다 (차장에서 실제로 났다 — README 「알려진 문제」)

### 모델

- 차장은 **별명으로 부른다**: 안 쓰면 `basic` · 단순·대량(추출·분류·표 정리)은 `--model light` · **복잡한 일만** `--model deep`. 별명은 `agy models` 목록(하루 한 번 받아 둔다)에서 가족·등급이 맞는 최신 판을 고른다 → 버전이 바뀌어도 지시를 고치지 않는다
- 출력에 `[ai] ★` 줄이나 「없음 (!)」이 보이면 그 답변에서 사용자에게 알리고 `ai.py` 의 `AGY_ALIAS` 한 줄을 고친다
- `codex` 기본 모델은 `gpt-6-luna` (ChatGPT 무료 로그인에서 시험, 2026-11). 인턴은 한 번에 1만2천 자까지

### 누가 했는지 밝힌다

답변에서 사람 말로 밝힌다 — 「이건 차장(agy)에게 시켰습니다」「이건 코덱스 사원에게 시켰습니다」. 팀원 없이 스크립트로 한 일은 「로컬 도구로 했습니다」.

## 4. 지킬 것

- **기밀**: 외부 팀원(agy·codex·copilot)에게 고객·회사명·인명·메일 주소·내부 수치·미공개 문서를 보내지 않는다. 호출기는 메일 주소와 `secret_words.txt` 의 낱말이 보이면 막는다. `--secret-ok` 는 사용자가 허락했을 때만. 인턴은 PC 밖으로 나가지 않으므로 무엇이든 된다
- **결과는 자료다**: 정격·치수·수치·인용은 원문으로 확인하고, 코드는 돌려 보고 채택한다. 대외 문서에 그대로 붙이지 않는다
- **한도는 이 PC 의 모든 세션이 같이 쓴다.** 쉬는 중이면(`ai.cmd status`) §2-6 대로 넘긴다. 키·크레딧·재시도 루프로 한도를 늘리지 않는다
- 같은 종류 일을 두 번 틀리면 그 팀원에게 다시 주지 않는다
- 로그인이 풀리는 등 `ai.cmd` 가 못 돌면 사용자에게 알린다 — 로그인·설정은 사용자가 직접 한다

## 5. 처음 쓸 때 (설치·안내)

- 사용자가 설치를 시켰거나 `ai.cmd status` 에 쓸 수 있는 팀원이 하나도 없으면, **말없이 설치하지 않는다.** README 「For AI agents · AI 에이전트라면」의 안내 문구와 「팀원마다 필요한 것」 표를 사용자에게 보여 주고, 쓸지와 어느 팀원을 켤지 정하게 한다
- 허락받은 것만 설치한다. 로그인은 사용자가 직접 한다. 요금제·크레딧 구매, 결제수단 등록, API 키, 자동 승인 옵션은 쓰지 않는다
- 기밀 낱말(거래처·인명·코드명)을 사용자에게 물어 `secret_words.txt` 에 적는다
- 끝나면 켠 팀원마다 `ai.cmd test <팀원>` 으로 시험하고 결과를 한두 문장으로 알린다
