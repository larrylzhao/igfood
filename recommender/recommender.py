#!/usr/bin/env python
"""
=========================================
Recommender Object
=========================================
Recommender

Usage:
recommender.py [-vdho] <image_under_test> 

Options:
    -h --help                          show this help message
    -v --verbose                       verbose stuff
    -o --output                        where to place output
    -d <path> --dbpath <path>      manually set dbPath, default is colorsetDB.csv
"""
from docopt import docopt
from PIL import Image, ImageDraw
from numpy import array, std, matrix
from scipy.cluster.vq import vq, kmeans, whiten
import csv
import ntpath
import os.path
import random
import database_manipulation

class Recommender:
    """Basic Recommender"""

    def __init__(self, image_under_test="test.png", dbpath="colorsetDB.csv"):
        self.image_under_test = image_under_test
        self.dbpath = dbpath
        self.reader = None
        self.reloadreader()
        self.testList = None

    def reloadreader(self):
        if os.path.isfile(dbpath):
            csvfile = open(self.dbpath, 'r')
            try:
                reader = csv.reader(csvfile)
                print "DB Exists and Loaded CSV Format DB Into a Reader Object at self.reader for {}".format(self)
                return reader
            except:
                print "No DB to Load"
                raise

    def cluster_wholeset(self):
        #Should we move this?
        reader=self.reloadreader()
        print "Pixel Clustering Based Off DB at {}".format(self.dbpath)
        #print self.reader_to_list(reader)
        print array(self.reader_to_list(reader))

    def reader_to_list(self, reader):
        temp_list = []
        for row in reader:
            #print "Reader to List {}".format(row)
            temp_list.append(row)
        return temp_list

    def fetch_data(self):
        print "Fetching Values Stored in DB for Specific {}".format(self.image_under_test)
        reader = self.reloadreader()
        found = False
        for row in reader:
            if self.image_under_test in row : 
                print "Found Image {} in DB".format(self.image_under_test)
                print row
                found = True
                return row
        if found:
            #TODO - Call Colorset.py or Import the Library at this point
            print "Push Colorset Value to the Database First"
            self.push_data()
            raise

    def push_data(self):
        print "Pushing Values Stored in DB for Item {}".format(self.image_under_test)
        print "STILL IN DEVELOPMENT"
        #TODO Make a CSV Writer Object at this point and push the data in Probably better in a different python file.
        return True

#class ItemToItemFiltering(Recommender):
#    def 

def openImage(filename="test.png", verbose=False):
    im = Image.open(filename)
    print "Loading Image {0} ".format(filename)
    if verbose:
        im.show()
    return im

def appendDatabase(colorset, in_filename="test.png", dbPath="./../database/colorsetDB.csv"):
    dataset = colorset
    ##TODO : Check Duplicate
    #add checkDuplicate(dbPath, in_filename) to if statement        
    if os.path.isfile(dbPath):
        print "Appending to database at {}".format(dbPath)
        with open(dbPath, 'a') as databasefile:
            fields=['in_filename', 'colorset_1', 'colorset_2', 'colorset_3']
            writer = csv.DictWriter(databasefile,fieldnames=fields)
            writer.writerow({'in_filename':in_filename, 'colorset_1': dataset[0], 'colorset_2':dataset[1], 'colorset_3':dataset[2]})
    else:
        print "Database does not exist, creating file at {}".format(dbPath)
        with open(dbPath, 'w') as databasefile:
            print "Appending value to database at {0}".format(dbPath)
            fields=['in_filename', 'colorset_1', 'colorset_2', 'colorset_3']
            writer = csv.DictWriter(databasefile,fieldnames=fields)
            writer.writeheader()
            writer.writerow({'in_filename':in_filename, 'colorset_1': dataset[0], 'colorset_2':dataset[1], 'colorset_3':dataset[2]})

if __name__ == '__main__':
    arguments = docopt(__doc__)
    print(arguments)
    image_under_test = arguments['<image_under_test>']
    dbpath = arguments['--dbpath'] or 'colorsetDB.csv'

    recommendation = Recommender(image_under_test, dbpath)
    recommendation.fetch_data()
    recommendation.cluster_wholeset()

    print "Recommendation Input {} and Dataset/DBPath {}".format(recommendation.image_under_test, recommendation.dbpath)

