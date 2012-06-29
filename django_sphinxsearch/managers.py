# coding: utf-8
from django.db import models
from django_sphinxsearch.apis import current as sphinxapi
from django_sphinxsearch import settings


class SearchManager(models.Manager):

    def __init__(self, index=None, fields={}, mode='SPH_MATCH_ALL', sort='SPH_SORT_RELEVANCE', limit=20, *a, **kw):
        super(SearchManager, self).__init__(*a, **kw)
        self._index = index
        self._sphinx = sphinxapi.SphinxClient()
        self._sphinx.SetServer(settings.SPHINX_SERVER['host'], settings.SPHINX_SERVER['port'])
        self._sphinx.SetMatchMode(getattr(sphinxapi, mode))
        self._sphinx.SetSortMode(getattr(sphinxapi, sort))
        self._sphinx.SetFieldWeights(fields)
        self._sphinx.SetLimits(0, limit)

    def _get_indexes_with_prefix(self, indexes):
        index_prefix = settings.SPHINX_INDEX_PREFIX + "_" if settings.SPHINX_INDEX_PREFIX else ""
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
            model_meta = queryset.model._meta
            if model_meta.get_field_by_name('id')[1]:
                db_table = model_meta.get_field_by_name('id')[1]._meta.db_table
            else:
                db_table = model_meta.db_table
            queryset = queryset.filter(pk__in=objects_ids)\
                .extra(select={'django_sphinxsearch_position': 'FIELD(`{}`.`id`, {})'.format(db_table, ",".join(objects_ids))})\
                .order_by('django_sphinxsearch_position')
        return queryset
