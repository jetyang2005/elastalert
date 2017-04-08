from elasticsearch import Elasticsearch
es = Elasticsearch([{'host':'localhost','port':9200}])
es.search(index='2017*', q='*')