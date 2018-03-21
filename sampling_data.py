#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import csv
from sys import argv
import sys
import numpy as np
##############################################################
##This function helps to sample data by specifing a set of labels as arguments..
##usage:
## python sampling_data.py filename <where data is stored> filename <where data will be saved>
##############################################################

def randomize_df(df):
    "return a randomized dataframe"
    df=df.loc[np.random.permutation(df.index)]
    return df

def sampling_data(label1='positive', label2='negative', N_samples=100000):
    """sample data of a given label based on 4 conditions and then save sampled data in an output file
    1. final_loc = 'final': meaning hashtag occurrs at the end of a tweet
    2. lang_id = 'en'
    3. label = positive|negative
    4. length of a tweet should be bigger than 4
    str, str, int -> None"""
    emotion = pd.read_csv(argv[1], iterator=True, chunksize=100000, delimiter=',', header=0)
    emotion = pd.concat(emotion, ignore_index=True)
    emotion.columns=["message_id","message","label","sent","lang_id","final_loc"]
    
    #pos_sampling
    pos_label= emotion[(emotion.final_loc=="final") & (emotion.lang_id=='en') & (emotion.sent==label1) & (emotion.message.str.split().str.len() >= 5)]
    pos_sample=  pos_label.sample(n= N_samples, replace=True)
    
    #neg sampling
    neg_label= emotion[(emotion.final_loc=="final") & (emotion.lang_id=='en') & (emotion.sent==label2) & (emotion.message.str.split().str.len() >= 5)]
    neg_sample=  neg_label.sample(n= N_samples, replace=True)
    
    #concat_data
    df=pd.concat([pos_sample,neg_sample])
    
    ###print length
    print(len(pos_sample))
    print(len(neg_sample))
    print(len(df))
    
    #randmize data
    df= randomize_df(df)
    
    #save df into an output file
    df.to_csv(argv[2],sep=',',index=False,columns=['message_id','message','sent'], quoting=csv.QUOTE_ALL)

sampling_data()
