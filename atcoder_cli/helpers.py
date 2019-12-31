import requests
from requests.sessions import Session
import json
from bs4 import BeautifulSoup
from pathlib import Path
import pickle


def get_answer():
    """Get an answer."""
    return True

def get_csrf(session: Session, url: str) -> str:
    res = session.get(url)
    bs = BeautifulSoup(res.text, 'html.parser')
    csrf = bs.find(attrs={'name':'csrf_token'}).get('value')
    return csrf

def dump_session(session: Session) -> None:
    with open(Path(__file__).resolve().parents[0].joinpath('.internal', 'session'), 'wb') as f:
        pickle.dump(session, f)

def load_session() -> Session:
    pt = Path(__file__).resolve().parents[0].joinpath('.internal', 'session')
    if pt.exists():
        with open(pt, 'rb') as f:
            return pickle.load(f)
    else:
        return None

def load_conf() -> {}:
    pt = Path(__file__).resolve().parents[0].joinpath('.internal', 'conf.json')
    with open(pt, 'r') as f:
        return json.load(f)

def dump_conf(data) -> None:
    pt = Path(__file__).resolve().parents[0].joinpath('.internal', 'conf.json')
    with open(pt, 'w') as f:
        json.dump(data, f, indent=4)

def get_lang_info(lang: str) -> (str, str):
    lang_info = {}
    lang_info['python3'] = ('3023', 'py')
    return lang_info[lang]