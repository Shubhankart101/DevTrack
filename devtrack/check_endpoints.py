import urllib.request
import urllib.error
import json

urls = [
    'http://127.0.0.1:8000/',
    'http://127.0.0.1:8000/api/',
    'http://127.0.0.1:8000/api/reporters/',
    'http://127.0.0.1:8000/api/issues/'
]

for u in urls:
    print('URL:', u)
    try:
        r = urllib.request.urlopen(u)
        text = r.read().decode('utf-8', errors='ignore')
        print('STATUS', r.status)
        print(text[:200])
    except urllib.error.HTTPError as e:
        print('STATUS', e.code)
        print(e.read().decode('utf-8', errors='ignore'))
    except Exception as e:
        print('ERROR', e)
    print('---')
