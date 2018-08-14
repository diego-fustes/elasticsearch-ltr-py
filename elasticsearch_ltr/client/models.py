from elasticsearch.client.utils import NamespacedClient, query_params, _make_path


class ModelsClient(NamespacedClient):

    def __init__(self, client):
        NamespacedClient.__init__(self, client)

    @query_params('master_timeout', 'timeout', 'wait_for_active_shards')
    def upload_model(self, featureset, model, params=None):
        """
        Upload a model to Elasticsearch

        `<https://elasticsearch-learning-to-rank.readthedocs.io/en/latest/training-models.html>`_

        :arg featureset: Name of the featureset related to the model
        :arg model: Model object to be uploaded
        :type model: A elasticsearch_ltrModel object from the
        :arg master_timeout: Specify timeout for connection to master
        :arg timeout: Explicit operation timeout
        :arg wait_for_active_shards: Set the number of active shards to wait for
            before the operation returns.

        """
        return self.transport.perform_request('POST', _make_path('_ltr', '_featureset', featureset, '_createmodel'),
                                              params=params,
                                              body={'model': {"name": model.name, "model": {"type": model.type,
                                                                                            "definition": model.definition}
                                                              }})

    @query_params('master_timeout', 'timeout', 'wait_for_active_shards')
    def get_model(self, model_name, params=None):
        """
        Retrieve a model from Elasticsearch

        `<https://elasticsearch-learning-to-rank.readthedocs.io/en/latest/training-models.html>`_

        :arg model_name: Name of the model
        :arg master_timeout: Specify timeout for connection to master
        :arg timeout: Explicit operation timeout
        :arg wait_for_active_shards: Set the number of active shards to wait for
            before the operation returns.

        """
        return self.transport.perform_request('GET', _make_path('_ltr', '_model', model_name),
                                              params=params)

    @query_params('master_timeout', 'timeout', 'wait_for_active_shards')
    def delete_model(self, model_name, params=None):
        """
        Delete a model from Elasticsearch

        `<https://elasticsearch-learning-to-rank.readthedocs.io/en/latest/training-models.html>`_

        :arg model_name: Name of the model
        :arg master_timeout: Specify timeout for connection to master
        :arg timeout: Explicit operation timeout
        :arg wait_for_active_shards: Set the number of active shards to wait for
            before the operation returns.

        """
        return self.transport.perform_request('DELETE', _make_path('_ltr', '_model', model_name),
                                              params=params)

    @query_params('master_timeout', 'timeout', 'wait_for_active_shards')
    def rescore_query(self, index, query, model_name, feature_params, window_size=1000, features=None, params=None):
        """
        Rescore the first elements of a query result by means of a stored model

        `<https://elasticsearch-learning-to-rank.readthedocs.io/en/latest/searching-with-your-model.html>`_

        :arg index: Index to which the query is sent
        :arg query: Query to match documents at first glance
        :arg model_name: Name of the model to rescore the search results
        :arg feature_params: Parameters needed to compute the model features
        :arg window_size: Number of results to be rescored and thus reranked
        :arg features: Optionally, specify the features to be included in the model computation
        :arg master_timeout: Specify timeout for connection to master
        :arg timeout: Explicit operation timeout
        :arg wait_for_active_shards: Set the number of active shards to wait for
            before the operation returns.

        """

        sltr = {
            'sltr': {
                'params': feature_params,
                'model': model_name,
            }
        }

        if features:
            sltr['active_features'] = features

        body = {'query': query,
                'rescore': {
                    'window_size': window_size,
                    'query': {
                        'rescore_query': sltr
                    }
                }
                }

        return self.transport.perform_request('GET', _make_path(index, '_search'),
                                              body=body, params=params)
