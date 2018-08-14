from elasticsearch.client.utils import NamespacedClient, query_params, _make_path


class FeaturesClient(NamespacedClient):

    def __init__(self, client):
        NamespacedClient.__init__(self, client)
        default_store_request = self.transport.perform_request('GET', _make_path('_ltr'))
        if not default_store_request['stores']:
            self._init_default_store()

    @query_params('master_timeout', 'timeout', 'wait_for_active_shards')
    def _init_default_store(self, params=None):
        """
        Inits the default store '_ltr'

        `<https://elasticsearch-learning-to-rank.readthedocs.io/en/latest/building-features.html>`_

        :arg master_timeout: Specify timeout for connection to master
        :arg timeout: Explicit operation timeout
        :arg wait_for_active_shards: Set the number of active shards to wait for
            before the operation returns.

        :return:
        """

        return self.transport.perform_request('PUT', _make_path('_ltr'),
                                              params=params)

    @query_params('master_timeout', 'timeout', 'wait_for_active_shards')
    def _delete_default_store(self, params=None):
        """
        Deletes the default store '_ltr'

        `<https://elasticsearch-learning-to-rank.readthedocs.io/en/latest/building-features.html>`_

        :arg master_timeout: Specify timeout for connection to master
        :arg timeout: Explicit operation timeout
        :arg wait_for_active_shards: Set the number of active shards to wait for
            before the operation returns.

        :return:
        """
        return self.transport.perform_request('DELETE', _make_path('_ltr'),
                                              params=params)

    @query_params('master_timeout', 'timeout', 'wait_for_active_shards')
    def create_featureset(self, featureset, features, params=None):
        """
        Create an featureset in Elasticsearch LTR plugin.
        `<https://elasticsearch-learning-to-rank.readthedocs.io/en/latest/building-features.html>`_
        :arg featureset: The name of the featureset
        :arg features: The list of features specified with the Mustache templates syntax
        :arg master_timeout: Specify timeout for connection to master
        :arg timeout: Explicit operation timeout
        :arg wait_for_active_shards: Set the number of active shards to wait for
            before the operation returns.
        """
        return self.transport.perform_request('POST', _make_path('_ltr', '_featureset', featureset),
                                              params=params, body={'featureset': {'features': features}})

    @query_params('master_timeout', 'timeout', 'wait_for_active_shards')
    def append_features(self, featureset, new_features, params=None):
        """
        Append list of features to an existing featureset.
        `<https://elasticsearch-learning-to-rank.readthedocs.io/en/latest/building-features.html>`_
        :arg featureset: The name of the featureset
        :arg new_features: The list of new features to be added. This features will override existing features with the
        same name
        :arg master_timeout: Specify timeout for connection to master
        :arg timeout: Explicit operation timeout
        :arg wait_for_active_shards: Set the number of active shards to wait for
            before the operation returns.
        """
        # self._init_default_store()
        return self.transport.perform_request('POST', _make_path('_ltr', '_featureset', featureset, '_addfeatures'),
                                              params=params, body={'features': new_features})

    @query_params('master_timeout', 'timeout', 'wait_for_active_shards')
    def get_featureset(self, featureset, params=None):
        """
        Get a featureset given its name

        `<https://elasticsearch-learning-to-rank.readthedocs.io/en/latest/building-features.html>`_

        :arg featureset: Name of the featureset
        :arg master_timeout: Specify timeout for connection to master
        :arg timeout: Explicit operation timeout
        :arg wait_for_active_shards: Set the number of active shards to wait for
            before the operation returns.

        :return: A JSON describing the feature set
        """

        return self.transport.perform_request('GET', _make_path('_ltr', '_featureset', featureset), params=params)

    @query_params('master_timeout', 'timeout', 'wait_for_active_shards')
    def list_featuresets(self, prefix=None, params=None):
        """
        List all feature sets. Optionally, filter by prefix

        `<https://elasticsearch-learning-to-rank.readthedocs.io/en/latest/building-features.html>`_

        :arg prefix: Prefix in order to filter feature sets
        :arg master_timeout: Specify timeout for connection to master
        :arg timeout: Explicit operation timeout
        :arg wait_for_active_shards: Set the number of active shards to wait for
            before the operation returns.

        :return: A JSON describing the list of feature sets
        """

        if prefix:
            prefix_path = '/_featureset?prefix={0}'.format(prefix)
        else:
            prefix_path = '/_featureset'

        return self.transport.perform_request('GET', _make_path('_ltr') + prefix_path, params=params)

    @query_params('master_timeout', 'timeout', 'wait_for_active_shards')
    def delete_featureset(self, featureset, params=None):
        """
        Delete a featureset given its name

        `<https://elasticsearch-learning-to-rank.readthedocs.io/en/latest/building-features.html>`_

        :arg featureset: Name of the featureset
        :arg master_timeout: Specify timeout for connection to master
        :arg timeout: Explicit operation timeout
        :arg wait_for_active_shards: Set the number of active shards to wait for
            before the operation returns.

        """

        return self.transport.perform_request('DELETE', _make_path('_ltr', '_featureset', featureset), params=params)

    @query_params('master_timeout', 'timeout', 'wait_for_active_shards')
    def log_features(self, index, documents, featureset, feature_params, params=None):
        """
        Compute features for a set of documents and given parameters (the parameters required to compute the features
        like the query keywords, the user name, etc.

        `<https://elasticsearch-learning-to-rank.readthedocs.io/en/latest/logging-features.html>`_
        :arg documents List of identifiers of the documents for which the features are being computed
        :arg featureset: Name of the featureset
        :arg feature_params: Parameters needed to compute the features, such as the query keywords or the user name
        :arg master_timeout: Specify timeout for connection to master
        :arg timeout: Explicit operation timeout
        :arg wait_for_active_shards: Set the number of active shards to wait for
            before the operation returns.

        :return A list of objects containing the document identifier and the computed features
        """
        query = {
            "bool": {
                "filter": {
                    "terms": {
                        "_id": documents
                    }
                }, "must": {
                    "sltr": {
                        "_name": "logged_featureset",
                        "featureset": featureset,
                        "params": feature_params
                    }}
            }
        }

        ext_features = {
            "ltr_log": {
                "log_specs": {
                    "name": "log_entry1",
                    "named_query": "logged_featureset"
                }
            }}

        body = {"query": query, "ext": ext_features}

        results = self.transport.perform_request('GET', _make_path(index, '_search'), body=body, params=params)

        return [{'_id': result['_id'], 'features': result['fields']['_ltrlog'][0]['log_entry1']}
                for result in results['hits']['hits']]
