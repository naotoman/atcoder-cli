# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('LICENSE') as f:
    license = f.read()


def _requires_from_file(filename):
    return open(filename).read().splitlines()


setup(
    name='atcoder-cli',
    version='0.1.2',
    description='cli tools for AtCoder.',
    author='Naoto Kido',
    url='https://github.com/naotoman/atcoder-cli',
    license=license,
    packages=find_packages(exclude=('tests')),
    install_requires=_requires_from_file('requirements.txt'),
    include_package_data=True,
    setup_requires=["pytest-runner"],
    tests_require=["pytest", "pytest-cov"],
    entry_points={
        'console_scripts': ['atc=atcoder_cli.commands:main'],
    }
)
