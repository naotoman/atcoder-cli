from typing import List

_LANGS = {
    'python': ('3023', 'py', 'Python3 (3.4.3)'),
    'pypy': ('3510', 'py', 'PyPy3 (2.4.0)'),
    'rust': ('3504', 'rs', 'Rust (1.15.1)'),
    'kotlin': ('3523', 'kt', 'Kotlin (1.0.0)'),
    'cpp': ('3003', 'cpp', 'C++14 (GCC 5.4.1)'),
    'java': ('3016', 'java', 'Java8 (OpenJDK 1.8.0)')
}

def langs() -> List[str]:
    return list(_LANGS.keys())

def exists(lang: str) -> bool:
    return str in _LANGS

def number(lang: str) -> str:
    return _LANGS[lang][0]

def suffix(lang: str) -> str:
    return _LANGS[lang][1]

def full_name(lang: str) -> str:
    return _LANGS[lang][2]