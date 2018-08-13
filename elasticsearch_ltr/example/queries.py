from elasticsearch_ltr import ElasticsearhLTR

# Sample connexion to a local Elasticsearch cluster. Change values to fit your cluster
es = ElasticsearhLTR(host='localhost', timeout=100, max_retries=5,
                     retry_on_timeout=True, maxsize=50, http_auth=('elastic', 'changeme'))

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
print(es.ltr.create_featureset(featureset, features))

# List featuresets. Previous featureset should be listed
print(es.ltr.list_featuresets())

# List featuresets, filtering by prefix. No featuresets should be listed
print(es.ltr.list_featuresets(prefix='notest'))

# List featuresets, filtering by prefix. Previous featureset should be listed
print(es.ltr.list_featuresets(prefix='test'))

# Retrieve created featureset
print(es.ltr.get_featureset(featureset))

# Delete created featureset
print(es.ltr.delete_featureset(featureset))
