from bs4 import BeautifulSoup as bs
import requests as req
from time import sleep
import os, json, lzma
from os.path import join as pjoin

data = {}
try:
    with open(os.path.join('..', 'data', 'CF.json.7z'), 'rb') as f:
        data = json.loads(lzma.decompress(f.read()).decode('utf-8'))
except:
    print('WARNING: OVERLOAD')
    pass

data['URL'] = 'codeforces.com/problemset/problem/{0}/{1}'
data['PID'] = 'CF {0} {1}'

def get(cid, pid):
    if f'{cid} {pid}' in data:
        return None
    sleep(2)
    print(f'Getting {cid}{pid}...')
    try:
        url = f'https://codeforces.com/contest/{cid}/problem/{pid}'
        res = req.get(url, headers = {
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; Tablet PC 2.0; wbx 1.0.0; wbxapp 1.0.0; Zoom 3.6.0)'
            })
        txt = res.text.replace('<br/>', '\n').replace('<br />', '\n')
        s = bs(txt, 'lxml')
        si = s.select('#pageContent > div.problemindexholder > div.ttypography > div.problem-statement > div.sample-tests > div.sample-test > div.input > pre')
        so = s.select('#pageContent > div.problemindexholder > div.ttypography > div.problem-statement > div.sample-tests > div.sample-test > div.output > pre')
        assert len(si) == len(so)
        ret = []
        for i in range(0, len(si)):
            ca = si[i].select('div')
            if len(ca) != 0:
                in_txt = ''
                for j in ca:
                    in_txt += j.get_text() + '\n'
                ret.append((in_txt, so[i].get_text()))
            else:
                ret.append((si[i].get_text(), so[i].get_text()))
        return ret
    except Exception as e:
        print(f'Error {e}')
        return get(cid, pid)
def save(cid, pid, sam):
    if sam is None:
        return
    print(f'Saving {cid}{pid}...')
    try:
        data[f'{cid} {pid}'] = []
        for i in range(len(sam)):
            data[f'{cid} {pid}'].append([sam[i][0].strip(), sam[i][1].strip()])
    except Exception as e:
        print(f'Error {e}')
def get_and_save(cid):
    print(f'Getting {cid}...')
    try:
        url = f'https://codeforces.com/contest/{cid}'
        res = req.get(url, headers = {
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; Tablet PC 2.0; wbx 1.0.0; wbxapp 1.0.0; Zoom 3.6.0)'
            })
        s = bs(res.text, 'lxml')
        p = s.select('#pageContent > div.datatable > div > table.problems > tr > td.id > a')
        for i in p:
            pid = i.get_text().strip()
            save(cid, pid, get(cid, pid))
    except Exception as e:
        print(f'Error {e}')
l, r = map(int, input('From ?~?: ').split())
for i in range(l, r + 1):
    get_and_save(i)

with open(os.path.join('..', 'data', 'CF.json.7z'), 'wb') as f:
    f.write(lzma.compress(json.dumps(data, separators=(',', ':')).encode('utf-8')))
