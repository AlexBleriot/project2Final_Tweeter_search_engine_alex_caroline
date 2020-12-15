import pandas as pd
import numpy as np
import string
import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
import os
import pandas as pd
from joblib import dump
import json
from gensim.models.doc2vec import Doc2Vec, TaggedDocument

nltk.download('stopwords')

# load dataset
data = pd.read_csv('tweets.csv', encoding='utf-8')

# information regarding the model
MODEL_DIR = os.environ["MODEL_DIR"]
MODEL_FILE = os.environ["MODEL_FILE"]
METADATA_FILE = os.environ["METADATA_FILE"]
MODEL_PATH = os.path.join(MODEL_DIR, MODEL_FILE)
METADATA_PATH = os.path.join(MODEL_DIR, METADATA_FILE)

indv_lines = data['text'].values.tolist()


# function for tweet data preprocessing
def text_clean(text):
    # create word tokens as well as remove punctuation
    rem_tok_punc = RegexpTokenizer(r'\w+')
    tokens = rem_tok_punc.tokenize(text)
    # convert the words to lower case
    words = [w.lower() for w in tokens]
    # involke all the english stopwords
    stop_word_list = set(stopwords.words('english'))
    # remove stops words
    words = [w for w in words if not w in stop_word_list]
    return words


# create empty list
tweet_data_list = list()
for line in indv_lines:
    tweet_data_list.append(text_clean(line))  # preprocess each tweet and save it inside the tweet_data_list

# Training Doc2Vec model

tagged_data = [TaggedDocument(d, [i]) for i, d in enumerate(tweet_data_list)]  # associate tag to each cleaned tweet

print("-------------------------- Start Training of the  doc2vec model ----------------------------------")
print(".......")
model = Doc2Vec(tagged_data, vector_size=100, window=2, min_count=1, epochs=100)
print("-------------------------------- doc2vec model trained --------------------------------------------")

# saving model into a global variable
print("Serializing model to: {}".format(MODEL_PATH))
dump(model, MODEL_PATH)





