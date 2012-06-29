# coding: utf-8
from django_sphinxsearch.settings import SPHINX_API_VERSION

try:
    # if you have installed sphinxapi, then use it.
    from sphinxapi import *
except (ImportError, ), exc:
    # Otherwise, if you set SPHINX_API_VERSION, we use this version.
    # If not, use the latest version of the "sphinxsearch.api278"
    name = '{}.api{}'.format(__name__.rpartition(".")[0], SPHINX_API_VERSION)
    sphinxapi = __import__(name)
    for name in name.split('.')[1:]:
        sphinxapi = getattr(sphinxapi, name)
    for attr in dir(sphinxapi):
        globals()[attr] = getattr(sphinxapi, attr)
