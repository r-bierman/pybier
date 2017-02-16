from setuptools import setup, find_packages
import codecs
import sys
import io
import os

import pybier_test

setup(
    name='pybier_test',
    version='0.1',
    url='http://github.com/r-bierman/pybier_test/',
    license='Apache Software License',
    author='Rob Bierman',
    author_email='rbierman@stanford.edu',
    description='Learning to build python package',
    long_description='long_description',
    packages=['pybier_test'],
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
