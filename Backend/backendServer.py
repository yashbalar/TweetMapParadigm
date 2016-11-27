#!/usr/bin/env python3
import sys
sys.path.append("/home/ec2-user/TweetMapParadigm")

from flask_restful import Api
from Backend.Tweets import *
from Backend.Subscription import *
from Backend.Config import *


if not es.indices.exists(index='twitter'):
    es.indices.create(index='twitter', ignore=400)

@app.route('/',methods=['GET'])
def index():
    if 'q' in request.args.keys():
        keyword = request.args['q']
        response = es.search(index='twitter', doc_type='tweet', body={"query": {"query_string": {"query": keyword}}},size=2000)
    else:
        response = es.search(index='twitter', doc_type='tweet',body={"query": {"match_all": {}}}, size=2000)

    data = response['hits']['hits']
    list = []
    for tweet in data:
        try:
            lat = tweet['_source']['coordinates']['coordinates'][1]
            lon = tweet['_source']['coordinates']['coordinates'][0]
            sentiment = tweet['_source']['sentiment']
            tuple = []
            tuple.append(lon)
            tuple.append(lat)
            tuple.append(sentiment)
            list.append(tuple)
        except:
            continue

    return render_template('index.html',data=list)


@socketio.on('message')
def handleMessage(msg):
    print("Message: '"+msg)
    send(msg, broadcast=True)

@socketio.on('json')
def handle_json(json):
    print("Json: '"+str(json))
    send(json, broadcast=True)

api = Api(app)
# api.add_resource(Index, "/", endpoint="index")
api.add_resource(Tweets, "/api/tweets", endpoint="tweets")
api.add_resource(Tweets, "/api/tweets/<string:keyword>", endpoint="keyword")
api.add_resource(Subscription, "/api/subscription", endpoint="subscription")


if __name__ == "__main__":
    #Run on localhost
    # app.run(host='0.0.0.0', debug=True, port=5000)
    #Run on Aws instance
    socketio.run(app,host='0.0.0.0', port=5000, debug=True)