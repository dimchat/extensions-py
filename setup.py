#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
    DIM Application eXtensions
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    Extensions for DaoKeDao module
"""

import io

from setuptools import setup, find_packages

__version__ = '1.0.0'
__author__ = 'Albert Moky'
__contact__ = 'albert.moky@gmail.com'

with io.open('README.md', 'r', encoding='utf-8') as fh:
    readme = fh.read()

setup(
    name='dimax',
    version=__version__,
    url='https://github.com/dimchat/extensions-py',
    license='MIT',
    author=__author__,
    author_email=__contact__,
    description='DIM Application eXtensions',
    long_description=readme,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    package_data={
        '': ['res/*.js']
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=[
        'dimp>=2.4.3',
    ]
)
