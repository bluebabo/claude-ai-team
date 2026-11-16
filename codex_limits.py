# codex 남은 한도 조회 — 모델을 부르지 않고 app-server 의 account/rateLimits/read 만 묻는다 (남은 % + 초기화 시각)
import json, os, subprocess, sys, time
env = dict(os.environ)
env['PATH'] = os.pathsep.join([os.path.expandvars(r'%ProgramFiles%\nodejs'), os.path.expandvars(r'%APPDATA%\npm'), env['PATH']])
env.pop('OPENAI_API_KEY', None)
p = subprocess.Popen(['cmd', '/c', 'codex.cmd', 'app-server'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, env=env, text=True, encoding='utf-8')
def send(o):
    p.stdin.write(json.dumps(o) + '\n'); p.stdin.flush()
send({'id': 1, 'method': 'initialize', 'params': {'clientInfo': {'name': 'limits', 'version': '0'}}})
send({'method': 'initialized'})
send({'id': 2, 'method': 'account/rateLimits/read'})
t0 = time.time()
for line in p.stdout:
    print(line.strip()[:1500])
    if '"id":2' in line or time.time() - t0 > 40:
        break
p.kill()
