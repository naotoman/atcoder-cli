from typing import List, Dict, Any, Tuple, Union
from bs4 import BeautifulSoup
import requests
from requests.sessions import Session
import json
import re

ATCODER_URL = 'https://atcoder.jp'


class Atcoder:

    def get_current_user(self, session: Session) -> str:
        quit_url = f'{ATCODER_URL}/quit'
        res = session.get(quit_url, allow_redirects=False)
        if res.status_code != 200:
            return ''
        else:
            bs = BeautifulSoup(res.text, "html.parser")
            la = bs.find('label', text=re.compile('(Username|ユーザ名)'))
            return la.parent.find('input')['value']

    def signin(self, username: str, password: str, session: Session) -> None:
        signin_url = f'{ATCODER_URL}/login'

        data = {'username': username, 'password': password}
        data['csrf_token'] = self.__get_csrf(signin_url, session)

        session.post(signin_url, data=data)


    def submit(self, contest: str, problem: str, lang: str, src: str, session: Session) -> None:
        submit_url = f'{ATCODER_URL}/contests/{contest}/submit'

        data = {'data.TaskScreenName': f'{contest}_{problem}', 'data.LanguageId': lang, 'sourceCode': src}
        data['csrf_token'] = self.__get_csrf(submit_url, session)

        session.post(submit_url, data)


    def submit_custom_test(self, contest: str, lang: str, src: str, stdin: str, session: Session) -> None:
        custom_test_url = f'{ATCODER_URL}/contests/{contest}/custom_test'
        custom_test_submit_api = f'{custom_test_url}/submit/json'

        data = {'data.LanguageId': lang, 'sourceCode': src, 'input': stdin}
        data['csrf_token'] = self.__get_csrf(custom_test_url, session)

        session.post(custom_test_submit_api, data)


    def get_custom_test_result(self, contest: str, session: Session) -> Dict[str, Any]:
        res = session.get(f'{ATCODER_URL}/contests/{contest}/custom_test/json')
        result = json.loads(res.text)
        return result


    def get_inout_samples(self, contest: str, problem: str, session: Session) -> Dict[str, List[str]]:
        problem_url = f'{ATCODER_URL}/contests/{contest}/tasks/{contest}_{problem}'
        res = session.get(problem_url)
        bs = BeautifulSoup(res.text, "html.parser")
        divs = bs.find_all('div', class_='part')
        inputs = []
        outputs = []
        for div in divs:
            if "入力例" in div.section.h3.string:
                inputs.append(div.section.pre.string.replace('\r\n', '\n'))
            if "出力例" in div.section.h3.string:
                outputs.append(div.section.pre.string.replace('\r\n', '\n'))
        return {'input': inputs, 'output': outputs}


    def get_problems(self, contest: str, session: Session) -> List[str]:
        problems_url = f'{ATCODER_URL}/contests/{contest}/tasks'
        res = session.get(problems_url)
        ng = not res
        if ng:
            contest_url = f'{ATCODER_URL}/contests/{contest}'
            res = session.get(contest_url)
        
        bs = BeautifulSoup(res.text, "html.parser")
        rows = bs.find('tbody').findAll("tr")

        if ng:
            return [row.findAll('td')[0].string.lower() for row in rows]
        else:
            return [row.findAll('td')[0].a.string.lower() for row in rows]

    def get_submit_results(self, contest: str, session: Session) -> Dict[str, List[str]]:
        result_url = f'{ATCODER_URL}/contests/{contest}/submissions/me?orderBy=created'
        res = session.get(f'{result_url}&page=1')
        bs = BeautifulSoup(res.text, "html.parser")
        
        pages = bs.find('ul', class_='pagination').findAll('li')
        max_page = max(map(lambda x: int(x.a.string), pages))

        results = {}
        for i in range(1, max_page + 1):
            if i > 1:
                res = session.get(f'{result_url}&page={i}')
                bs = BeautifulSoup(res.text, "html.parser")
            rows = bs.find('tbody').findAll('tr')
            for tr in rows:
                tds = tr.findAll('td')
                prob = tds[1].a.get('href').split('_')[-1].lower()
                status = tds[6].span.string
                if not prob in results:
                    results[prob] = []
                results[prob].append(status)
        return results


    def __get_csrf(self, url: str, session: Session) -> str:
        res = session.get(url)
        bs = BeautifulSoup(res.text, 'html.parser')
        csrf = bs.find(attrs={'name':'csrf_token'}).get('value')
        return csrf