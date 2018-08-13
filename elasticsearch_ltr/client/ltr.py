from elasticsearch.client.utils import NamespacedClient, query_params, _make_path, SKIP_IN_PATH


class LTRClient(NamespacedClient):

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
        # self._init_default_store()
        return self.transport.perform_request('PUT', _make_path('_ltr', '_featureset', featureset),
                                              params=params, body={'featureset': {'features': features}})

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
