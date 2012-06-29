# coding: utf-8
import unittest
from nose.tools import eq_


class TestSphinxSearch(unittest.TestCase):

    def setUp(self):
        from django.db import connection
        from django.db.models.base import ModelBase
        from django.core.management.color import no_style
        from django_sphinxsearch.managers import SearchManager

        # Create a dummy model which extends the mixin
        import  pudb; pudb.set_trace()
        self.model = ModelBase('__TestModel__{}'.format(self.mixin.__name__), (self.mixin, ),
                { '__module__': self.mixin.__module__ })
        # Create the schema for our test model
        self._style = no_style()
        sql, _ = connection.creation.sql_create_model(self.model, self._style)
        self._cursor = connection.cursor()
        for statement in sql:
            self._cursor.execute(statement)

        self.model.search = SearchManager(index="test_index", fields={'data': 100}, limit=10)
        self.model.search.contribute_to_class(model=self.model, name="search")

        source_data = (
            "Python is a programming language that lets you work more quickly and integrate your systems more effectively.",
            "You can learn to use Python and see almost immediate gains in productivity and lower maintenance costs.",
            "Python runs on Windows, Linux/Unix, Mac OS X, and has been ported to the Java and .NET virtual machines.",
            "Python is free to use, even for commercial products, because of its OSI-approved open source license.",
            "New to Python or choosing between Python 2 and Python 3? Read Python 2 or Python 3.",
            "The Python Software Foundation holds the intellectual property rights behind Python, underwrites the PyCon conference, and funds other projects in the Python community."
        )
        for pk, data in enumerate(source_data, start=1):
            instance = self.model(pk=pk, data=data)
            instance.save()

        # Generate config
        # Run indexer

    def tearDown(self):
        # Delete the schema for the test model
        sql = connection.creation.sql_destroy_model(self.model, (), self._style)
        for statement in sql:
            self._cursor.execute(statement)

    def test_search_query(self):
        search_query = "Java"
        results = self.model.search.query(search_query)
        eq_(bool(results), True)
        result = results[0]
        eq_(result.data, 3)  # pk=3, because it is Java

if __name__ == '__main__':
    import os
    import sys
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
    unittest.main()

# To run the test suite
# pip install nose
# python tests.py -v
