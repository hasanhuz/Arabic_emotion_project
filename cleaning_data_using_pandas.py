author='Hassan'
date='Feb, 2018'
email='halhuzali@gmail.com'

import pandas as pd
import numpy as np
import sys  
import json 
import csv

#loading data using pandas
df=pd.read_csv("path", iterator=True, chunksize=100000, sep=',', error_bad_lines=False)
df = pd.concat(df, ignore_index=True)
df.columns= ['user_id','tweet_id','location','name','tweet']

#pipline for cleaning text using pandas
#filter non-Arabic chars, convert @name to "<USER>", conver http to "<URL>", keep a tweet with more than 5 words at min
df['tweet'].replace(to_replace="[~A-Za-z0-9]+", value=r" ", regex=True, inplace=True)
df['tweet'].replace(to_replace="@[^\s]+", value=r"<USER>", regex=True, inplace=True)
df['tweet'].replace(to_replace="http[^\s]+", value=r"<URL>", regex=True, inplace=True)
df['tweet'].replace(to_replace="\s+", value=r" ", regex=True, inplace=True)
df = df[df.tweet.str.split().str.len() >= 5]
df['tweet']= df.tweet.map(str.strip)

################################################
#clean data given some set of rules
target objective language, religious content, quotations #:/-, adult, 
list_seeds= ['سبحان الله', 'الله أكبر', 'اللهم', 'بسم الله', 'يا رب', 'العضيم','سبحان','يارب','قران','quran','قولون عصب','قال','إذا','-','الدراسات',' - ','فرق','"',' " '
             'حديث','hadith', 'صلاه_الفجر','﴾','ﷺ', 'صحيح البخاري','صحيح مسلم','يآرب', 'سورة','زوجتك','انثئ','…','رب',':','الرسول','صلى','الله','عليه','وسلم']
pattern= '|'.join(list_seeds)
df= df[~df.tweet.str.contains(pattern)]

##############################################
#remove tweet that have more than 5 diac
diac = ['لَأ', 'فّّ', 'ةّ', 'هِ', 'تْ', 'هُ', 'زَ', 'يّ', 'نُ', 'ُ','ْ','َ','ِ','ّ','ً','ٍ','ٌ','لإ','أ','آ', 'ۓ']
pt2= '|'.join(diac)
df= df[df.tweet.str.count(pt2) <= 5]

##############################################
#split: train (80%), dev (10%), and test (10%)
train, val, test = np.split(df_emo, [int(.8 * len(df)), int(.9 * len(df))])
print(len(train), len(val), len(test))

#save df to an output file
df.to_csv('path', sep=',', index=False)
