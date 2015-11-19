#!/usr/bin/env python

from setuptools import setup

setup(
    name='pwgen-passphrase',
    version='1.1',
    description='Secure wordlist-based passphrase generator',
    author='Michal Krenek (Mikos)',
    author_email='m.krenek@gmail.com',
    url='https://github.com/xmikos/pwgen-passphrase',
    license='GNU GPLv3',
    packages=['pwgen_passphrase'],
    package_data={
        "pwgen_passphrase": [
            "wordlists/*.txt"
        ]
    },
    entry_points={
        'console_scripts': [
            'pwgen-passphrase=pwgen_passphrase.__main__:main'
        ],
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Security',
        'Topic :: Utilities'
    ]
)
