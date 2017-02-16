from setuptools import setup, find_packages
import codecs
import sys
import io
import os

import pybier

setup(
    name='pybier',
    version='0.1',
    url='http://github.com/r-bierman/pybier/',
    license='Apache Software License',
    author='Rob Bierman',
    author_email='rbierman@stanford.edu',
    description='Personal python package to cleanly store code I reuse',
    long_description='Contains python research tools I build, such as queries to ucsc and plotting',
    packages=['pybier'],
    include_package_data=True,
    platforms='any',
    classifiers = [
        'Programming Language :: Python',
        'Development Status :: 4 - Beta',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        ],
)
