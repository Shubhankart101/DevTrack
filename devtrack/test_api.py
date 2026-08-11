import json
import urllib.request
import urllib.error

BASE = 'http://127.0.0.1:8000/api'

requests = [
    ('POST', f'{BASE}/reporters/', {
        'id': 1,
        'name': 'Alice Engineer',
        'email': 'alice@example.com',
        'team': 'backend',
    }),
    ('GET', f'{BASE}/reporters/', None),
    ('GET', f'{BASE}/reporters/?id=1', None),
    ('POST', f'{BASE}/issues/', {
        'id': 1,
        'title': 'Login button not working on mobile',
        'description': 'Users on iOS 17 cannot tap the login button',
        'status': 'open',
        'priority': 'critical',
        'reporter_id': 1,
    }),
    ('GET', f'{BASE}/issues/', None),
    ('GET', f'{BASE}/issues/?id=1', None),
    ('GET', f'{BASE}/issues/?status=open', None),
]

for method, url, data in requests:
    print('---')
    print(method, url)
    try:
        if method == 'POST':
            body = json.dumps(data).encode('utf-8')
            req = urllib.request.Request(url, data=body, headers={'Content-Type': 'application/json'}, method='POST')
        else:
            req = urllib.request.Request(url, method='GET')
        with urllib.request.urlopen(req) as resp:
            text = resp.read().decode('utf-8')
            print('STATUS', resp.status)
            print(text)
    except urllib.error.HTTPError as e:
        print('STATUS', e.code)
        print(e.read().decode('utf-8'))
    except Exception as e:
        print('ERROR', e)
