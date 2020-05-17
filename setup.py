#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup
from setuptools import find_packages

setup(
    name='oautom',
    version='1.0.0',
    packages=find_packages(exclude=["*_tests"]),
    license='MIT',
    long_description=open('README.md').read(),
    install_requires = [
        'apscheduler'
    ],
    extras_require={
        'dev': [
            'honcho',
            'pylint',
            'coverage',
            'api_based_workflow'
        ]
    },
    classifier= [
        'Programming Language :: Python :: 3',
        'Framework :: Flask',
        'Operating System :: POSIX :: Linux'
    ],
)
