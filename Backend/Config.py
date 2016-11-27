from flask import Flask
from elasticsearch import Elasticsearch, RequestsHttpConnection
from flask_socketio import SocketIO, send



# es = Elasticsearch(
#     ['localhost:9200'],
#     connection_class=RequestsHttpConnection
# )


es = Elasticsearch(
    ['https://search-twittmapvivekghatala-lf7exg22nxsy6tbfynxpy3oowy.us-east-1.es.amazonaws.com/'],
    connection_class=RequestsHttpConnection
)
app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
app.config['threaded'] = True
socketio = SocketIO(app)