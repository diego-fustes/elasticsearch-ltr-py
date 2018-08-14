from elasticsearch_ltr import ElasticsearchLTR, Model

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
    }, {
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

# Create featureset
print(es.features.create_featureset(featureset, features))

# Upload model
model = Model(name='my_linear_model', type='model/linear', definition='{"title_query": 0.3,  "user_rating": 0.8}')
es.models.upload_model(featureset, model)

# Retrieve model
print(es.models.get_model(model.name))

# Create index
index = 'lorem'
doc1 = {'title': 'lorem ipsum', 'vote_average': 0}
es.index(index=index, doc_type='space', id="doc1", body=doc1)
doc2 = {'title': 'dolor sit amet', 'vote_average': 2}
es.index(index=index, doc_type='space', id="doc2", body=doc2)

# Launch search
match_query = {'match_all': {}}
print(es.search(index=index, body={'query': match_query}))

# Rescore search with stored model
print(es.models.rescore_query(index=index, query=match_query, model_name=model.name,
                              feature_params={'keywords': 'lorem'}))

# Delete model
print(es.models.delete_model(model.name))
