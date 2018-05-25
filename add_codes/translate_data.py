#!/usr/bin/env python
# encoding: utf-8
author='Hassan'

from sys import argv
from textblob import TextBlob
import csv


def trans_sent(message, lang_tag= "ar"):
    """translate a message using Google Api, default lang is Arabic
    
    message(str), [lang(str)] -> None"""
    with open(argv[1], 'ab') as f_w:
        writer = csv.writer(f_w, delimiter = ',', quoting=csv.QUOTE_ALL)
        try:
            trans_message= TextBlob(message).translate(to= lang_tag)
            writer.writerow((message, trans_message))
        except :
            pass
    print('...Done...')
        
print('Translating begin')
trans_sent(message)
