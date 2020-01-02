# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages


with open('LICENSE') as f:
    license = f.read()

def _requires_from_file(filename):
    return open(filename).read().splitlines()

setup(
    name='atcoder-cli',
    version='0.1.0',
    description='cli tools for atcoder.',
    author='Naoto Kido',
    url='https://github.com/',
    license=license,
    packages=find_packages(exclude=('tests')),
    install_requires=_requires_from_file('requirements.txt'),
    setup_requires=["pytest-runner"],
    tests_require=["pytest", "pytest-cov"],
    entry_points={
        'console_scripts': ['atc=atcoder_cli.commands:main'],
    }
)

