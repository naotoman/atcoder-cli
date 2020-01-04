from typing import Dict, Tuple, Any, Union
import requests
from requests.sessions import Session
import json
from bs4 import BeautifulSoup
from pathlib import Path
import pickle

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