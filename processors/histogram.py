#!/usr/bin/env python
"""
Input values, output histogram and histogram image
Usage:
histogram.py [-vh] <input> <output>

Options:
	-h --help                          show this help message
	-v --verbose                       show input and output image
"""
from docopt import docopt
from PIL import Image, ImageDraw
from numpy import array, std
from scipy.cluster.vq import vq, kmeans, whiten
import csv
import ntpath
import os.path
import colorset
import json
import numpy
from pprint import pprint
import matplotlib.pyplot as plt

def plotHistogram(histogramtitle="Histogram",input_array, bins=10):
	#numpy.histogram(input_array, bins)
	plt.figure()
	plt.hist(input_array, bins = 'auto')
	plt.title(histogramtitle)
	plt.show()

def plotRGBHistogram(histogramtitle="Histogram", color, input_array, bins=10):
	#numpy.histogram(input_array, bins)

	
	plt.figure()
	plt.hist(input_array, bins = '32')
	plt.title(histogramtitle)
	plt.show()

def loadCSV(dbPath):
	with open(dbPath, 'r') as databasefile:
		reader = csv.DictReader(databasefile)
		tempList = []
		for row in reader:	
			print("Appending Values {} {} {}".format(row['colorset_1'], row['colorset_2'], row['colorset_3']))
			tempList.append(row['colorset_1'])
			tempList.append(row['colorset_2'])
			tempList.append(row['colorset_3'])
		dataArray = numpy.array(tempList)
		return dataArray

if __name__ == '__main__':
	arguments = docopt(__doc__)
	#output_path = arguments['<output>']
	dbPath = arguments['<input>']
	verbose = arguments['-v']
	if verbose:
		print(arguments)
	#input is a CSV for now
	dataArray = loadCSV(dbPath)
	plotRGBHistogram(dataArray)
	#histogram(input_path)
