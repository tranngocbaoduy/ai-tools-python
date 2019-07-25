from searchai import create_app
# from searchai.capgen import CaptionGenerator 
# from elasticsearch import Elasticsearch
# from elasticsearch.helpers import bulk
import json 

app = create_app()
 
if __name__ == '__main__': 
    app.run(debug=True)
 