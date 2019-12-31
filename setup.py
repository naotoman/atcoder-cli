# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='atcoder-cli',
    version='0.1.0',
    description='cli tools for atcoder.',
    long_description=readme,
    author='Naoto Kido',
    author_email='me@example.com',
    url='https://github.com/',
    license=license,
    packages=find_packages(exclude=('tests', 'docs')),
    entry_points={
        'console_scripts': ['atc=atcoder_cli.command_line:main'],
    }
)

