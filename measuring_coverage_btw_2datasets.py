#!/usr/bin/env python
# -*- coding: utf-8 -*-

author='Hassan'
date='Feb 15, 2018'
email='halhuzali@gmail.com'

from sys import argv
import re
from collections import defaultdict
import pandas as pd

def loadTrainData(in_p):
    "return a list of tweets"
    list_tweets=[]
    emotion = pd.read_csv(in_p, sep='\t', iterator=True, chunksize=100000, error_bad_lines=False)#, header=0)
    emotion = pd.concat(emotion, ignore_index=True)
    emotion=emotion.reset_index(drop=True)
    for i in range(len(emotion)):
        message=emotion.ix[i, "message"]
        list_tweets.append(message)
    print(len(list_tweets))
    return list_tweets

def get_dict(data):
    "return a dict of words and their freqs given a list of tweets"
    word_space=defaultdict(int)
    for twt in data:
        for word in twt.split():
            word_space[word]=len(word_space)
    return word_space

def filter_words_given_threshold(dic, threshold=10):
    "return a dict where counts of keys should satsifiy a given threshold (default is 10)"
    d={word:count for word, count in dic.items() if count >= threshold}
    return d
            
def get_coverage(train,dev):
    """return % and # of word coverage in one dev/test dataset against a given train dataset
    
    train, dev/test -> coverage (#), coverage (%)"""
    
    D1_dict=filter_words_given_threshold(get_dict(train), 10)
    print(str(len(D1_dict)) + ' train_dict')
    D2_dict=filter_words_given_threshold(get_dict(dev), 10)
    print(str(len(D2_dict)) + ' dev_dict')
    
    coverage=set(D1_dict.keys()).intersection(D2_dict.keys())
    #length_of_coverage= len(D2_dict.keys()) - len(coverage) 
    percentage= len(coverage) / float(len(D2_dict.keys())) * 100
    
    print('The percentage of coverage ' + str(int(percentage)) + '%')
    print('The number of coverage ' + str(len(coverage)))
    return len(coverage), int(percentage)
    

def reformatOutput(number, percentage, dataset1_name, dataset2_name):
    "refromat output values such that we get a column named by dataset1 and a row named by using dataset2"
    with open('results.csv', 'a') as f:
        f.write('' + ',' + dataset1_name.split('.')[1].replace('EmoNet2017_final_loc/','') + ', ' + '' + '\n')
        f.write('' + ',' + '#' + ', ' + '%' + '\n')
        f.write(dataset2_name.split('.')[0].replace('norm_semEval_data','') + ' ,' + str(number) + ', '+str(percentage) + '\n')
        
def main():
    "call functions"
    d1= argv[1]
    train=loadTrainData(d1)
    d2= argv[2]
    dev= loadTrainData(d2)
    number_of_coverage, perc_of_coverage= get_coverage(train,dev)
    reformatOutput(number_of_coverage, perc_of_coverage, d1, d2)
    
if __name__=="__main__":
    #called the main function
    main()
