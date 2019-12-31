import argparse
from pathlib import Path
import getpass
import os
import time

from . import atcoder
from . import wrapper
from . import helpers

def command_init(args: argparse.Namespace) -> None:
    session = helpers.load_session()
    if not (session and atcoder.is_signed(session)):
        session = wrapper.signin()

    contest = args.contest
    lang = args.lang
    problems = atcoder.get_problems(contest, session)

    if Path(contest).exists():
        print('already exists')
        return
    lang_info = helpers.get_lang_info(lang)
    for p in problems:
        Path(f'{contest}/{p}').mkdir(parents=True)
        Path(f'{contest}/{p}/{p}.{lang_info[1]}').touch()
    
    conf = {'contest': contest, 'language': lang_info[0]}
    conf['src_files'] = {}
    for p in problems:
        conf['src_files'][p] = f'{os.getcwd()}/{contest}/{p}/{p}.{lang_info[1]}'

    helpers.dump_conf(conf)
    helpers.dump_session(session)


def command_sub(args: argparse.Namespace):
    print(args)
   

def command_test(args: argparse.Namespace):
    session = helpers.load_session()
    if not (session and atcoder.is_signed(session)):
        session = wrapper.signin()
    
    conf = helpers.load_conf()
    prob = args.problem
    src = ''
    with open(conf['src_files'][prob], 'r') as f:
        src = f.read()

    samples = wrapper.get_inout_samples(conf['contest'], prob, session)
    for stdin, stdout in (samples['input'], samples['output']):
        result = wrapper.code_test(conf['contest'], conf['language'], src, stdin, session)
        print('[in]')
        print(stdin)
        print('[out]')
        print(result['Stdout'])
        print(stdout == result['Stdout'])
    
    helpers.dump_session(session)
    
def command_signin(args: argparse.Namespace) -> None:
    session = wrapper.signin()
    helpers.dump_session(session)

def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    # init
    parser_init = subparsers.add_parser('init', help='see `init -h`')
    parser_init.add_argument('-c', required=True, help='contest name', dest='contest')
    lang_options = ['python3', 'pypy']
    parser_init.add_argument('-l', required=True, choices=lang_options, help='programming language to use', dest='lang')
    parser_init.set_defaults(func=command_init)

    # signin
    parser_signin = subparsers.add_parser('signin', help='see `signin -h`')
    parser_signin.set_defaults(func=command_signin)

    # submit
    parser_sub = subparsers.add_parser('sub', help='see `sub -h`')
    parser_sub.add_argument('problem', help='problem to solve')
    parser_sub.add_argument('-f', '--force', action='store_true', help='submit without testing')
    parser_sub.set_defaults(func=command_sub)

    # test
    parser_test = subparsers.add_parser('test', help='see `test -h`')
    parser_test.add_argument('problem', help='problem to solve')
    parser_test.set_defaults(func=command_test)

    args = parser.parse_args()
    args.func(args)