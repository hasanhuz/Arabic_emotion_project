#!/usr/bin/env python
# encoding: utf-8

author='Hassan'
email='halhuzali@gmail.com'


from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.svm import SVC
from sklearn import cross_validation
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import cross_val_predict
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.linear_model import Perceptron
from sklearn.naive_bayes import MultinomialNB
from sklearn.multiclass import OneVsRestClassifier
from sklearn.metrics import f1_score
from os.path import join, isfile
from os import listdir
from collections import Counter
import numpy as np
import re
import codecs
import sys
reload(sys)
sys.setdefaultencoding('utf8')

def calculateMajorityClass(data):
    counter=Counter(data)
    print(counter)
    print ("Majority Class : " + str((max(counter.values())*100)/sum(counter.values())) + "%")

def vectorize_data(data):
    #process data and extract features as vectors, based on bag of words assumption {norm[l1 = normalized freq, l2 = binary ]}
    vectorizer = HashingVectorizer(decode_error='ignore', non_negative=True, binary=True, norm=None, ngram_range= (1,2), n_features=50000)
    data_vec=vectorizer.fit_transform(data)
    dense = data_vec.todense()
    return dense

def to_table(report):
    "reformat classification report"
    report = report.splitlines()
    res = []
    res.append(['']+report[0].split())
    for row in report[2:-2]:
        res.append(row.split())
    lr = report[-1].split()
    res.append([' '.join(lr[:3])]+lr[3:])
    return np.array(res)

srcName = sys.argv[1]
TRAIN_DIR = srcName + '/train'
TEST_DIR = srcName + '/test'
def main():
    # get information from traning file
    print('Extracting data from training files...')
    train_files = [join(TRAIN_DIR, f) for f in listdir(TRAIN_DIR) if isfile(join(TRAIN_DIR, f))]
    # initialize lists for gold labels and predicted labels
    all_labels = []
    all_pred_labels = []
    # initialize classifier
    print('Initializing ' + str(cls) +'...')
    multi_classes = np.array([0,1,2,3])#,4,5,6, 7])
    # train classifier over "batches" of data
    print('Batch-training classifier...')
    for train_file in train_files:
        print('  Training from ' + train_file + '...')
        # get labels and tweet vectors for batch
        emo_label, tweets = loadTrainData(train_file)
        tweet_vecs = vectorize_data(tweets)
        cls.partial_fit(tweet_vecs, emo_label, classes=multi_classes)
        
    # test classifier
    print('Classifying test set...')
    test_files = [join(TEST_DIR, f) for f in listdir(TEST_DIR) if isfile(join(TEST_DIR, f))]      
    for test_file in test_files:
        print('  Classifying ' + test_file + '...')
        # get labels and tweet vectors for batch
        emo_label, tweets = loadTestData(test_file)
        tweet_vecs = vectorize_data(tweets)
        # partial fit the batch based on specified labels and classes
        all_labels.extend(emo_label)
        all_pred_labels.extend(cls.predict(tweet_vecs))
        
    print('Done.')
    print('')
    
    # get classification results
    print('CLASSIFICATION REPORT')
    calculateMajorityClass(all_labels)
    print('')
    cls_rep= classification_report(all_labels, all_pred_labels)
    tb= to_table(cls_rep)
    dest= open('cls_report.csv', 'a')
    for i in tb:
         i= ','.join(i)
         dest.write(i + '\n')
    dest.write('*****************************' + '\n')
    dest.flush()
    dest.close()
    print('...Done...')
    print('')
    print ("The accuracy score is {:.2%}".format(accuracy_score(all_labels, all_pred_labels)))

if __name__ == "__main__":
    partial_fit_classifiers = {
    'SGD': SGDClassifier(),
    'PT': Perceptron(),
    'NBM': MultinomialNB(),
    'PAC': PassiveAggressiveClassifier()}
    for cls in partial_fit_classifiers.values():
        print('###################################################################')
        print(' ')
        main()
            
