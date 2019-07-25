# from elasticsearch import Elasticsearch
# from elasticsearch.helpers import bulk
# import json 
 
# es = Elasticsearch()

# def index_data():
#     global es
#     with open("searchai/main/dataset.json") as f:
#         data = json.load(f)
#     items = [{
#         "_op_type": "index",
#         "_id": i,
#         "_source": {
#             "imgurl": data['images'][i]['filename'],
#             "description": data['images'][i]['sentences'][0]['raw'],
#         }
#     } for i in range(len(data['images']))]
#     bulk(es,items,index="desearch",doc_type="json")

# def description_search(query, number):
#     global es
#     results = es.search(
#         index="desearch",
#         body={
#             "size": number,
#             "query": {
#             "match": {
#                 "description": {
#                     'query': query,
#                     'operator': 'and',
#                     'fuzziness': 'auto:2,6',
#                     }
#                 }
#             }
#         })
#     hitCount = results['hits']['total']
#     if hitCount > 0:
#         if hitCount is 1:
#             print(str(hitCount),' result')
#         else:
#             print(str(hitCount), 'results')
#         answers =[]  
#         for hit in results['hits']['hits']:
#             desc = hit['_source']['description']
#             imgurl = 'static/img/'+ hit['_source']['imgurl']
#             answers.append([imgurl,desc])
#     else:
#         answers = []
#     return answers
