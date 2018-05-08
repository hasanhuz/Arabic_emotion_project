#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd
import csv
import sys

in_p=sys.argv[1]
out_p=open(sys.argv[2], 'wb') 
#-----------------------------------------------------------------
writer = csv.writer(out_p,delimiter = ',', quoting=csv.QUOTE_ALL)
writer.writerow(('user_id','tweet_id','emoji','emo_label','sent_label','tweet'))

def drop_duplicate_messages(in_p, out_p):
    "This function helps to drop duplicate using pandas and then store data into output file"
    
    emotion = pd.read_csv(in_p, iterator=True, chunksize=100000, delimiter=',', header=0)
    emotion = pd.concat(emotion, ignore_index=True)
    emotion.columns =  ['tweet_id','emoji','emo_label','tweet']
    #message must named "tweet", otherwise change below field
    emotion=emotion.drop_duplicates(subset=["tweet"], keep=False)
    emotion=emotion.reset_index(drop=True)
    for i in range(len(emotion)):
        user_id=emotion.ix[i,"user_id"]
        tweet_id=emotion.ix[i, "tweet_id"]
        emoji=emotion.ix[i, "emoji"]
        emo_label=emotion.ix[i, "emo_label"]
        senti_label=emotion.ix[i, 'sent_label']
        tweet=emotion.ix[i, "tweet"]
        writer.writerow((user_id, tweet_id, emoji, emo_label, senti_label, tweet))

drop_duplicate_messages(in_p, out_p)
