import tweepy
from tweepy.streaming import StreamListener
from tweepy import Stream
import time
from flask import Flask,render_template,request
import json
import jinja2
import boto.sqs
from boto.sqs.message import RawMessage



_CONSUMER_KEY = 'CONSUMERKEY'
_CONSUMER_SEC_KEY = 'CONSUMERSECRETKEY'
_ACCESS_TOKEN = 'ACCESSTOKEN'
_ACCESS_TOKEN_SECRET = 'ACCESSTOKENSECRET'

#Reference: http://docs.tweepy.org/en/v3.4.0/streaming_how_to.html

class StdOutListener(StreamListener):
    def on_data(self, data):
        if data != None:
            tweet = json.loads(data)
            if 'contributors' in tweet and tweet['coordinates'] is not None and tweet['lang'] == 'en':
                if tweet['coordinates']['type'] == 'Point':
                    #print(tweet)
                    newtweet = {}
                    newtweet['text'] = tweet['text']
                    newtweet['coordinates'] = tweet['coordinates']
                    json_tweet = json.dumps(newtweet)

                    #writing tweet to sqs
                    time.sleep(1)
                    sqs.addMessageToQueue(json_tweet)
                    return True

    def on_error(self, status_code):
        print(status_code)
        #API CALL limit
        if status_code == 420:
            # returning False in on_data disconnects the stream
            return False

    def on_exception(self, exception):
        """Called when an unhandled exception occurs."""
        print(exception)
        return

class SimpleQueueService:
    q = None

    def createQueue(self):
        conn = boto.sqs.connect_to_region("us-east-1",aws_access_key_id='ACCESSKEY',aws_secret_access_key='SECRETKEY')
        self.q = conn.create_queue('myqueue')

    def addMessageToQueue(self,json_msg):
        m = RawMessage()
        m.set_body(json.dumps(json_msg))
        self.q.write(m)

application = Flask(__name__)
app = application

#Elasticsearch##


#SETUP SQS
sqs = SimpleQueueService()
sqs.createQueue()

##Keywords ##
keywords = ['Vote', 'Cricket', 'Instagram', 'TGIF', 'TheWalkingDead', 'pizza', 'Snapchat',
                    'Hillary', 'Food', 'Trump']
## Starting a Stream##
l = StdOutListener()
auth = tweepy.OAuthHandler(_CONSUMER_KEY, _CONSUMER_SEC_KEY)
auth.set_access_token(_ACCESS_TOKEN, _ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

stream = Stream(auth, l)
stream.filter(track=keywords, async=True)


if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0',port=5004,debug=True)
    except Exception:
        print (Exception.message)
