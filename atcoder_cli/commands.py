import argparse
from pathlib import Path
import requests
from requests.sessions import Session
import getpass

from . import atcoder
from . import wrapper
from . import data_io as io
from . import lang_info as lg


def command_gen(args: argparse.Namespace) -> None:
    session = _get_session()

    # validation
    

    contest = args.contest
    lang = args.lang
    problems = atcoder.get_problems(contest, session)
    lang_info = io.get_lang_info(lang)
    cur = Path('.')

    if not (cur/contest/lang).exists():
        (cur/contest/lang/'src').mkdir(parents=True)
        for p in problems:
            (cur/contest/lang/'src'/f'{p}.{lang_info[1]}').touch()
        if lang == 'rust':
            pt_dir = Path(__file__).resolve().parents[0]/'resources'/lang
            with open(pt_dir/'template.rs', 'r') as t:
                template = t.read()
                for p in problems:
                    with open(cur/contest/lang/'src'/f'{p}.{lang_info[1]}', 'w') as f:
                        f.write(template)
            with open(pt_dir/'Cargo.toml', 'r') as r, open(cur/contest/lang/'Cargo.toml', 'w') as w:
                toml = r.read()
                w.write(toml + '\n')
                for p in problems:
                    abs_path = str((cur/contest/lang/'src'/f'{p}.rs').resolve())
                    w.write(f'[[bin]]\nname = "{p}"\npath = "{abs_path}"\n\n')
                
    conf = {'contest': contest, 'lang': lang_info[0]}
    conf['src'] = {}
    for p in problems:
        conf['src'][p] = str((cur/contest/lang/'src'/f'{p}.{lang_info[1]}').resolve())

    io.dump_conf(conf)
    io.dump_session(session)


def command_sub(args: argparse.Namespace) -> None:
    session = _get_session()

    conf = io.load_conf()
    prob = args.problem
    src = ''
    with open(conf['src'][prob], 'r') as f:
        src = f.read()

    samples = wrapper.get_inout_samples(conf['contest'], prob, session)
    submit = True
    for stdin, stdout in zip(samples['input'], samples['output']):
        result = wrapper.code_test(conf['contest'], conf['lang'], src, stdin, session)
        if result['Result']['ExitCode'] == 0 and result['Stdout'] == stdout:
            continue
        submit = False
        print('[in]')
        print(stdin)
        if result['Result']['ExitCode'] != 0:
            print('[err]')
            print(result['Stderr'])
        else:
            print('[out (correct)]')
            print(stdout)
            print('[out (answer)]')
            print(result['Stdout'])
    if submit:
        atcoder.submit(conf['contest'], prob, conf['lang'], src, session)
        print('passed test. submit.')
    
    io.dump_session(session)


def command_test(args: argparse.Namespace) -> None:
    session = _get_session()
    
    conf = io.load_conf()
    prob = args.problem
    src = ''
    with open(conf['src'][prob], 'r') as f:
        src = f.read()

    samples = wrapper.get_inout_samples(conf['contest'], prob, session)
    for stdin, stdout in zip(samples['input'], samples['output']):
        result = wrapper.code_test(conf['contest'], conf['lang'], src, stdin, session)
        print('[in]')
        print(stdin)
        print('[out]')
        print(result['Stdout'])
        print(stdout == result['Stdout'])
    
    io.dump_session(session)


def command_result(args: argparse.Namespace) -> None:
    session = _get_session()

    contest = args.contest or io.load_conf()['contest']
    results = atcoder.get_submit_results(contest, session)
    color_green = '\033[92m'
    color_end = '\033[0m'
    max_len = max(map(lambda x: len(x[-1]), results.values()))
    for p in sorted(results.keys()):
        print(f'{p}: ', end='')
        l_str = results[p][-1].ljust(max_len)
        if results[p][-1] == 'AC':
            print(f'{color_green}{l_str}{color_end} ({color_green}AC{color_end})')
        elif 'AC' in results[p]:
            print(f'{l_str} ({color_green}AC{color_end})')
        else:
            print(f'{l_str}')
    io.dump_session(session)

def command_login(args: argparse.Namespace) -> None:
    session = requests.Session()
    _login(session)
    io.dump_session(session)

def command_user(args: argparse.Namespace) -> None:
    if io.has_session:
        session = io.load_session()
        usr = atcoder.get_current_user(session)
        if usr:
            print(f'You are logged in as `{usr}`.')
            return
    print('You are not logged in.')


def main() -> None:
    langs = lg.langs()

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    # login
    parser_login = subparsers.add_parser('login', help='log in to AtCoder')
    parser_login.set_defaults(func=command_login)

    # gen
    parser_gen = subparsers.add_parser('gen', help='set defaults and make directories for the contest')
    parser_gen.add_argument('contest', help='contest name')
    parser_gen.add_argument('-l', '--lang', choices=langs, help='programming language')
    parser_gen.set_defaults(func=command_gen)

    # test
    parser_test = subparsers.add_parser('test', help='test your code on AtCoder server')
    parser_test.add_argument('problem', help='problem to solve')
    parser_test.add_argument('-c', '--contest', help='contest name')
    parser_test.add_argument('-l', '--lang', choices=langs, help='programming language for your code')
    parser_test.add_argument('-s', '--src', help='path to your source code')
    parser_test.set_defaults(func=command_test)

    # sub
    parser_sub = subparsers.add_parser('sub', help='test your code and submit it to AtCoder server')
    parser_sub.add_argument('problem', help='problem to solve')
    parser_sub.add_argument('-f', '--force', action='store_true', help='submit without testing')
    parser_sub.add_argument('-c', '--contest', help='contest name')
    parser_sub.add_argument('-l', '--lang', choices=langs, help='programming language for your code')
    parser_sub.add_argument('-s', '--src', help='path to your source code')
    parser_sub.set_defaults(func=command_sub)

    # result
    parser_result = subparsers.add_parser('result', help='show results of the newest submissions for each problem')
    parser_result.add_argument('-c', '--contest', help='contest name')
    parser_result.set_defaults(func=command_result)

    # user
    parser_user = subparsers.add_parser('user', help='show the logged in user')
    parser_user.set_defaults(func=command_user)


    info_dir = Path.home()/'.atcoder_cli_info'
    if not info_dir.exists():
        info_dir.mkdir()
        info_dir.chmod(0o700)

    args = parser.parse_args()
    args.func(args)


# Funtctions used only in this file ################
def _get_session() -> Session:
    if io.has_session():
        session = io.load_conf()
        if atcoder.get_current_user(session):
            return session
    session = requests.Session()
    _login(session)
    return session
        

def _login(session: Session) -> None:
    username = input('Username: ')
    password = getpass.getpass()
    atcoder.login(username, password, session)
