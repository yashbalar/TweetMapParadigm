import sys
sys.path.append("/home/ec2-user/TweetMapParadigm")

from flask import Flask,render_template,request
import json
import jinja2
import boto.sns
import boto.sqs
from boto.sqs.message import RawMessage
import threading
from ProcessTweets.alchemyapi import AlchemyAPI
# import nltk
# nltk.download()
#from nltk.corpus import stopwords
#from nltk.tokenize import word_tokenize
#from nltk.stem import PorterStemmer
import re
import string
#from html.parser import HTMLParser
#from HTMLParser import HTMLParser

import urllib3

# alchemy_apikey='3a56ce0d1bb9106ae225e5d1203e3a52b980379b'

class SentimentAnalyzer:
    alchemyapi = None
    #html_parser = None
    #stop_words = set(stopwords.words('english'))
    ps = None

    def __init__(self):
        self.alchemyapi = AlchemyAPI()
        #self.html_parser = HTMLParser()
        #self.ps = PorterStemmer()

    def preProcess(self,tweet_text):
        text = tweet_text.encode('ascii', 'ignore').decode("utf-8")
        text = re.sub(r"http\S+", "", text)
        # Remove Punctuations
        text = re.sub(r"@\w+", "", text)
        text = re.sub(r"#\w+", "", text)
        text = text.lower()
        text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
        text = re.sub(r"\n", "", text)
        # word_tokens = word_tokenize(text)
        # filtered_words = [w for w in word_tokens if not w in self.stop_words]
        # stemmed_words = [self.ps.stem(w) for w in filtered_words]
        # clean_text = " ".join(stemmed_words)
        return text

    def getSentiment(self,tweet_text):
        clean_text = self.preProcess(tweet_text)
        response = self.alchemyapi.sentiment("text", clean_text)

        if response['status'] == 'OK':
            sentiment = response['docSentiment']['type']
        else:
            print("Error fetching Sentiment: "+ tweet_text)
            sentiment = "unknown"
        return sentiment

class Publisher:
    conn = None
    topicARN = None

    def __init__(self):
        self.conn = boto.sns.connect_to_region("us-east-1",aws_access_key_id='ACCESSKEY',aws_secret_access_key='SECRETKEY')
        sns = self.conn.create_topic('test')
        self.topicARN = sns['CreateTopicResponse']['CreateTopicResult']['TopicArn']
        # self.conn.subscribe(self.topicARN, 'http', 'http://54.197.18.228:5000/api/subscription')

    def publish(self,msg):
        self.conn.publish(topic=self.topicARN, message=msg)


class SimpleQueueService:
    q = None

    def getQueue(self):
        conn = boto.sqs.connect_to_region("us-east-1",aws_access_key_id='ACCESSKE',aws_secret_access_key='SECRETKEY')
        self.q = conn.get_queue('myqueue')
        self.q.set_message_class(RawMessage)
        return

    def readMessage(self):
        msg = self.q.get_messages()
        if len(msg):
            return msg

class ProcessTweet:
    sqs = None
    analyzer = None
    publisher = None

    def __init__(self):
        self.sqs = SimpleQueueService()
        self.sqs.getQueue()
        self.analyzer = SentimentAnalyzer()
        self.publisher = Publisher()

    def getMessageFromQueue(self):
        msglist = self.sqs.readMessage()
        if msglist is not None:
            for msg in msglist:
                if msg:
                    t = threading.Thread(target=self.processTweet, args=(msg,))
                    t.setDaemon(True)
                    t.start()
                    #self.processTweet(msg)



    def processTweet(self,msg):
        #two json.loads to strip extra // characters and to form correct json
        try:
            #print(msg.get_body())
            tweet = json.loads(json.loads(msg.get_body()))
            print('tweet')
            sentiment = self.analyzer.getSentiment(tweet['text'])
            tweet['sentiment'] = sentiment
            print(sentiment)
            tweet = json.dumps(tweet)
            self.publisher.publish(tweet)
            self.sqs.q.delete_message(msg)

        except Exception as  e:
            print("Error processing tweet. Tweet not deleted.")
            print(e.msg)



instance = ProcessTweet()

while(instance.sqs.q.count()):
    instance.getMessageFromQueue()

app = Flask(__name__)

sqs = SimpleQueueService()
sqs.getQueue()
sqs.readMessage()

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0',port=5003,debug=True)
    except Exception:
        print (Exception.message)
