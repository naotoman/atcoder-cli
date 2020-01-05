from typing import Dict
import argparse
from pathlib import Path
import requests
from requests.sessions import Session
import getpass

from . import atcoder
from . import wrapper
from . import data_io as io
from . import lang_info as lg

GREEN = '\033[92m'
WARNINGC = '\033[93m'
FAILC = '\033[91m'
ENDC = '\033[0m'


def command_gen(args: argparse.Namespace) -> None:
    session = _get_session()

    # validation
    

    contest = args.contest
    lang = args.lang
    problems = atcoder.get_problems(contest, session)
    lang_info = []
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
    data = _validate_sub(args)
    src = ''
    with open(data['src'], 'r') as f:
        src = f.read()

    session = _get_session()
    io.dump_session(session)

    if args.force:
        atcoder.submit(data['contest'], args.problem, data['lang'], src, session)
        print('submit without testing.')
        return

    samples = io.get_inout_samples(data['contest'], args.problem, session)
    submit = True
    for stdin, stdout in zip(samples['input'], samples['output']):
        result = wrapper.code_test(data['contest'], data['lang'], src, stdin, session)
        if result['Result']['ExitCode'] == 0 and result['Stdout'] == stdout:
            continue
        submit = False
        print('[in]')
        print(stdin.rstrip())
        if result['Result']['ExitCode'] == 9:
            print(f'{FAILC}TLE{FAILC}')
        elif result['Result']['ExitCode'] != 0:
            print('[err]')
            print(result['Stderr'].rstrip())
            print(f'{WARNINGC}CE or RE{WARNINGC}')
        else:
            print('[expected]')
            print(stdout.rstrip())
            print('[out]')
            print(result['Stdout'].rstrip())
            print(f'{FAILC}WA{FAILC}')
    if submit:
        atcoder.submit(data['contest'], args.problem, data['lang'], src, session)
        print('passed all test. submit.')
    

def command_test(args: argparse.Namespace) -> None:
    data = _validate_sub(args)
    src = ''
    with open(data['src'], 'r') as f:
        src = f.read()
    session = _get_session()
    io.dump_session(session)

    samples = io.get_inout_samples(data['contest'], args.problem, session)
    for stdin, stdout in zip(samples['input'], samples['output']):
        print('[in]')
        print(stdin.rstrip())
        print('[expected]')
        print(stdout.rstrip())
        result = wrapper.code_test(data['contest'], data['lang'], src, stdin, session)
        if result['Result']['ExitCode'] == 9:
            print(f'{FAILC}TLE{FAILC}')
        elif result['Result']['ExitCode'] != 0:
            print('[err]')
            print(result['Stderr'].rstrip())
            print(f'{WARNINGC}CE or RE{WARNINGC}')
        else:
            print('[out]')
            print(result['Stdout'].rstip())
            if result['Stdout'] == stdout:
                print(f'{GREEN}AC{GREEN}')
            else:
                print(f'{FAILC}WA{FAILC}')
    

def command_result(args: argparse.Namespace) -> None:
    # validate
    contest = args.contest
    if contest is None and io.has_conf():
        contest = io.load_conf().get('contest', None)
    if contest is None:
        print(f'{FAILC}use -c option or edit conf.json to specify a contest.{FAILC}')
        exit()

    session = _get_session()
    io.dump_session(session)

    results = atcoder.get_submit_results(contest, session)
    if not results:
        print(f'There are no submissions for {contest}.')
        return
    max_len = max(map(lambda x: len(x[-1]), results.values()))
    for p in sorted(results.keys()):
        print(f'{p}: ', end='')
        l_str = results[p][-1].ljust(max_len)
        if results[p][-1] == 'AC':
            print(f'{GREEN}{l_str}{ENDC} ({GREEN}AC{ENDC})')
        elif 'AC' in results[p]:
            print(f'{l_str} ({GREEN}AC{ENDC})')
        else:
            print(f'{l_str}')

def command_login(args: argparse.Namespace) -> None:
    session = requests.Session()
    _login(session)
    io.dump_session(session)

def command_user(args: argparse.Namespace) -> None:
    if io.has_session():
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
    parser_test.add_argument('-s', '--src', help='path to your sourcecode file')
    parser_test.set_defaults(func=command_test)

    # sub
    parser_sub = subparsers.add_parser('sub', help='test your code and submit it to AtCoder server')
    parser_sub.add_argument('problem', help='problem to solve')
    parser_sub.add_argument('-f', '--force', action='store_true', help='submit without testing')
    parser_sub.add_argument('-c', '--contest', help='contest name')
    parser_sub.add_argument('-l', '--lang', choices=langs, help='programming language for your code')
    parser_sub.add_argument('-s', '--src', help='path to your sourcecode file')
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


# below: funtctions used only in this file ################

def _get_session() -> Session:
    if io.has_session():
        session = io.load_session()
        if atcoder.get_current_user(session):
            return session
    session = requests.Session()
    _login(session)
    return session
        

def _login(session: Session) -> None:
    username = input('Username: ')
    password = getpass.getpass()
    atcoder.login(username, password, session)
    cur = atcoder.get_current_user(session)
    if not (cur and (cur == username)):
        print(f'{FAILC}Failed to login.{FAILC}')
        exit()


def _validate_sub(args: argparse.Namespace) -> Dict[str, str]:
    res = {}
    conf = {}
    if io.has_conf():
        conf = io.load_conf()

    exit_flag = False
    # contest
    if args.contest is not None:
        res['contest'] = args.contest
    elif 'contest' in conf:
        res['contest'] = conf['contest']
    else:
        print(f'{FAILC}use -c option or edit conf.json to specify a contest.{FAILC}')
        exit_flag = True
    
    # lang
    if args.lang is not None:
        res['lang'] = args.lang
    elif 'lang' in conf:
        res['lang'] = conf['lang']
    else:
        print(f'{FAILC}use -l option or edit conf.json to specify a language.{FAILC}')
        exit_flag = True
    
    # src
    if args.src is not None:
        res['src'] = args.src
    elif ('src' in conf) and (args.problem in conf['src']):
        res['src'] = conf['src'][args.problem]
    else:
        print(f'{FAILC}use -s option or edit conf.json to specify a path to the sourcecode.{FAILC}')
        exit_flag = True
    
    if exit_flag:
        exit()
    return res