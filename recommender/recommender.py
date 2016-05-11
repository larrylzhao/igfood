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
import matplotlib.pyplot as plt

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

    def item2item_cosine_filtering_ranges(self):
        temp_dataset = self.dataset.drop(['in_filename', 'colorset_1_r', 'colorset_1_g', 'colorset_1_b', 
                                            'colorset_2_r', 'colorset_2_g', 'colorset_2_b', 
                                            'colorset_3_r', 'colorset_3_g', 'colorset_3_b'], 1) 
        storage_results = pandas.DataFrame(index=temp_dataset.columns, columns=temp_dataset.columns)
        for col_counter in range(0, len(storage_results.columns)):
            for counter in range(0, len(storage_results.columns)):
                storage_results.ix[col_counter, counter] = 1 - cosine(temp_dataset.ix[:,col_counter], temp_dataset.ix[:,counter])

        similarity_results = pandas.DataFrame(index=storage_results.columns, columns=range(0,5))

        for x in range(0, len(storage_results.columns)):
            similarity_results.ix[x,:5] = storage_results.ix[0:,x].order(ascending=False)[:5].index

        print similarity_results.head(5).ix[:5]

    def euclidean_recommender(self):
        """Realtive Distances"""
        print self.dataset.corr()['likes']

    def cluster_wholeset(self):
        #Should we move this?
        print "Pixel Clustering Based Off Kmeans with Likes {}".format(self.dbpath)
        #print self.reader_to_list(reader)
        #for row in self.LearningDict:
        #    print row
        #print self.LearningDict
        print self.dataset
        temp_dataset = self.dataset.drop(['in_filename', 'colorset_1_r', 'colorset_1_g', 'colorset_1_b', 
                                            'colorset_2_r', 'colorset_2_g', 'colorset_2_b', 
                                            'colorset_3_r', 'colorset_3_g', 'colorset_3_b'],1)
        whitened = whiten(temp_dataset)
        centroids = kmeans(whitened,3)[0][1] * std(temp_dataset, 0)
        rounded_centroid = []
        for colors in centroids:
            rounded_color = [int(round(band_value)) for band_value in colors ]
            rounded_centroid.append(rounded_color)
        print "Rounded Centroids at \n{0}".format(rounded_centroid)
        return rounded_centroid

    def reader_to_list(self, reader):
        temp_list = []
        for row in reader:
            #print "Reader to List {}".format(row)
            temp_list.append(row)
        return temp_list

    def range_to_likes(self):
        print self.dataset['red_range_l'] > .01

        temp_dataset = self.dataset
        #model = pandas.ols(y=temp_dataset['red_range_l'], x=temp_dataset.ix[:,['likes']])
        #print model

        #for x in range(0, self.dataset.size() ):
        #    print "Range 2 Likes \n{}".format(self.dataset.ix[x])

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

    def plotHistogram_likes(self, data_array, histogramtitle="Histogram", bins=255):
        #numpy.histogram(input_array, bins)
        plt.figure()
        plt.hist(data_array*self.dataset['likes'], bins)
        plt.title(histogramtitle)
        plt.show()

    def plotHistogram(self, data_array, histogramtitle="Histogram", bins=255):
        #numpy.histogram(input_array, bins)
        plt.figure()
        plt.hist(data_array*self.dataset['likes'], bins)
        plt.title(histogramtitle)
        plt.show()

    def plotHistograms(self):
        self.plotHistogram_likes(self.dataset['red_range_l'], "red_range_l_scaled_likes", 50)
        self.plotHistogram_likes(self.dataset['red_range_h'], "red_range_h_scaled_likes", 50)
        self.plotHistogram_likes(self.dataset['green_range_l'], "green_range_l_scaled_likes", 50)
        self.plotHistogram_likes(self.dataset['green_range_h'], "green_range_h_scaled_likes", 50)
        self.plotHistogram_likes(self.dataset['blue_range_l'], "blue_range_l_scaled_likes", 50)
        self.plotHistogram_likes(self.dataset['blue_range_h'], "blue_range_l_scaled_likes", 50)

        self.plotHistogram(self.dataset['red_range_l'], "red_range_l_scaled_", 50)
        self.plotHistogram(self.dataset['red_range_h'], "red_range_h_scaled_", 50)
        self.plotHistogram(self.dataset['green_range_l'], "green_range_l_scaled", 50)
        self.plotHistogram(self.dataset['green_range_h'], "green_range_h_scaled", 50)
        self.plotHistogram(self.dataset['blue_range_l'], "blue_range_l_scaled", 50)
        self.plotHistogram(self.dataset['blue_range_h'], "blue_range_l_scaled", 50)

if __name__ == '__main__':
    arguments = docopt(__doc__)
    print(arguments)
    image_under_test = arguments['<image_under_test>']
    dbpath = arguments['--dbpath'] or 'test.csv'

    recommendation = Recommender(dbpath)
    #print recommendation.dataset.head()
    recommendation.item2item_cosine_filtering()
    recommendation.item2item_cosine_filtering_ranges()
    #recommendation.dataset.describe()
    recommendation.dataset.corr()['likes']
    #recommendation.cluster_wholeset()
    recommendation.euclidean_recommender()
    recommendation.range_to_likes()
    recommendation.plotHistograms()


