# coding: utf-8
from django.db import models
from djangosphinxsearch.apis import current as sphinxapi
from djangosphinxsearch import settings


class SearchManager(models.Manager):

    def __init__(self, index=None, fields={}, mode='SPH_MATCH_ALL', sort='SPH_SORT_RELEVANCE', limit=20, *a, **kw):
        super(SearchManager, self).__init__(*a, **kw)
        self._index = index
        self._sphinx = sphinxapi.SphinxClient()
        self._sphinx.SetServer(
            settings.SPHINX_SERVER.get('host', 'localhost'),
            settings.SPHINX_SERVER.get('port', 3312))
        self._sphinx.SetMatchMode(getattr(sphinxapi, mode))
        self._sphinx.SetSortMode(getattr(sphinxapi, sort))
        self._sphinx.SetFieldWeights(fields)
        self._sphinx.SetLimits(0, limit)

    def _get_indexes_with_prefix(self, indexes):
        index_prefix = settings.DJANGO_SPHINXSEARCH_PREFIX + "_" if settings.DJANGO_SPHINXSEARCH_PREFIX else ""
        indexes = [
            index_prefix + index_name
            for index_name in indexes.split(" ")]
        return " ".join(indexes)

    def query(self, search_query, indexes=None, queryset=None):
        self._index = self.model._meta.db_table if not self._index and hasattr(self, 'model') else self._index
        indexes = self._get_indexes_with_prefix(indexes or self._index)
        self._search_results = self._sphinx.Query(search_query, indexes)
        matches = (self._search_results or {}).get('matches', [])
        objects_ids = [str(m['id']) for m in matches]
        if queryset is None:
            queryset = self.get_query_set()
        if not objects_ids:
            queryset = queryset.filter(pk__in=[None])
        else:
            db_table = queryset.model._meta.db_table
            queryset = queryset.filter(pk__in=objects_ids)\
            .extra(select={'djangosphinxsearch_position': 'FIELD(`{}`.`id`, {})'.format(db_table, ",".join(objects_ids))})\
            .order_by('djangosphinxsearch_position')
        return queryset