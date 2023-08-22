from bs4 import BeautifulSoup as bs
import requests as req
from os.path import join as pjoin
import re, time, os, json, lzma

Type = input('Type: ').strip().upper();
assert Type[0] == 'A' and Type[-1] == 'C'
stitle = re.compile(r'(入|出)力例\s?\d+')

data = {}
try:
    with open(os.path.join('..', 'data', f'{Type}.json.7z'), 'rb') as f:
        data = json.loads(lzma.decompress(f.read()).decode('utf-8'))
except:
    print('WARNING: OVERLOAD')
    pass

data['URL'] = f'atcoder.jp/contests/{Type}{{0}}/tasks/{Type}{{0}}_{{1}}'
data['PID'] = f'{Type} {{0}} {{1}}'

def get(cid, pid, url):
    if f'{cid[3:]} {pid.upper()}' in data:
        return None
    print(f'Getting {cid}{pid}...')
    try:
        res = req.get(url, headers = {
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; Tablet PC 2.0; wbx 1.0.0; wbxapp 1.0.0; Zoom 3.6.0)'
            })
        time.sleep(2)
        s = bs(res.text, 'lxml')
        sa = s.select('#task-statement > div > section')
        if sa == []:
            sa = s.select('#task-statement > span > span.lang-ja > div > section')
        if sa == []:
            sa = s.select('#task-statement > span > span.lang-jp > div > section')
        if sa == []:
            return []
        tsa = []
        for i in sa:
            if stitle.match(i.find('h3').get_text()):
                tsa.append(i.find('pre'))
        assert len(tsa) % 2 == 0
        ret = []
        for i in range(0, len(tsa), 2):
            ret.append((tsa[i].get_text(), tsa[i + 1].get_text()))
        return ret
    except Exception as e:
        print(f'Error {e}')
        return []
def save(cid, pid, sam):
    if sam is None:
        return
    print(f'Saving {cid}{pid}...')
    try:
        data[f'{cid[3:]} {pid.upper()}'] = []
        for i in range(len(sam)):
            data[f'{cid[3:]} {pid.upper()}'].append([sam[i][0].replace('\r', '').strip(), sam[i][1].replace('\r', '').strip()])
    except Exception as e:
        print(f'Error {e}')
def get_and_save(cid):
    print(f'Getting {cid}...')
    try:
        url = f'https://atcoder.jp/contests/{cid}/tasks'
        res = req.get(url, headers = {
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; Tablet PC 2.0; wbx 1.0.0; wbxapp 1.0.0; Zoom 3.6.0)'
            })
        time.sleep(2)
        s = bs(res.text, 'lxml')
        p = s.select('#main-container > div.row > div:nth-child(2) > div > table > tbody > tr > td:nth-child(1) > a')
        for i in p:
            lk = i.get('href')
            tmp = lk.split('/')
            rcid, pid = tmp[2], tmp[4].split('_')[-1]
            save(rcid, pid, get(rcid, pid, 'https://atcoder.jp' + lk))
    except Exception as e:
        print(f'Error {e}')
l, r = map(int, input('From ?~?: ').split())
for i in range(l, r + 1):
    get_and_save('%s%03d' % (Type.upper(), i))

with open(os.path.join('..', 'data', f'{Type}.json.7z'), 'wb') as f:
    f.write(lzma.compress(json.dumps(data, separators=(',', ':')).encode('utf-8')))
