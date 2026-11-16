# -*- coding: utf-8 -*-
"""AI 팀원 호출기 — 구독 로그인 CLI 에 지시문을 넘기고 결과 텍스트만 받는다 (파일은 못 고치게 읽기 전용으로 부름).
사용: ai.cmd status | safe | test <팀원> | run <팀원> <지시파일> [첨부…] [--min N] [--model M] [--secret-ok]
차장 --model 은 별명 basic(기본) · light(단순) · deep(복잡) — 모델 ID 를 직접 줘도 된다
팀원: agy(차장) · codex · copilot(사원) · ollama(인턴, 로컬)
요금 방어: API 키 환경변수를 지우고 부르고, 한도가 차면 크레딧·키로 넘어가지 않고 쉰다. 자세한 것 = README.md
"""
import sys, os, re, json, time, shutil, subprocess, urllib.request, pathlib

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')
HOME = pathlib.Path.home()
HERE = pathlib.Path(__file__).resolve().parent
WORK = HERE / '_work'
STATE, LOG, LOCK = WORK / 'state.json', WORK / 'log.md', WORK / 'agy.lock'
SECRETS = HERE / 'secret_words.txt'  # 외부 팀원에게 보내면 안 되는 낱말 (한 줄에 하나 · 깃에 올리지 않는다)
SEATS = {'agy': '차장', 'codex': '사원', 'copilot': '사원', 'ollama': '인턴'}
AGY_SET = HOME / '.gemini' / 'antigravity-cli' / 'settings.json'
CODEX_CFG, CODEX_AUTH = HOME / '.codex' / 'config.toml', HOME / '.codex' / 'auth.json'
EXTRA = [os.path.expandvars(p) for p in (r'%APPDATA%\npm', r'%ProgramFiles%\nodejs', r'%LOCALAPPDATA%\agy\bin', r'%LOCALAPPDATA%\Programs\Ollama')]
KEYS = ('GEMINI_API_KEY', 'GOOGLE_API_KEY', 'GOOGLE_APPLICATION_CREDENTIALS', 'AGY_ADC_AUTH', 'GOOGLE_GEMINI_BASE_URL',
        'OPENAI_API_KEY', 'CODEX_API_KEY', 'OPENAI_BASE_URL')
WORDS = [w.strip() for w in SECRETS.read_text('utf-8').splitlines() if w.strip() and not w.lstrip().startswith('#')] if SECRETS.exists() else []
SECRET = re.compile('|'.join([r'[\w.+-]+@[\w-]+\.[\w.]+'] + [re.escape(w) for w in WORDS]))
LIMIT = re.compile(r'quota|rate.?limit|429|exhaust|usage limit|credits?\b|too many requests', re.I)
# 기술 일은 지어내기 금지, 창작 일만 허용
PREFACE = ('너는 팀장(Claude)의 조수다. 지시에 정한 형식으로만 답하고 서론·맺음말을 쓰지 않는다. 파일을 고치지 말고 결과를 텍스트로만 답한다.\n'
           '기술 업무(부품·정격·치수·수치·규격·코드·API·특허·문헌·인용·판독)는 지어내지 않는다. 받은 자료나 확인한 출처에 있는 사실만 쓰고 값마다 근거(파일·쪽·줄·URL)를 단다. '
           '못 찾거나 못 읽으면 「미확인」, 흐린 글자는 「판독 불가」라고 쓰고 추측으로 채우지 않는다.\n'
           '지시문 첫 줄에 [창작] 이 있을 때만(그림·문구·삽화·이름 짓기 등) 자유롭게 지어낸다.\n\n')
READ = 'Read prompt.md in the current directory and carry out its instructions. Reply with the result text only. Do not modify any files.'


def find(exe):
    p = shutil.which(exe, path=os.pathsep.join(EXTRA + [os.environ.get('PATH', '')]))
    return None if p and 'copilot-shim' in p else p  # VS Code 안의 shim 은 CLI 가 아니다


# 차장 모델 별명 (2026-11 기준: 기본 Hydrogen, 복잡한 일만 Argon). 버전이 바뀌어도 가족·등급으로 최신 판을 찾는다
AGY_ALIAS = {'basic': ('hydrogen', 'medium'), 'light': ('hydrogen', 'low'), 'deep': ('argon', 'high')}
# 옛 가족이 목록에 남은 채 새 가족이 나오면 옛것을 계속 써서 성능만 잃는다 → 더 새 버전 가족으로 옮겨 탄다. deep 은 알림만
AGY_FOLLOW = ('basic', 'light')


def agy_model(name):
    name = name or 'basic'
    if name not in AGY_ALIAS:
        return name
    family, grade = AGY_ALIAS[name]
    cache = WORK / 'agy_models.txt'  # 목록은 하루 한 번만 받는다 — 부를 때마다 약 4초
    if cache.exists() and time.strftime('%Y%m%d', time.localtime(cache.stat().st_mtime)) == time.strftime('%Y%m%d'):
        out = cache.read_text('utf-8')
    else:
        try:
            env = {k: v for k, v in os.environ.items() if k not in KEYS}
            env['PATH'] = os.pathsep.join(EXTRA + [env.get('PATH', '')])
            out = subprocess.run([find('agy') or 'agy', 'models'], capture_output=True, text=True, encoding='utf-8', errors='replace',
                                 env=env, timeout=60, check=True).stdout
            WORK.mkdir(exist_ok=True)
            cache.write_text(out, 'utf-8')
        except (OSError, subprocess.TimeoutExpired, subprocess.CalledProcessError):
            out = ''
    ver = {}  # 가족 → (버전 튜플, 모델 ID) 중 최신
    for line in out.splitlines():
        if m := re.fullmatch(rf'gemini-([\d.]+)-([a-z]+)-{re.escape(grade)}', line.split('\t', 1)[0]):
            ver[m[2]] = max(ver.get(m[2], ((), '')), (tuple(map(int, m[1].split('.'))), m[0]))
    mine = ver.get(family, ((), ''))[0]
    new = [f for f in ver if f not in {a[0] for a in AGY_ALIAS.values()} and ver[f][0] >= mine]
    if new:
        f = max(new, key=lambda f: ver[f][0])
        if name in AGY_FOLLOW and ver[f][0] > mine:
            print(f'[ai] ★ 차장 새 모델 가족 {f}({ver[f][1]}) 가 {family} 보다 새것 — {name} 을 {f} 로 돌렸다. 사용자에게 알리고 ai.py AGY_ALIAS 를 고칠 것')
            family = f
        else:
            print(f'[ai] ★ 차장 새 모델 가족 {", ".join(new)} 등장 — {name} 은 {family} 그대로. 사용자에게 알릴 것')
    if family in ver:
        return ver[family][1]
    print(f"[ai] 차장 모델 별명 '{name}'({family}-{grade}) 이 agy models 에 없음 — agy 기본 모델로 돈다. ai.py AGY_ALIAS 를 고칠 것")
    return None


def jload(p):
    return json.loads(p.read_text('utf-8')) if p.exists() else {}


def cooldown(seat):
    left = jload(STATE).get(seat, 0) - time.time()
    return left if left > 0 else 0


def set_cooldown(seat, hours=5):
    WORK.mkdir(exist_ok=True)
    s = jload(STATE)
    s[seat] = time.time() + hours * 3600
    STATE.write_text(json.dumps(s), 'utf-8')


def status():
    for k in KEYS:
        if os.environ.get(k):
            print(f'! 환경변수 {k} 가 설정돼 있음 — ai.cmd 는 지우고 부르지만 다른 도구가 쓰면 요금이 난다')
    for seat, rank in SEATS.items():
        exe = find(seat)
        print(f'{rank} {seat:8}: ' + (exe or '미설치'))
    for k, t in jload(STATE).items():
        if t > time.time():
            print(f'  쉬는 중: {k} — {(t - time.time()) / 3600:.1f}시간 (한도 소진 추정)')
    print(f'  기밀 낱말: {len(WORDS)}개 ({SECRETS.name})' + ('' if WORDS else ' — 없음. secret_words.example.txt 를 secret_words.txt 로 복사해 채운다'))
    if find('agy'):
        v = jload(AGY_SET).get('useG1Credits')
        print(f'  agy useG1Credits = {v} (키가 없으면 기본값 꺼짐 — agy 가 실행할 때마다 설정 파일을 다시 써서 기본값은 적지 않는다)' + ('  ← 켜져 있다! agy 에서 /config → Use AI Credits Off' if v else ''))
        for n in AGY_ALIAS:
            print(f"  agy 별명 {n} → {agy_model(n) or '없음 (!)'}")
    if CODEX_AUTH.exists():
        a = jload(CODEX_AUTH)
        print('  codex 로그인 방식: ' + ('API 키 (!) — 로그아웃 후 ChatGPT 로 다시' if a.get('OPENAI_API_KEY') else 'ChatGPT 계정'))
    try:
        m = json.load(urllib.request.urlopen('http://localhost:11434/api/tags', timeout=3))['models']
        print('  ollama 모델: ' + ', '.join(x['name'] for x in m))
    except OSError:
        print('  ollama 서버 응답 없음 — 트레이 앱을 켠다')


def safe():
    CODEX_CFG.parent.mkdir(parents=True, exist_ok=True)
    t = CODEX_CFG.read_text('utf-8') if CODEX_CFG.exists() else ''
    if 'forced_login_method' in t:
        print('codex: forced_login_method 이미 있음 — 값 확인:', re.findall(r'forced_login_method.*', t))
    else:
        if t:
            shutil.copy2(CODEX_CFG, CODEX_CFG.with_suffix('.toml.bak'))
        CODEX_CFG.write_text('forced_login_method = "chatgpt"\n' + t, 'utf-8')
        print(f'codex: forced_login_method="chatgpt" 기록 ({CODEX_CFG})')


def attach(task, files, seat, d):
    for f in files:
        p = pathlib.Path(f)
        if p.suffix.lower() in ('.pdf', '.png', '.jpg', '.jpeg', '.webp', '.gif'):
            if seat != 'agy':
                sys.exit(f'{p.name}: 이미지·PDF 는 차장(agy)만 읽는다')
            shutil.copy2(p, d / p.name)
            task += f'\n\n=== 첨부: {p.name} (현재 폴더의 파일을 직접 열어 읽어라) ==='
        else:
            task += f'\n\n=== 첨부: {p.name} ===\n' + p.read_text('utf-8', 'replace')
    return task


def ollama(task, model, secs):
    model = model or 'qwen2.5:7b'
    if 'cloud' in model:
        return 'ERROR', '', 'ollama 클라우드 모델은 종량 요금 위험으로 금지'
    body = json.dumps({'model': model, 'messages': [{'role': 'user', 'content': task}], 'stream': False,
                       'keep_alive': '30m', 'options': {'num_ctx': 16384}}).encode()
    req = urllib.request.Request('http://localhost:11434/api/chat', body, {'Content-Type': 'application/json'})
    for tried in range(2):  # 모델을 새로 올리는 중 간헐적으로 500 이 났다 (원인 미확인)
        try:
            return 'SUCCESS', json.load(urllib.request.urlopen(req, timeout=secs))['message']['content'], ''
        except urllib.error.HTTPError as e:
            if e.code != 500 or tried:
                raise


def cli(seat, d, task, minutes, model):
    exe = find(seat)
    if not exe:
        return 'ERROR', '', f'{seat} 미설치'
    m = lambda flag: [flag, model] if model else []
    if seat == 'agy':
        cmd, inp = [exe, '-p', READ, '--output-format', 'json', '--print-timeout', f'{minutes}m'] + m('--model'), None
    elif seat == 'codex':
        cmd, inp = [exe, 'exec', '--sandbox', 'read-only', '--skip-git-repo-check', '--ephemeral', '-o', str(d / 'out.md')] + m('-m') + ['-'], task
    else:
        cmd, inp = [exe, '-s', '--no-ask-user'] + m('--model'), task
    kw = {'input': inp.encode('utf-8')} if inp else {'stdin': subprocess.DEVNULL}
    env = {k: v for k, v in os.environ.items() if k not in KEYS}
    env['PATH'] = os.pathsep.join(EXTRA + [env.get('PATH', '')])  # npm 도구는 node 를 PATH 에서 찾는다
    p = subprocess.run(cmd, capture_output=True, cwd=d, env=env, timeout=minutes * 60 + 30, **kw)
    out, err = p.stdout.decode('utf-8', 'replace'), p.stderr.decode('utf-8', 'replace')
    if seat == 'agy':
        try:
            j = json.loads(out)
            text = next((j[k] for k in ('response', 'result', 'text', 'output', 'message') if isinstance(j.get(k), str)), out)
            return j.get('status', 'ERROR'), text, err
        except ValueError:
            return ('SUCCESS' if p.returncode == 0 and out.strip() else 'ERROR'), out, err
    if seat == 'codex' and (d / 'out.md').exists():
        out = (d / 'out.md').read_text('utf-8')
    return ('SUCCESS' if p.returncode == 0 and out.strip() else 'ERROR'), out, err


def run(seat, task_file, files, minutes=10, model=None, secret_ok=False):
    if seat not in SEATS:
        sys.exit(f'팀원은 {"/".join(SEATS)} 중 하나')
    key = seat
    if seat == 'agy':  # /usage 의 한도 묶음: Gemini · Claude+GPT · Argon — 묶음끼리 따로 잠긴다
        model = agy_model(model)
        g = 'argon' if 'argon' in (model or '') else (model or 'gemini').split('-')[0]
        key = 'agy:' + {'gpt': 'claude'}.get(g, g)
    elif seat == 'codex':  # ChatGPT 무료 로그인에서 되는 모델 (2026-11 시험)
        model = model or 'gpt-6-luna'
    if cooldown(key):
        sys.exit(f'{key}: 한도 소진 추정으로 {cooldown(key)/3600:.1f}시간 쉼 — 다른 팀원이나 팀장 직접. 크레딧·API 로 넘기지 않는다')
    WORK.mkdir(exist_ok=True)
    for old in WORK.iterdir():
        if old.is_dir() and re.match(r'\d{8}_\d{6}_', old.name) and time.time() - old.stat().st_mtime > 14 * 86400:
            shutil.rmtree(old)
    d = WORK / f"{time.strftime('%Y%m%d_%H%M%S')}_{seat}"
    d.mkdir()
    task = attach(PREFACE + pathlib.Path(task_file).read_text('utf-8'), files, seat, d)
    hit = SECRET.search(task)
    if hit and seat != 'ollama' and not secret_ok:
        sys.exit(f'기밀 낱말 「{hit.group()}」 — 외부 팀원에게 보내지 않는다. 지우거나 ollama 로, 사용자가 허락했으면 --secret-ok')
    if len(task) > 12000 and seat == 'ollama':
        sys.exit('인턴은 1만2천 자까지 — 쪼개서 맡긴다')
    (d / 'prompt.md').write_text(task, 'utf-8')
    if seat == 'agy':
        if LOCK.exists() and time.time() - LOCK.stat().st_mtime < 1800:
            sys.exit('차장이 다른 일을 하는 중 — 끝난 뒤 다시 (차장은 한 번에 하나)')
        LOCK.write_text('1')
    t0 = time.time()
    try:
        status_, text, err = ollama(task, model, minutes * 60) if seat == 'ollama' else cli(seat, d, task, minutes, model)
    except (OSError, subprocess.TimeoutExpired) as e:
        status_, text, err = 'ERROR', '', f'{type(e).__name__}: {e} ' + (e.read().decode('utf-8', 'replace')[:400] if hasattr(e, 'read') else '')
    finally:
        LOCK.unlink(missing_ok=True)
    secs = int(time.time() - t0)
    ok = status_ == 'SUCCESS'
    if not ok and LIMIT.search(err + text):
        set_cooldown(key)
        status_ = 'LIMIT'
    (d / 'out.md').write_text(text, 'utf-8')
    if not LOG.exists():
        LOG.write_text('# AI 팀원 호출 로그\n\n| 시각 | 팀원 | 지시 | 초 | 결과 | 작업폴더 |\n|---|---|---|---|---|---|\n', 'utf-8')
    with LOG.open('a', encoding='utf-8') as f:
        f.write(f"| {time.strftime('%m-%d %H:%M')} | {seat} | {pathlib.Path(task_file).name} | {secs} | {status_} | {d.name} |\n")
    print(f'[ai] {SEATS[seat]}({seat}) {status_} {secs}초 → {d / "out.md"}\n')
    print(text if ok else '\n'.join(err.strip().splitlines()[-15:]))
    sys.exit(0 if ok else 1)


def main(a):
    flags = {'--min': 10, '--model': None}
    pos, secret_ok, i = [], False, 0
    while i < len(a):
        if a[i] in flags:
            flags[a[i]] = int(a[i + 1]) if a[i] == '--min' else a[i + 1]
            i += 2
        elif a[i] == '--secret-ok':
            secret_ok, i = True, i + 1
        else:
            pos.append(a[i])
            i += 1
    cmd = pos[0] if pos else ''
    if cmd == 'status':
        status()
    elif cmd == 'safe':
        safe()
    elif cmd == 'test' and len(pos) >= 2:
        WORK.mkdir(exist_ok=True)
        t = WORK / 'test_prompt.md'
        t.write_text('OK 라고만 답하라.', 'utf-8')
        run(pos[1], t, [], 3, flags['--model'])
    elif cmd == 'run' and len(pos) >= 3:
        run(pos[1], pos[2], pos[3:], flags['--min'], flags['--model'], secret_ok)
    else:
        print(__doc__)


main(sys.argv[1:])
