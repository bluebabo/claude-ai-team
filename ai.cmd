@echo off
REM AI team dispatcher (subscription logins only, no API keys).
REM Usage: ai.cmd status | safe | test agy|codex|copilot|ollama | run <seat> <task.md> [attachments...] [--min N] [--model M] [--secret-ok]
REM Python 3.8+: AI_PYTHON if set, else the py launcher, else python on PATH
setlocal
set PYTHONUTF8=1
if defined AI_PYTHON goto custom
where py >nul 2>nul && goto launcher
python "%~dp0ai.py" %*
exit /b
:launcher
py -3 "%~dp0ai.py" %*
exit /b
:custom
"%AI_PYTHON%" "%~dp0ai.py" %*
