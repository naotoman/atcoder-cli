from pathlib import Path
import json
from bs4 import BeautifulSoup
import requests

# pt = Path(__file__).resolve().parents[0].joinpath('.internal', 'conf.json')


# with pt.open('r') as f:
#     js = json.load(f)
#     js['test'] = 'hello'
#     print(js)

session = requests.session()
problem_url = f'https://atcoder.jp/contests/abc141/taskss'
res = session.get(problem_url)
print(res)
if res:
    print('yes')
else:
    print('no')

bs = BeautifulSoup(res.text, "html.parser")

table = bs.findAll("table")[0].findAll('tbody')[0]
rows = table.findAll("tr")

for row in rows:
    print(row.findAll('td')[0].a.string)