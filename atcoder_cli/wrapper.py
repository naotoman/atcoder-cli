from typing import Dict, List, Union, Any
import getpass
from requests.sessions import Session
import time
from pathlib import Path
import json

from . import atcoder
from . import helpers

def signin() -> Session:
    username = input('Username: ')
    password = getpass.getpass()
    session = atcoder.signin(username, password)
    return session

def code_test(contest: str, lang: str, src: str, stdin: str, session: Session) -> Dict[str, Any]:
    atcoder.submit_custom_test(contest, lang, src, stdin, session)
    time.sleep(1)
    result = atcoder.get_custom_test_result(contest, session)
    while result['Result']['Status'] != 3:
        time.sleep(1)
        result = atcoder.get_custom_test_result(contest, session)
    
    return result

def get_inout_samples(contest: str, problem: str, session: Session) -> Dict[str, Union[str, List[str]]]:
    pt = Path(__file__).resolve().parents[0].joinpath('.internal', f'problem_{problem}.json')
    if pt.exists():
        with open(pt, 'r') as f:
            js = json.load(f)
            if js['contest'] == contest:
                return js
    with open(pt, 'w') as f:
        js = atcoder.get_inout_samples(contest, problem, session)
        js['contest'] = contest
        json.dump(js, f)
        return js