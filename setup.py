#!/usr/bin/env python
from setuptools import setup, find_packages
from djangosphinxsearch import __version__

setup(
    name='django-sphinxsearch',
    version=__version__,
    description = 'An integration layer bringing Django and SphinxSearch together.',
    keywords='django, sphinx, sphinxsearch',
    author='Mikhail Andreev',
    author_email='x11org@gmail.com',
    url='http://github.com/adw0rd/django-sphinxsearch',
    license='BSD',
    install_requires=['django>=1.3'],
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Operating System :: OS Independent",
        "Environment :: Web Environment",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet :: WWW/HTTP :: Indexing/Search",
    ],
)
