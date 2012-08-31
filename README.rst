django-sphinxsearch
=======================
This is a fork of ``django-sphinx`` devoid of its shortcomings.

*Note:* Now only works in conjunction Django + Mysql + SphinxSearch.

Installation
------------

To install the latest development version (updated quite often)::

	git clone git://github.com/adw0rd/django-sphinxsearch.git
	cd django-sphinxsearch
	python setup.py install

*Note:* You will need to install the `sphinxapi.py` package into your Python Path or use one of the included versions. To use the included version, you must specify the following in your `settings.py` file::

	# Sphinx 0.9.9 and above
	SPHINX_API_VERSION = 0x116

	# Sphinx 0.9.8
	SPHINX_API_VERSION = 0x113

	# Sphinx 0.9.7
	SPHINX_API_VERSION = 0x107

Usage
-----

The following is some example usage::

	from djangosphinxsearch.managers import SearchManager

	class MyModel(models.Model):

		search = SearchManager()
		# The default "index_name" is taken from the SPHINX_INDEX_PREFIX + MyModel._meta.db_table
		# Or you can specify the "index_name" like this:
		search = SearchManager('index_name')

		# Or maybe we want to be more.. specific
		searchdelta = SearchManager(
			index='index_name delta_name',
			fields={
				'name': 100,
				'description': 10,
				'tags': 80,
			},
			mode='SPH_MATCH_ALL',
			rankmode='SPH_RANK_NONE',
			limit=100
		)

	queryset = MyModel.search.query('query')
	results1 = queryset.filter(my_attribute=5)
	results2 = queryset.exclude(my_attribute=5)[0:10]
	results3 = queryset.count()


If you can not specify a manager in the model, you can use this::

	from djangosphinxsearch.managers import SearchManager
	from django.contrib.comments import Comment

	Comment.search = SearchManager(index="my_index_for_comments", fields={'name': 50, 'description': 200})
	Comment.search.contribute_to_class(model=Comment, name="search")

	queryset = Comment.search.query('test', indexes='my_custom_index_for_comments')



Conversations:
-----

Russian topic: http://pyha.ru/forum/topic/7894.0
