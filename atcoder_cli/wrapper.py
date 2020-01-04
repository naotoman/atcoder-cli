from typing import Dict, List, Union, Any
import getpass
from requests.sessions import Session
import time
from pathlib import Path
import json

from . import atcoder


def code_test(contest: str, lang: str, src: str, stdin: str, session: Session) -> Dict[str, Any]:
    atcoder.submit_custom_test(contest, lang, src, stdin, session)
    time.sleep(1)
    result = atcoder.get_custom_test_result(contest, session)
    while result['Result']['Status'] != 3:
        time.sleep(1)
        result = atcoder.get_custom_test_result(contest, session)
    
    return result

def get_inout_samples(contest: str, problem: str, session: Session) -> Dict[str, Union[str, List[str]]]:
    pt = Path.home()/'.atcoder_cli_info'/f'problem_{problem}.json'
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