from django.conf import settings

SPHINX_SERVER = {
    'host': 'localhost',
    'port': 3306,
    }
SPHINX_SERVER = getattr(settings, 'SPHINX_SERVER', SPHINX_SERVER)

DJANGO_SPHINXSEARCH_PREFIX= getattr(settings, 'DJANGO_SPHINXSEARCH_PREFIX', '')

# Sphinx 0.9.9 and above -> 0x116
# Sphinx 0.9.8 -> 0x113
# Sphinx 0.9.7 -> 0x107
SPHINX_API_VERSION = getattr(settings, 'SPHINX_API_VERSION', 0x116)