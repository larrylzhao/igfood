#!/usr/bin/env python
"""
=========================================
Recommender Object
=========================================
Recommender
Ideal Values to Generate: 
Overall Colorset: Primary and secondary
Saturation Levels to be used for Color Balancing
Range for normalization for Color Balancing
Number of Centroids used on a photo

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
from scipy.spatial.distance import cosine
import csv
import ntpath
import os.path
import random
import json
import pandas

class Recommender:
    """Basic Recommender"""

    def __init__(self, dbpath="test.csv"):
        self.dbpath = dbpath
        self.LearningDict = self.reloadreader()
        self.dataset = pandas.read_csv(dbpath)

    def reloadreader(self):
        if os.path.isfile(dbpath):
            with open(self.dbpath, 'r') as csvfile:
                print "DB Exists and Loaded CSV Format DB Into a Reader Object at self.reader for {}".format(self)
                reader = (csv.DictReader(csvfile))
                outputDict = list(csv.DictReader(csvfile))
                #for row in reader:
                #    print row
                return outputDict
        else:
            print "No DB to Load"
            raise

    def item2item_cosine_filtering(self):
        """cosine similarity filter thru colorset + likes
        """
        temp_dataset = self.dataset.drop(['in_filename', 'red_range_l', 'red_range_h', 'green_range_l', 'green_range_h', 'blue_range_l', 'blue_range_h'], 1) 
        storage_results = pandas.DataFrame(index=temp_dataset.columns, columns=temp_dataset.columns)
        for col_counter in range(0, len(storage_results.columns)):
            for counter in range(0, len(storage_results.columns)):
                storage_results.ix[col_counter, counter] = 1 - cosine(temp_dataset.ix[:,col_counter], temp_dataset.ix[:,counter])

        similarity_results = pandas.DataFrame(index=storage_results.columns, columns=range(0,10))

        for x in range(0, len(storage_results.columns)):
            similarity_results.ix[x,:10] = storage_results.ix[0:,x].order(ascending=False)[:10].index

        print similarity_results.head(10).ix[:10]



    def cluster_wholeset(self):
        #Should we move this?
        print "Pixel Clustering Based Off DB at {}".format(self.dbpath)
        #print self.reader_to_list(reader)
        #for row in self.LearningDict:
        #    print row
        #print self.LearningDict

    def reader_to_list(self, reader):
        temp_list = []
        for row in reader:
            #print "Reader to List {}".format(row)
            temp_list.append(row)
        return temp_list

    # def fetch_data(self):
    #     print "Fetching Values Stored in DB for Specific {}".format(self.image_under_test)
    #     reader = self.reloadreader()
    #     found = False
    #     for row in reader:
    #         if self.image_under_test in row : 
    #             print "Found Image {} in DB".format(self.image_under_test)
    #             print row
    #             found = True
    #             return row
    #     if found:
    #         #TODO - Call Colorset.py or Import the Library at this point
    #         print "Push Colorset Value to the Database First"
    #         self.push_data()
    #         raise


if __name__ == '__main__':
    arguments = docopt(__doc__)
    print(arguments)
    image_under_test = arguments['<image_under_test>']
    dbpath = arguments['--dbpath'] or 'test.csv'

    recommendation = Recommender(dbpath)
    #print recommendation.dataset.head()
    recommendation.item2item_cosine_filtering()
    recommendation.cluster_wholeset()


