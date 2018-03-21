#!/usr/bin/env python
# encoding: utf-8

Author="Hassan"
Date= "April 29, 2017"

from json import loads
from time import sleep
from geopy.geocoders import Nominatim
from os.path import join, splitext, isfile
from os import listdir
from sys import argv
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def readData(src, list_users):
    """return a set of info given a file
    
    dir -> user_id (str), user_name (str), user_location (str), user_lang (str)"""
    for fileName in listdir(src):
        sys.stdout.write("\r" + "processing with File %s " % fileName)
        sys.stdout.flush()
        path=join(src,fileName)
        if str(fileName) not in list_users:
            with open(path) as f:
                line=f.readline()
                user_id, user_name, user_location, user_lang= extract_user_location(line)
                storeData(user_id, user_name, user_location, user_lang)
        else:
            print('User id found: ' + str(fileName))
                
def extract_user_location(data):
    """This function helps to extract user_timelines_dat
    str -> dict {country: [city....]"""
    print("Extracting user_location")
    try:
        extract=loads(data)
        user_id = str(extract["user"]["id"])
        user_name= str(extract["user"]["name"]) if str(extract["user"]["name"]) else 'Null'
        user_location = str(extract["user"]["location"]) if str(extract["user"]["location"])  else 'Null'
        user_lang= str(extract["user"]["lang"]) if str(extract["user"]["lang"]) else 'Null'
        return user_id, user_name, user_location, user_lang
    except ValueError, e:
        print("Error", e)
        pass
    
def mappedLocationData(loc):
    """return a location using GeoPy
    
    user_location -> country_code, country, city"""
    geolocator = Nominatim()
    country_code, country, city= '', '', ''
    print('Starting to extract countries and cities names...')
    try:
        location= geolocator.geocode(loc,addressdetails=True, timeout=20)
        if location != None:
            user_loc= location.raw['address']
            country_code= user_loc['country_code'] if 'country_code' in user_loc else 'Null'
            if 'country' in user_loc:
                country= str(user_loc['country'])
            else:
                country='Null'
            if 'city' in user_loc:
                city= user_loc['city']
            else:
                city= 'Null'
        sleep(1)
    except :
        pass
    return country_code, country, city

def storeData(Id, name, location, lang):
    "save data to an output file"
    with open(argv[3], mode='a') as file_write:
        country_code, country, city= 'Null', 'Null', 'Null'
        loc=location
        print(loc)
        if loc != ' ' and len(loc.split()) <= 5 and loc != '' and loc != 'Null': 
            country_code, country, city= mappedLocationData(location)
        file_write.write(Id + '\t' + name + '\t' + loc + '\t'+ country_code + '\t' + country + '\t' + city + '\t' + lang + '\n')
        file_write.flush()

def main():
    #loading data, process data, and lastly saving data [user_timelines]
    FileInput = open(argv[1])
    print('Getting list of users ids...')
    list_users=[line.split('\t')[0] for line in FileInput]
        
    print(str(len(list_users)) + ' users ids found...')
    FileInput.close()
    
    print('Starting to extract data...')
    src= argv[2]
    readData(src, list_users_face_output)
    #storeData(user_id, user_name, user_location, user_lang) user_id, user_name, user_location, user_lang= 
    
if __name__=="__main__":
    #called the main function
    main() 

