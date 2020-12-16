from flask import Flask, request, render_template
import json
from joblib import load
import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
nltk.download('stopwords')
import os
import time
import random
import pandas as pd
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from joblib import load

from prometheus_client import start_http_server
from prometheus_client import Counter, Gauge, Summary, Histogram


MODEL_DIR = os.environ["MODEL_DIR"]
MODEL_FILE = os.environ["MODEL_FILE"]
METADATA_FILE = os.environ["METADATA_FILE"]
MODEL_PATH = os.path.join(MODEL_DIR, MODEL_FILE)
METADATA_PATH = os.path.join(MODEL_DIR, METADATA_FILE)

app = Flask(__name__)
model = load(MODEL_PATH)
data = pd.read_csv("tweets.csv") 

REQUESTS =Counter('twitter_search_app_calls_total', 'How many times the app was called')
EXCEPTIONS =Counter('twitter_search_app_exceptions_total', 'How many exceptions the app triggers')
INPROGRESS = Gauge('twitter_search_app_inprogress', 'number of requests in progress')
LAST = Gauge('twitter_search_app_times_seconds', 'the last time our app was called')
LATENCY_SUM = Summary('twitter_search_app_latency_sum_seconds', 'the time needed for a request')
LATENCY_HIS = Histogram('twitter_search_app_latency_his_seconds', 'the time needed for a request')

    
#function for tweet data preprocessing
def text_clean(text):
    #create word tokens as well as remove punctuation 
    rem_tok_punc= RegexpTokenizer(r'\w+')
    tokens = rem_tok_punc.tokenize(text)
    #convert the words to lower case
    words = [w.lower() for w in tokens]
    #involke all the english stopwords
    stop_word_list = set(stopwords.words('english'))
    #remove stops words
    words = [w for w in words if not w in stop_word_list]
    return words   

     

    
@app.route('/', methods=['GET','POST'])
def index():
    LAST.set(time.time())
    REQUESTS.inc()
    start = time.time()
    rand = random.random()
    #with EXCEPTIONS.count_exceptions():
    #     if rand < 0.2:
    #         raise Exception
             
    INPROGRESS.inc()
    #time.sleep(5)
    if rand < 0.5:
        time.sleep(rand * 0.1)
        
        
    scores = []
    tweets = []
    rank = [*range(1, 21, 1)]
    inputvalue=''
    if request.method == 'POST':
        enter = request.form['search']  # take the user input string
        inputvalue=enter
        test_doc = text_clean(enter)  # preprocess the user input
        test_doc_vector = model.infer_vector(test_doc)  # infer a vector representation for this user input
        # call the model for getting the 20 most similar tweet
        similar_doc = model.docvecs.most_similar(positive=[test_doc_vector], topn=20)
        # ID of the top similar tweets
        first_tuple_elements = [a_tuple[0] for a_tuple in similar_doc]
        # The top 20 most score
        scores = [a_tuple[1] for a_tuple in similar_doc]
        # the top 20 most similar tweets
        tweets = [data['text'][i] for i in first_tuple_elements]
        
    INPROGRESS.dec()
    last = time.time()
    LATENCY_SUM.observe(last - start)
    LATENCY_HIS.observe(last - start)
    
    return render_template('index.html', inputvalue=inputvalue,rank=rank,scores=scores,tweets=tweets)
    
if __name__ == '__main__':
    start_http_server(8000)
    app.run(host='0.0.0.0')
    
    





