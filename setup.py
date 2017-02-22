from setuptools import setup, find_packages

import pybier

def readme():
    with open('README.rst') as f:
        return f.read()

setup(
    name='pybier',
    version='0.1',
    url='http://github.com/r-bierman/pybier/',
    license='Apache Software License',
    author='Rob Bierman',
    author_email='rbierman@stanford.edu',
    description='Personal python package to cleanly store code I reuse',
    long_description=readme(),
    packages=['pybier'],
    scripts=['bin/pydrive_sync'],
    install_requires=[],
    include_package_data=True,
    zip_safe=False,
    test_suite='nose.collector',
    tests_require=['nose'],
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
