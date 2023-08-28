import os, json, lzma, re
print('probset', 'size', 'last', sep='\t')
for file in os.listdir(os.path.join('..', 'data')):
    n = 0
    with open(os.path.join('..', 'data', file), 'rb') as f:
        data = json.loads(lzma.decompress(f.read()).decode('utf-8'))
    for token in data:
        tmp = re.compile('\d+').search(token)
        if tmp is not None: n = max(n, int(tmp.group()))
    print(file.split('.')[0], len(data) - 2, n, sep='\t')
