from flask import Flask, request, render_template
import json
from joblib import load
import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
nltk.download('stopwords')
import os
import pandas as pd
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from joblib import load


MODEL_DIR = os.environ["MODEL_DIR"]
MODEL_FILE = os.environ["MODEL_FILE"]
METADATA_FILE = os.environ["METADATA_FILE"]
MODEL_PATH = os.path.join(MODEL_DIR, MODEL_FILE)
METADATA_PATH = os.path.join(MODEL_DIR, METADATA_FILE)

app = Flask(__name__)
model = load(MODEL_PATH)
data = pd.read_csv("tweets.csv") 

    
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
    return render_template('index.html', inputvalue=inputvalue,rank=rank,scores=scores,tweets=tweets)
    
if __name__ == '__main__':
	app.run(host='0.0.0.0')
    
    





