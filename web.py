from flask import *
import os, difflib, json, lzma
app = Flask('Sample Searcher Beta+')
html, data = None, {}
MAXL = 256
with open('index.html') as f:
    html = f.read()
for dirpath, dirnames, filenames in os.walk('data'):
    for filepath in filenames:
        with open(os.path.join(dirpath, filepath), 'rb') as f:
            data[filepath.split('.')[0]] = json.loads(lzma.decompress(f.read()))
print('init OK')
def simi(x, y):
    return difflib.SequenceMatcher(None, x, y).ratio()
@app.route('/')
def index():
    return html
@app.route('/favicon.ico')
def favicon():
    return redirect('/static/favicon.ico')
@app.route('/search')
def search():
    ret = []
    cin = request.args.get('i').strip()
    cout = request.args.get('o').strip()
    if len(cin) > MAXL or len(cout) > MAXL:
        return jsonify([])
    checkIn = request.args.get('t') != '2'
    checkOut = request.args.get('t') != '0'
    for probset in data:
        for name in data[probset]:
            if type(data[probset][name]) is not list:
                continue
            i = 0
            for sam_li in data[probset][name]:
                i += 1
                try:
                    if len(sam_li[0]) <= MAXL and len(sam_li[1]) <= MAXL:
                        std, cio = '', ''
                        if checkIn:
                            std += sam_li[0] + '\0'; cio += cin + '\0'
                        if checkOut:
                            std += sam_li[1] + '\0'; cio += cout + '\0'
                        v = simi(std, cio)
                        if int(v * 100) >= 80:
                            token = name.split(' ')
                            ret.append({
                                'URL': data[probset]['URL'].format(*token).lower(),
                                'PID': data[probset]['PID'].format(*token),
                                'SID': i, 'SIM': int(v * 100), 
                            })
                except Exception as e:
                    print(f'Error {e} | {probset} {name}')
                    pass
    ret.sort(key = lambda x : -x['SIM'])
    return jsonify(ret)
app.run('127.0.0.1', 80)
