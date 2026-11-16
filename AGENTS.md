# AGENTS.md

This repository is an **Agent Skill** (`SKILL.md`) for Claude Code on Windows. Claude stays the lead and delegates routine work to AI CLIs the user logs in to (`agy`, `codex`, `copilot`) and a local Ollama model, through one dispatcher (`ai.cmd`). No API keys, paid credits or pay-per-use billing.

- **Do not install it silently.** Tell the user what it does and let them decide whether to use it and which members to turn on. The suggested message and the "what each member needs" table are in [README.md](README.md), section *For AI agents*.
- Install only what the user approves. Logins (`codex login`, `copilot login`, Google sign-in for agy) are done by the user.
- Ask whether the team should work on every task or only when asked. For every task, add the one-line rule from README (*For AI agents*, step 8) to the `CLAUDE.md` the user chooses — show the line and the file first.
- Never buy plans or credits, add payment methods, set API-key environment variables, or use auto-approve options.
- After setup, follow [`SKILL.md`](SKILL.md): show the user who does what before each job, send self-contained tasks with `ai.cmd run`, and review every result before using it.

## 한국어

- **말없이 설치하지 않는다.** 무엇을 하는 스킬인지 알리고, 쓸지와 어느 팀원을 켤지는 사용자가 정한다. 안내 문구와 「팀원마다 필요한 것」 표는 [README.md](README.md) 의 *For AI agents · AI 에이전트라면* 절에 있다
- 사용자가 허락한 것만 설치한다. 로그인(`codex login`, `copilot login`, agy 의 Google 로그인)은 사용자가 직접 한다
- 모든 일에 늘 쓸지, 부를 때만 쓸지 묻는다. 늘 쓰려면 README(*For AI agents* 8단계)의 한 줄을 사용자가 고른 `CLAUDE.md` 에 넣는다 — 넣기 전에 그 줄과 파일을 보여 준다
- 요금제·크레딧 구매, 결제수단 등록, API 키 환경변수 설정, 자동 승인 옵션은 쓰지 않는다
- 설치 뒤에는 [`SKILL.md`](SKILL.md) 대로 — 일마다 「무엇을 누가」를 먼저 보여 주고, `ai.cmd run` 으로 자기완결 지시를 보내고, 결과는 검토한 뒤에 쓴다
