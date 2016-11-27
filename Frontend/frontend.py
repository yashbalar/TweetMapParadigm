#!/usr/bin/env python3
from flask import Flask

from flask import render_template,request

from requests import get,post

app = Flask(__name__)
#
# es = Elasticsearch(
#     ['localhost:9200'],
#     connection_class=RequestsHttpConnection
# )

@app.route('/')
def index():
        data = get("http://54.197.18.228:5000/api/tweets")
        return render_template('index.html',data=data.json())

@app.route('/',methods=['POST'])
def search():
    try:
        searchtext = request.form['TrendKeyword']
        url = "http://54.197.18.228:5000/api/tweets/"+searchtext
        data = get(url)
        return render_template('index.html', data=data.json())
    except Exception:
        print (Exception.message)



if __name__ == "__main__":
    #Run on localhost
    app.run(host='0.0.0.0', debug=True, port=5001)
    #Run on Aws instance
    # app.run(host='0.0.0.0', debug=True, port=5000)
