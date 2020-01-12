from typing import Dict, Any
import json
from pathlib import Path
import pickle
from requests.sessions import Session

from . import atcoder


data_dir = Path.home()/'.atcoder_cli_info'


def has_session() -> bool:
    ck = data_dir/'cookie.pkl'
    return ck.exists()


def load_session() -> Any:
    ck = data_dir/'cookie.pkl'
    with open(ck, 'rb') as f:
        return pickle.load(f)


def dump_session(session: Session) -> None:
    ck = data_dir/'cookie.pkl'
    with open(ck, 'wb') as f:
        pickle.dump(session, f)
        ck.chmod(0o600)


def has_conf() -> bool:
    cf = data_dir/'conf.json'
    return cf.exists()


def load_conf() -> Any:
    cf = data_dir/'conf.json'
    with open(cf, 'r') as f:
        return json.load(f)


def dump_conf(data: Dict[str, Any]) -> None:
    cf = data_dir/'conf.json'
    with open(cf, 'w') as f:
        json.dump(data, f, indent=4)


def get_inout_samples(contest: str, problem: str, session: Session) -> Any:
    pt = data_dir/f'problem_{problem}.json'
    if pt.exists():
        with open(pt, 'r') as f:
            js = json.load(f)
            if js['contest'] == contest:
                return js
    with open(pt, 'w') as f:
        js = atcoder.get_inout_samples(contest, problem, session)
        js['contest'] = contest
        json.dump(js, f, indent=4)
        return js
