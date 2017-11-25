#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Reference: https://docs.python.org/3/distutils/setupscript.html
import os
import sys

from setuptools import (
    setup,
    find_packages,
)


DIR = os.path.dirname(os.path.abspath(__file__))


readme = open(os.path.join(DIR, 'README.md')).read()

install_requires = [
    "cytoolz>=0.8.2",
    "ethereum-abi-utils>=0.4.3",
    "ethereum-keyfile>=0.3.0",
    "ethereum-keys>=0.1.0-alpha.7",
    "ethereum-utils>=0.5.0",
    "pylru>=1.0.9",
    "pysha3>=0.3",
    "requests>=2.12.4",
    "rlp>=0.4.7",
    "toolz>=0.8.2",
    "ethereum-tester~=0.1.0b1",
]

if sys.platform == 'win32':
    install_requires.append('pypiwin32')

setup(
    name='pyethfinality',
    version='1.0.0',
    description="""PyEthFinality""",
    long_description_markdown_filename='README.md',
    author='Luke Schoen',
    author_email='ltfschoen@gmail.com',
    url='https://github.com/pipermerriam/web3.py',
    include_package_data=True,
    install_requires=install_requires,
    setup_requires=['setuptools-markdown'],
    extras_require={
        'tester': ["eth-testrpc>=1.3.3"],
    },
    py_modules=['web3', 'ens'],
    license="BSD",
    zip_safe=False,
    keywords='ethereum finality',
    packages=find_packages(exclude=["tests", "tests.*"]),
    classifiers=[
        'Development Status :: 1',
    ],
)