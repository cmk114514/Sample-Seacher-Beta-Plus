from bs4 import BeautifulSoup as bs
from time import sleep
import requests as req
import os, json, lzma
from os.path import join as pjoin

data = {}
try:
    with open(os.path.join('..', 'data', 'UOJ.json.7z'), 'rb') as f:
        data = json.loads(lzma.decompress(f.read()).decode('utf-8'))
except:
    print('WARNING: OVERLOAD')
    pass

data['URL'] = "uoj.ac/problem/{0}"
data['PID'] = "UOJ {0}"

try:
    os.mkdir('data/' + uoj_url)
except Exception:
    pass
def get(pid):
    if f'{pid}' in data:
        return None
    sleep(10)
    print(f'Getting {pid}...')
    try:
        url = f'https://uoj.ac/problem/{pid}'
        res = req.get(url, headers = {
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; Tablet PC 2.0; wbx 1.0.0; wbxapp 1.0.0; Zoom 3.6.0)'
            })
        s = bs(res.text, 'lxml')
        sa = s.select('#tab-statement > article > h4')
        ret = []
        for e in sa:
            if e.get_text() == "input":
                ret.append((e.next_sibling.next_sibling.get_text().strip(), e.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.get_text().strip()))
        return ret
    except Exception as e:
        print(f'Error {e}')
        return []
def save(pid, sam):
    if sam is None:
        return
    print(f'Saving {pid}...')
    try:
        data[f'{pid}'] = []
        for i in range(len(sam)):
            data[f'{pid}'].append([sam[i][0].strip(), sam[i][1].strip()])
    except Exception as e:
        print(f'Error {e}')
l, r = map(int, input("From ?~?: ").split())
for i in range(l, r + 1):
    save(i, get(i))
with open(os.path.join('..', 'data', 'UOJ.json.7z'), 'wb') as f:
    f.write(lzma.compress(json.dumps(data, separators=(',', ':')).encode('utf-8')))
