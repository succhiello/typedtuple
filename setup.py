#!/usr/bin/env python
from setuptools import setup, find_packages


setup(
    name='typedtuple',
    version='0.0.1',
    description='namedtuple with validation',
    author='xica developer team',
    author_email='info@xica.net',
    url='http://github.com/xica/typedtuple',
    packages=find_packages(),
    install_requires=[
        'voluptuous',
        'six',
    ],
    extras_require={
        'fast': [
            'cnamedtuple',
        ],
    },
    tests_require=[
        'pytest'
    ],
)
