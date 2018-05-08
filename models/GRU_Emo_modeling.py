#!/usr/bin/env python
# -*- coding: utf-8 -*-

author = "Hassan"
Date= "Nov 1st"
Email= "halhuzali@gmail.com"

from collections import Counter
from sklearn.metrics import classification_report
from sys import argvfrom keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.utils.np_utils import to_categorical
from keras.models import Sequential
from keras.optimizers import *
from keras.layers.recurrent import LSTM, GRU
from keras.layers.core import Dense, Activation
from keras.layers.embeddings import Embedding
from keras.layers import Dense, Dropout
from keras import regularizers
import numpy as np
import pandas as pd
import argparse
import re
import h5py
np.random.seed(7)

seeds={}

def norm_alif(text):
    #print(type(text))
    text = text.replace("إ", "ا")  # HAMZA below, with LETTER ALEF
    #text = text.replace(u"\u0621", u"\u0627")  # HAMZA, with LETTER ALEF
    text = text.replace("آ", "ا")  # ALEF WITH MADDA ABOVE, with LETTER ALEF
    text = text.replace("أ", "ا")  # ALEF WITH HAMZA ABOVE, with LETTER ALEF
    return text
    
def removeWordWithOneChar(text):
    l=[w for w in text.split(' ') if len(w)>2]
    return ' '.join(l)
    
def remove_seeds(twt):
    for key in seeds:
        for seed in seeds[key]:
            twt= norm_alif(twt)
            twt= twt.replace(seed, '')    
    return twt

def loadTrainData(filename): #, 'r', errors='ignore', encoding='utf-8' happiness
    emotion = pd.read_csv(filename, sep=',', iterator=True, chunksize=10000, error_bad_lines=False)
    emotion = pd.concat(emotion, ignore_index=True)
    emo_label_map = {"ANGER":0, "ANTICIPATION":1, "DISGUST":2, "FEAR":3, "HAPPINESS":4, "SADNESS":5, "SURPRISE":6, "TRUST":7}
    labels= []
    twts=[]
    emotion=emotion.reset_index(drop=True)
    for i in range(len(emotion)):
        tweet_id=emotion.ix[i, "tweet_id"]
        label=emotion.ix[i, "label"]
        seed=emotion.ix[i, "seed_w"]
        feeling=emotion.ix[i, "feeling_w"]
        twt=emotion.ix[i, "tweet"]
        if not isinstance(twt, str):
            continue
            
        #data_processing
        twt= norm_alif(twt)
        twt= remove_seeds(twt)
        twt= twt.replace(str(seed).strip(), '')
        twt= twt.replace(str(feeling).strip(), '')
        twt= removeWordWithOneChar(twt)
        try:      
            label = emo_label_map[str(label).upper()]
            labels.append(label)
            twts.append(twt)
        except :
            print(label)
            pass
    print(len(labels), len(twts))
    return labels, twts

def tokenizeData(X_train,X_test, vocab):
    "tokenize data"
    #init tokenizer
    tokenizer= Tokenizer(num_words=vocab, filters='\t\n',char_level=False)
    #use tokenizer to split vocab and index them
    tokenizer.fit_on_texts(X_train)
    ##txt to seq
    X_train= tokenizer.texts_to_sequences(X_train)
    X_test = tokenizer.texts_to_sequences(X_test)
    return X_train,X_test

def paddingSequence(X_train,X_test, maxLen=30):
    "padding a sequnace of texts using a given length"
    #######equalize list of seq
    X_train= pad_sequences(X_train, maxLen, padding='post', truncating='post')
    X_test= pad_sequences(X_test, maxLen, padding='post', truncating='post')
    return X_train,X_test

def to_table(report):
    report = report.splitlines()
    res = []
    res.append(['']+report[0].split())
    for row in report[2:-2]:
        res.append(row.split())
    lr = report[-1].split()
    res.append([' '.join(lr[:3])]+lr[3:])
    return np.array(res)

def createModel(X_train,y_train,X_test,y_test, vocab= 50000, batch=128, epoch= 2, nub_nodes= 500, dim_size= 300, max_length = 30):
    "create a sequence model (lstm/gru):"
    model = Sequential()
    model.add(Embedding(input_dim=vocab, output_dim= dim_size, input_length=max_length))
    model.add(GRU(nub_nodes, return_sequences=True))
    model.add(Dropout(0.5))
    model.add(GRU(nub_nodes, return_sequences=True))
    model.add(GRU(nub_nodes))
    model.add(Dense(8))
    model.add(Activation('softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    model.fit(X_train, y_train, epochs=epoch, batch_size=batch, validation_data=(X_test, y_test))
    return model

def main():
    "Main function call"
    #parses:
    parser = argparse.ArgumentParser(description='Modeling GRU')
    parser.add_argument('--train', dest='train', type=str, help='Filename where train data are stored')
    parser.add_argument('--dev', dest='dev', type=str, help='Filename where validation data are stored')
    parser.add_argument('--batch_size', type=int, help='number of data points to process per batch')
    parser.add_argument('--vocab_size', type=int, help='number of vocabulary size')
    parser.add_argument('--epoch', type=int, help='number of epochs')
    parser.add_argument('--nodes', type=int, help='number of nodes')
    args = parser.parse_args()
    
    print('...Loading data...')
    #load training data:
    y_train, X_train= loadTrainData(args.train)
    y_test, X_test= loadTestData(args.dev)
    
    y_train= to_categorical(np.asarray(y_train), num_classes=8)

    #tokenizer
    print('...Tokenizing data...')
    X_train,X_test= tokenizeData(X_train,X_test, args.vocab_size)
    
    #split sequences to the same length
    print('...Sequenece padding...')
    X_train,X_test = paddingSequence(X_train,X_test)
    
    #ceating a model
    print('...Creating the model...')
    model= createModel(X_train,y_train,X_test,to_categorical(np.asarray(y_test),  num_classes=8), args.vocab_size, args.batch_size, args.epoch, args.nodes)
    print(' ')
    
    print('Evaluate the model')
    prediction= model.predict_classes(X_test, batch_size=128)
    cls_rep= classification_report(y_test, prediction)
    tb= to_table(cls_rep)
    dest= open('cls_report_GRU_BID.csv', 'a')
    for i in tb:
         i= ','.join(i)
         dest.write(i + '\n')
    dest.write('*****************************' + '\n')
    dest.flush()
    dest.close()
    print('...Done Evaulation...')
    
if __name__ == "__main__":
    main()
