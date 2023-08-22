from requests import get
from time import sleep
import os, json, lzma

data = {}
try:
    with open(os.path.join('..', 'data', 'LG.json.7z'), 'rb') as f:
        data = json.loads(lzma.decompress(f.read()).decode('utf-8'))
except:
    print('WARNING: OVERLOAD')
    pass

data['URL'] = 'www.luogu.com.cn/problem/P{0}'
data['PID'] = 'LG {0}'

def fetch(name):
    return get(f'https://www.luogu.com.cn/problem/{name}?_contentOnly', headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.78'
        })

def get_samples(name):
    if(f'{name[1:]}' in data):
        return
    sleep(2)
    resp = fetch(name)
    while resp.status_code != 200:
        print(f'warn: fetched status code {resp.status_code}, retrying.')
        sleep(2)
        resp = fetch(name)
    if resp.json()['code'] != 200:
        print(f'warn: {name} is forbidden, {resp.json()["currentData"]["errorMessage"]}')
        return
    samples = resp.json()['currentData']['problem']['samples']
    sample_id = 0; data[f'{name[1:]}'] = []
    for [sample_input, sample_output] in samples:
        sample_id += 1
        data[f'{name[1:]}'].append([sample_input.strip(), sample_output.strip()])
    print(f'info: fetched {name} with {sample_id} samples.')
print('From ??? to ???')
x, y = map(int, input().split())
names = [f'P{_}' for _ in range(x, y + 1)]
for name in names:
    get_samples(name)
with open(os.path.join('..', 'data', 'LG.json.7z'), 'wb') as f:
    f.write(lzma.compress(json.dumps(data, separators=(',', ':')).encode('utf-8')))
