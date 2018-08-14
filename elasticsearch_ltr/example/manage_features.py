from elasticsearch_ltr import ElasticsearchLTR

# Sample connexion to a local Elasticsearch cluster. Change values to fit your cluster
es = ElasticsearchLTR(host='localhost', timeout=100, max_retries=5,
                      retry_on_timeout=True, maxsize=50, http_auth=('elastic', 'BbdemoforMgmt1!'))

featureset = 'test_featureset'

features = [
    {
        "name": "title_query",
        "params": [
            "keywords"
        ],
        "template_language": "mustache",
        "template": {
            "match": {
                "title": "{{keywords}}"
            }
        }
    }]

# Create featureset
print(es.features.create_featureset(featureset, features))

# List featuresets. Previous featureset should be listed
print(es.features.list_featuresets())

# List featuresets, filtering by prefix. No featuresets should be listed
print(es.features.list_featuresets(prefix='notest'))

# List featuresets, filtering by prefix. Previous featureset should be listed
print(es.features.list_featuresets(prefix='test'))

# Add more features to the featureset
additional_features = [{
    "name": "user_rating",
    "params": [],
    "template_language": "mustache",
    "template": {
        "function_score": {
            "field_value_factor": {
                "field": "vote_average",
            },
            "query": {
                "match_all": {}
            }
        }
    }
}]

print(es.features.append_features(featureset, additional_features))

# Retrieve created featureset. Additional features should be listed
print(es.features.get_featureset(featureset))

# Create index and log features for indexed documents and query
index = 'lorem'
doc1 = {'title': 'lorem ipsum', 'vote_average': 0}
es.index(index=index, doc_type='space', id="doc1", body=doc1)
doc2 = {'title': 'dolor sit amet', 'vote_average': 2}
es.index(index=index, doc_type='space', id="doc2", body=doc2)

print(es.features.log_features(index=index, documents=["doc1", "doc2"], featureset=featureset,
                               feature_params={'keywords': 'lorem'}))

# Delete created featureset
print(es.features.delete_featureset(featureset))
