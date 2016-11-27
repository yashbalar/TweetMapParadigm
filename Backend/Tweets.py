from flask import jsonify, url_for, redirect, request
from flask_restful import Resource
from flask import render_template,request
import json
#Custome Imports

from StreamTweet.streamTweet import keywords
from Backend.Config import *


class Tweets(Resource):

    def get(self,keyword=None):
        if keyword:
            response = es.search(index='twitter', doc_type='tweet',body={"query": {"query_string": {"query": keyword}}}, size=2000)
            data = {'searchParams': keywords, 'tweets': response['hits']['hits'], 'currentSearch': keyword}
            return jsonify(data)
        else:
            # searchtext = keywords[0]
            # response = es.search(index='test1', doc_type='tweet',body={"query": {"query_string": {"query": searchtext}}}, size=2000)
            # data = {'searchParams': keywords, 'tweets': response['hits']['hits']}
            # return jsonify(data)

            response = es.search(index='twitter', doc_type='tweet',
                                 body={"query": {"match_all": {}}}, size=2000)
            data = {'searchParams': keywords, 'tweets': response['hits']['hits']}
            return jsonify(data)

    def post(self):
        print(request)
        data = json.loads(request.get_json())
        print('Tweet indexed into elasticsearch...')
        print(data)
        es.index(index='twitter', doc_type='tweet', body=data)
        socketio.emit('json',data)






