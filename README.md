# elasticsearch-ltr-py
Python client to deal with Learning to Rank (automatic relevance optimization)
 plugin for Elasticsearch (https://elasticsearch-learning-to-rank.readthedocs.io/en/latest)

Installation
------------

Open a terminal and in the project root folder run:

    python setup.py install

Example use
-----------

    >>> from elasticsearch_ltr import ElasticsearchLTR
    >>> es = ElasticsearchLTR()
    >>> es.features.get_featureset('test_featureset')
    
See more examples in the package _elasticsearch_ltr/example_