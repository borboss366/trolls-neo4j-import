import requests
items = []
initial = "http://archive.org/wayback/available"

with open('names.csv') as f:
    for line in f:
        params = {'url': 'http://twitter.com/' + line}
        r = requests.get(initial, params=params)
        d = r.json()
        print(d)
        items.append(d)

with open('./data/available_urls.csv', 'w') as f:
    for item in items:
        if 'archived_snapshots' in item:
            if 'closest' in item['archived_snapshots']:
                f.write(item['archived_snapshots']['closest']['url'] + '\n')