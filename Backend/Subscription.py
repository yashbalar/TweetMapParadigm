from flask import jsonify, url_for, redirect, request
from flask_restful import Resource
from flask import render_template,request
import json
import boto.sns
from requests import get,post
import threading
#Custome Imports
from Backend.Config import *
from StreamTweet.streamTweet import keywords


class Subscription(Resource):

    def get(self,keyword=None):
        data = request
        pass

    def post(self):
        data=request.data
        t = threading.Thread(target=indexTweet, args=(data,))
        t.setDaemon(True)
        t.start()




def indexTweet(data):
    data = data.decode('utf-8')
    json_data = json.loads(data)
    if json_data['Type'] == 'Notification':
        print("Notification received...")
        tweet = json_data['Message']
        post("http://127.0.0.1:5000/api/tweets", json=tweet)
        return

    # If it is not notification, consider it as subscription confirmation
    print(data)
    conn = boto.sns.connect_to_region("us-east-1",aws_access_key_id='ACCESSKEY',aws_secret_access_key='SECRETKEY')
    resp = conn.confirm_subscription(data['TopicArn'], data['Token'])
    print("Subscription Response: " + str(resp))

