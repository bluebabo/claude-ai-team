# Claude AI 팀 — 팀장 Claude 가 차장·사원·인턴 AI 를 부린다

**Claude Code 는 팀장, 이미 로그인해 둔 AI CLI 들은 팀원.** API 키·크레딧·종량 요금 없이.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
![Platform](https://img.shields.io/badge/Windows-10%20%7C%2011-brightgreen.svg)
![Agent Skills](https://img.shields.io/badge/Agent%20Skills-SKILL.md-orange.svg)

Claude 토큰은 판단과 검토에 쓰고, 긴 문서 읽기·사진 판독·번역·초벌 코드·형식 변환은 구독·무료 계정·로컬 모델이 맡는다. Claude 가 일을 가르고(업무분장), 팀원에게 자기완결 지시문을 보내고, 돌아온 결과를 검토해 채택한다.

[English summary below](#english)

---

## 무엇을 하나

| | |
|---|---|
| 🧭 **업무분장이 먼저** | 시작 전에 「무엇을 누가」 표를 보여 주고, 기밀 → 판단 → 이미지·긴 문서 → 코드 → 반복 일 순으로 갈라 맡긴다 |
| 📨 **호출기 하나** | `ai.cmd run <팀원> 지시.md` — 결과 텍스트만 `_work/…/out.md` 로 받는다. 팀원은 읽기 전용이라 파일을 못 고친다 |
| 🔒 **기밀 막기** | 메일 주소와 내 기밀 낱말(`secret_words.txt`)이 든 지시는 외부 팀원에게 나가지 않는다. PC 밖으로 안 나가는 로컬 인턴은 예외 |
| 💸 **요금 방어** | API 키 환경변수를 지우고 부르고, 한도가 차면 그 팀원을 5시간 쉼으로 표시한다 — 크레딧·키로 넘어가지 않는다 |
| 🔁 **위로 넘기기** | 한도 소진·실패면 같은 급 → 상위 팀원 → 팀장 직접 |
| 🚫 **지어내기 금지** | 모든 지시 앞에 「기술 일은 확인된 사실만, 값마다 근거, 못 찾으면 미확인」 머리말이 붙는다. 창작 일만 `[창작]` 으로 허용 |
| 🆕 **모델 별명** | 차장 모델을 `basic`·`light`·`deep` 별명으로 부른다 — 새 버전이 나오면 저절로 따라간다 |

## 조직도

| 직급 | 팀원 | 필요한 계정 | 한도 (2026-11 시험한 계정 기준) | 맡길 일 |
|---|---|---|---|---|
| 팀장 | Claude Code | Claude 구독 | — | 판단·검토·통합, 정격·수치 확정 |
| 차장 | `agy` (Google Antigravity CLI) | Google 계정 (Google AI Pro 로 시험) | 5시간마다 갱신 + 주간 한도, 모델 묶음별 | 긴 문서·여러 파일, 스캔본·사진·PDF 판독, 큰 모듈, UI 시안, 대량 번역, 조사 |
| 사원 | `codex` (OpenAI Codex CLI) | ChatGPT 계정 (무료 계정으로 시험) | 30일 창 하나 | 함수·스크립트·시험 코드, 코드 2차 검토 |
| 사원 | `copilot` (GitHub Copilot CLI) | GitHub 계정 (Copilot Free) | 월 한도 (수치 미공개) | 짧은 코드 조각, codex 대신 |
| 인턴 | `ollama` (로컬 `qwen2.5:7b`) | 없음 | 없음 — 느리고 약하다 | 형식 변환·표 정리·요약·초벌 번역·분류, 기밀 자료 1차 처리 |

## 설치

1. 이 저장소를 Claude Code 스킬 폴더에 받는다 — 한 프로젝트면 `.claude/skills/claude-ai-team/`, 모든 프로젝트면 `~/.claude/skills/claude-ai-team/`
   ```
   git clone https://github.com/bluebabo/claude-ai-team .claude/skills/claude-ai-team
   ```
2. Python 3.8 이상 (`py` 런처나 `python`). 다른 파이썬을 쓰려면 `set AI_PYTHON=C:\경로\python.exe`
3. **쓸 팀원만** 설치하고 로그인한다. 로그인은 사람이 직접 한다

   | 팀원 | 설치 | 로그인 |
   |---|---|---|
   | codex | `npm install -g @openai/codex` | `codex login` → 「Sign in with ChatGPT」 (API 키 로그인 쓰지 않음) |
   | copilot | `npm install -g @github/copilot` | `copilot login` (GitHub 계정). 「Access denied by policy」가 나오면 GitHub 의 Copilot 설정에서 Copilot CLI 가 Enabled 인지 본다 |
   | agy | Google Antigravity CLI 안내대로 (`%LOCALAPPDATA%\agy\bin` 에 설치된 판으로 시험) | Google 계정 (방법은 Antigravity 안내) |
   | ollama | [ollama.com](https://ollama.com) 에서 설치 → `ollama pull qwen2.5:7b` | 필요 없음 (ollama 계정 로그인 안 함) |

4. `ai.cmd safe` — codex 설정에 `forced_login_method = "chatgpt"` 를 넣어 API 키 로그인을 막는다
5. `copy secret_words.example.txt secret_words.txt` → 거래처·인명·코드명을 한 줄에 하나씩
6. `ai.cmd status` → 경고 줄이 없으면 `ai.cmd test ollama` 처럼 한 줄 시험

## 쓰는 법

Claude Code 에게 「팀원 활용해」「이건 차장에게 맡겨」처럼 말하면 [`SKILL.md`](SKILL.md) 대로 업무분장을 보여 주고 나눠 맡긴다. 직접 부를 때:

```
ai.cmd status                                  설치·로그인 방식·쉬는 팀원·기밀 낱말 수·요금 설정 점검
ai.cmd test codex                              한 줄 시험
ai.cmd run agy 지시.md 도면.pdf --min 15        이미지·PDF 는 차장만
ai.cmd run agy 지시.md --model deep             복잡한 일
ai.cmd run codex 지시.md 원본.py                텍스트 첨부는 지시 뒤에 붙여 보낸다
ai.cmd run ollama 지시.md 회의메모.txt           기밀이어도 된다 (로컬)
```

- 결과 = `_work/<시각>_<팀원>/out.md` (14일 뒤 자동 삭제) · 호출 이력 = `_work/log.md`
- 지시문은 자기완결로 쓴다 — 목표·입력·출력 형식(표만·N줄·서론 금지)·수치의 근거 요구
- 한도·쉼 표시·차장 잠금(한 번에 하나)은 이 PC 의 모든 세션이 같이 쓴다

### 차장 모델 별명

| 별명 | 가족·등급 (2026-11) | 쓰는 곳 |
|---|---|---|
| `basic` | Hydrogen Medium | 기본 (안 쓰면 이것) |
| `light` | Hydrogen Low | 단순·대량 (추출·분류·표 정리) |
| `deep` | Argon High | 복잡한 일만 |

- `agy models` 목록에서 `gemini-<버전>-<가족>-<등급>` 중 버전이 가장 높은 것을 고른다. 목록은 하루 한 번 받아 `_work/agy_models.txt` 에 둔다 (받는 데 약 4초)
- 표에 없는 새 가족이 지금 것보다 버전이 높으면 `basic`·`light` 는 그쪽으로 옮기고 `[ai] ★` 줄을 찍는다. `deep` 은 알림만. 가족이 아예 없으면 agy 기본 모델로 돌며 경고한다
- 쓸 수 있는 모델은 계정·시기마다 다르다 — `ai.cmd status` 의 별명 줄로 보고, 다르면 `ai.py` 의 `AGY_ALIAS` 한 줄을 고친다
- 차장 한도는 모델 묶음(Gemini · Claude/GPT · Argon)마다 따로라 호출기도 묶음별로 쉰다
- `codex` 기본 모델은 `gpt-6-luna` — 다른 모델은 `--model` 로

## 요금 방어

| 팀원 | 호출기가 막는 것 | 사람이 계정에서 지킬 것 |
|---|---|---|
| agy | API 키·ADC 환경변수를 지우고 부른다 · `status` 가 「Use AI Credits」 켜짐을 경고 | AI 크레딧을 사지 않는다 · 크레딧 초과 사용 = Never · agy `/config` 에서 Use AI Credits = Off |
| codex | `--sandbox read-only` 로만 부른다 · `OPENAI_API_KEY` 를 지운다 · `safe` 로 ChatGPT 로그인 강제 | OpenAI Platform 에 결제수단을 등록하지 않는다 |
| copilot | 로그인만 쓰고 `--allow-all-tools` 는 쓰지 않는다 | 업그레이드·결제수단 등록 안 함 |
| ollama | 모델 이름에 `cloud` 가 들어가면 막는다 | ollama 계정 로그인 안 함 |
| 공통 | API 키 환경변수 8종을 지우고 호출 · 429·quota 응답이면 그 팀원(묶음)을 5시간 쉼으로 표시 · 재시도 루프 없음 | — |

## 남은 한도 보기 (모델 호출 없이)

- 차장: `agy -p "/usage"` — 묶음별 주간·5시간 남은 % 와 초기화 시각 (UTC)
- codex: `python codex_limits.py` — app-server 의 `account/rateLimits/read` (남은 % 와 초기화 시각)
- copilot: CLI 로는 못 본다 → GitHub 의 Copilot 설정 화면
- 인턴: 한도 없음

## 시험한 판 (2026-11, Windows 11)

| 팀원 | 판 | 한 줄 시험 |
|---|---|---|
| agy | 1.5.4 | OK — 48초 (기본 모델) |
| codex | 0.167.0 | OK — 15초 (`gpt-6-luna`) |
| copilot | 1.0.108 | OK — 16초 |
| ollama | `qwen2.5:7b` | OK — 첫 호출 101초 (모델 올림), 이후 3초 |

## 알려진 문제

- 차장이 「SUCCESS」를 내고 `out.md` 가 0바이트인 경우가 있었다 — 사진 여러 장 판독, 첨부 없는 웹 조사에서 두 번씩 (원인 미확인). 결과가 비면 성공으로 치지 않는다
- 인턴은 30분 안 쓰면 모델이 내려가 첫 호출이 40~100초 걸린다
- ollama 가 모델을 새로 올리는 중 가끔 500 을 낸다 — 호출기가 한 번 다시 부른다
- codex 설정 파일에 적힌 일부 모델은 ChatGPT 무료 로그인에서 오류가 난다 — 그래서 기본을 `gpt-6-luna` 로 정했다
- agy 는 승인 안 된 파일 쓰기를 조용히 거절하고 정상 종료한다 → 팀원은 읽기 전용으로만 쓰고 자동 승인 옵션은 쓰지 않는다
- 같은 Google 계정의 Antigravity 앱 사용분도 차장 한도에서 같이 빠지는 것으로 보인다 (추정)
- 클라우드에서 도는 Claude 세션은 이 PC 의 팀원에 닿지 못한다

## 폴더

```
SKILL.md                  AI 에이전트(Claude)가 따르는 규칙
ai.cmd · ai.py            호출기
codex_limits.py           codex 남은 한도 조회
secret_words.example.txt  기밀 낱말 견본 → secret_words.txt 로 복사 (깃에 안 올라감)
_work/                    결과·로그·한도 상태 (자동 생성, 깃에 안 올라감)
```

## 라이선스

MIT. 각 CLI 와 모델은 그 제공사의 약관을 따른다. 이 도구는 사용자가 로그인한 CLI 를 그대로 부를 뿐, 한도를 늘리거나 우회하지 않는다.

---

## English

**Claude Code as lead; your already-logged-in AI CLIs as teammates.** No API keys, credits, or pay-per-use fees. Claude tokens go to judgment and review, while subscription, free-tier, and local models handle long-document reading, image/PDF reading, translation, draft code, and formatting. Claude splits the work (delegation first), sends self-contained prompts, and reviews the returned results.

### What it does

| | |
|---|---|
| **Delegation first** | Shows a "who does what" table before starting; assigns in order: confidential → judgment → images/long docs → code → repetitive tasks |
| **One dispatcher** | `ai.cmd run <member> task.md` — returns text only to `_work/…/out.md`. Members are read-only and cannot edit files |
| **Secret guard** | Prompts containing email addresses or words in `secret_words.txt` are blocked from external members (local intern is exempt) |
| **Cost guard** | Strips API-key environment variables before calling and marks a member as resting for 5 hours on quota exhaustion — never falls back to credits or keys |
| **Escalation** | On quota exhaustion or failure: same role → higher role → lead directly |
| **No fabrication** | Prepends a rule to every prompt: technical work must state only verified facts with sources, or "unconfirmed"; only a task whose first line is `[창작]` ("creative") may invent freely |
| **Model aliases** | Picks the senior's model by `basic`, `light`, and `deep` aliases — automatically follows newer versions |

### Team

| Role | Member | Account needed | Limits (tested 2026-11) | Good for |
|---|---|---|---|---|
| lead | Claude Code | Claude subscription | — | Judgment, review, integration, confirming part ratings and figures |
| senior | `agy` (Google Antigravity CLI) | Google account (tested with Google AI Pro) | 5-hour refresh + weekly limit per model group | Long docs/multi-file, scans/photos/PDF reading, large modules, UI drafts, bulk translation, research |
| staff | `codex` (OpenAI Codex CLI) | ChatGPT account (tested on Free) | Single 30-day window | Functions, scripts, test code, second-pass code review |
| staff | `copilot` (GitHub Copilot CLI) | GitHub account (Copilot Free) | Monthly limit (undisclosed) | Short code snippets, codex fallback |
| intern | `ollama` (local `qwen2.5:7b`) | None | None — slow and weak | Formatting, tables, summaries, draft translation, classification, initial handling of confidential data |

### Install

1. Clone this repository into Claude Code's skills folder (`.claude/skills/claude-ai-team/` for one project, or `~/.claude/skills/claude-ai-team/` for all):
   ```
   git clone https://github.com/bluebabo/claude-ai-team .claude/skills/claude-ai-team
   ```
2. Python 3.8+ (`py` launcher or `python`). To use another Python: `set AI_PYTHON=C:\path\to\python.exe`
3. Install and log in **only** to the members you plan to use (manual login):

   | Member | Install | Login |
   |---|---|---|
   | codex | `npm install -g @openai/codex` | `codex login` → "Sign in with ChatGPT" (do not use API key login) |
   | copilot | `npm install -g @github/copilot` | `copilot login` (GitHub account). On "Access denied by policy", check that Copilot CLI is Enabled in GitHub Copilot settings |
   | agy | Follow Google Antigravity CLI instructions (tested with `%LOCALAPPDATA%\agy\bin`) | Google account (see Antigravity instructions) |
   | ollama | Install from [ollama.com](https://ollama.com) → `ollama pull qwen2.5:7b` | None (do not log in to an ollama account) |

4. `ai.cmd safe` — sets `forced_login_method = "chatgpt"` in codex config to block API key login
5. `copy secret_words.example.txt secret_words.txt` — add client names, people, or code names one per line
6. `ai.cmd status` — if no warnings appear, run a one-line test such as `ai.cmd test ollama`

### Usage

```
ai.cmd status                                  Check installs, login method, resting members, secret words, cost settings
ai.cmd test codex                              One-line test
ai.cmd run agy task.md drawing.pdf --min 15    Images/PDFs: senior only
ai.cmd run agy task.md --model deep            Complex tasks
ai.cmd run codex task.md source.py             Text attachments are appended after the prompt
ai.cmd run ollama task.md notes.txt            Safe for confidential data (local)
```

### Cost guards

| Member | Enforced by runner | User must keep in account |
|---|---|---|
| agy | Strips API-key/ADC env vars; `status` warns if "Use AI Credits" is on | Do not buy AI credits; Credit overage = Never; set Use AI Credits = Off in agy `/config` |
| codex | Runs with `--sandbox read-only`; strips `OPENAI_API_KEY`; `safe` forces ChatGPT login | Do not add a payment method on OpenAI Platform |
| copilot | Uses login only; never passes `--allow-all-tools` | Do not upgrade or add a payment method |
| ollama | Blocks model names containing `cloud` | Do not log in to an ollama account |
| Common | Strips 8 API-key env vars; marks member/group as resting 5 hours on 429/quota; no retry loop | — |

### Known issues

- senior (`agy`) occasionally returned `SUCCESS` with a 0-byte `out.md` (observed twice on multi-image reading and web research without attachments; cause unconfirmed). Empty outputs are not treated as success.
- intern (`ollama`) unloads the model after 30 minutes of inactivity, making the first call take 40–100s.
- ollama sometimes returns 500 while loading a model; the runner retries once.
- Some models in codex config fail on ChatGPT Free login, so `gpt-6-luna` is set as default.
- agy silently declines unapproved file writes and exits normally; keep members read-only without auto-approve options.
- Antigravity app usage on the same Google account appears to share the senior quota (inferred).
- Cloud-hosted Claude sessions cannot reach members on this PC.
