#!/usr/bin/env python
from setuptools import setup, find_packages


setup(
    name='typedtuple',
    version='0.1.1',
    description='namedtuple with validation',
    author='Satoshi Ebihara',
    author_email='succhiello@gmail.com',
    url='http://github.com/succhiello/typedtuple',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
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
