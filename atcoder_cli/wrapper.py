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