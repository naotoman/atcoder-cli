from typing import Dict, Any
from requests.sessions import Session
import time

from . import atcoder


def code_test(contest: str, lang: str, src: str,
              stdin: str, session: Session) -> Dict[str, Any]:
    atcoder.submit_custom_test(contest, lang, src, stdin, session)
    time.sleep(1)
    result = atcoder.get_custom_test_result(contest, session)
    cnt = 20
    while cnt > 0 and result['Result']['Status'] != 3:
        cnt -= 1
        time.sleep(1)
        result = atcoder.get_custom_test_result(contest, session)
    if result['Result']['Status'] != 3:
        return {}
    return result
