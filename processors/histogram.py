#!/usr/bin/env python
"""
Input values, output histogram and histogram image
Usage:
histogram.py [-vh] <input_image> 
histogram.py [-vh] <input_image> <input_database>

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
import math
import colorset
from pprint import pprint
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import re

class Analysis:
	"""Actions and Graphing and Generating Results from Input Data"""
	def __init__(self, filename = "test.png"):
		self.filename = filename
		self.original_image = self.openImage(filename)

	def openImage(self, filename="test.png", verbose=False):
		im = Image.open(filename)
		im = im.convert('RGB')
		print "Loading Image {0} ".format(filename)
		if verbose:
			im.show()
		return im 

	def plotHistogram(self, input_array, histogramtitle="Histogram", bins=10):
		#numpy.histogram(input_array, bins)
		plt.figure()
		plt.hist(input_array, bins)
		plt.title(histogramtitle)
		plt.show()

	def plotRGBHistogram(self, datalist, red=True, green=True , blue=True, histogramtitle="RGB Histogram of Overall Dataset", popularity=False,bins=255):
		#numpy.histogram(input_array, bins)
		redList=[]
		greenList=[]
		blueList=[]
		n=0
		for row in datalist:
			#print "row[{}] {}".format(n,row)
			n+=1
			tempList=row
			#print "tempList {}".format(tempList)
			intsonly = re.compile('\d+(?:\.\d+)?')
			#print int(intsonly.findall(tempList[1])[0])
			#print tempList
			redList.append((tempList[0]))
			greenList.append((tempList[1]))
			blueList.append((tempList[2]))
		plt.figure()
		#red_histogram = numpy.histogram(array(redList), bins = 256)
		redList_normalized = self.normalize_histogram(redList)
		greenList_normalized = self.normalize_histogram(greenList)
		blueList_normalized = self.normalize_histogram(blueList)
	
		if red:
			plt.hist(redList, bins = 64, color = 'red', histtype='step')
			plt.hist(redList_normalized, bins = 64, color = 'lightpink', histtype='step')
		if green:
			plt.hist(greenList, bins = 64, color = 'green', histtype='step')
			plt.hist(greenList_normalized, bins = 64, color = 'lightgreen', histtype='step')
		if blue:
			plt.hist(blueList, bins = 64, color = 'blue', histtype='step')
			plt.hist(blueList_normalized, bins = 64, color = 'lightblue', histtype='step')
	
		#plt.plot(red_histogram, color = 'red')
		if popularity:
			plt.title("Popularity Weighted Data" + histogramtitle)
		else:
			plt.title(histogramtitle)
		plt.show()

	def plot_array_histogram(self, datalist, red=True, green=True , blue=True, 
		histogramtitle="RGB Histogram of Overall Dataset", popularity=False,bins=255):

	def plotCSVRGBHistogram(self, datalist, histogramtitle="RGB Histogram of Overall Dataset", popularity=False,bins=64):
		#numpy.histogram(input_array, bins)
		redList=[]
		greenList=[]
		blueList=[]
		n=0
		for row in datalist:
			print "row[{}] {}".format(n,row)
			n+=1
			tempList=row.split()
			#print "tempList {}".format(tempList[0].strip())
			intsonly = re.compile('\d+(?:\.\d+)?')
			print int(intsonly.findall(tempList[1])[0])
			print tempList
			redList.append(int(intsonly.findall(tempList[0])[0]))
			greenList.append(int(intsonly.findall(tempList[1])[0]))
			blueList.append(int(intsonly.findall(tempList[2])[0]))
		#red_histogram = numpy.histogram(array(redList), bins = 256)
		plt.hist(redList, bins = 64, color = 'red', histtype='step')
		plt.hist(greenList, bins = 64, color = 'green', histtype='step')
		plt.hist(blueList, bins = 64, color = 'blue', histtype='step')
	
		#plt.plot(red_histogram, color = 'red')
		if popularity:
			plt.title("Popularity Weighted Data" + histogramtitle)
		else:
			plt.title(histogramtitle)
		plt.show()

	def normalize_histogram(self, datalist, low = 0, high = 255):
		""" Normalize Input List on a range for Histogram usage.
		"""
		print "Normalizing from Low {} to High {}".format(low, high)
		data_min = numpy.amin(datalist)
		data_max = numpy.amax(datalist)
		normalized_list = (datalist - data_min) * high / (high - low)
		print "Pre-existing data_min {} data_max {}".format(data_min, data_max)
		#print "Normalized List {}".format(normalized_list)
		return normalized_list
	
	def normalize_RGB_array(self, input_array, low = 0, high = 255):
		"""Normalize an RGB Array - but only of RGB values, and no positional information"""
		print "Normalizing from Low {} to High {}".format(low, high)
		data_min = numpy.amin(input_array,axis=0)
		data_max = numpy.amax(input_array,axis=0)
		print "Pre-existing data_min {} data_max {}".format(data_min, data_max)
		normalized_list = (input_array - data_min) * high / (high - low)
		#print "Normalized List {}".format(normalized_list)
		return normalized_list
	
	def normalize_PIL_array(self, input_array, normalization_range = ((0, 255), (0, 255), (0, 255))):
		"""normalize_PIL_array - 
		input: numpy Array, RGB Range for Normalization
		output: Array of normalized values
		Normalize an input Array over a range. Probably will only work on image Arrays
		"""
		image_extrema = im.getextrema()
		scalar = numpy.subtract((image_extrema[0],image_extrema[1], image_extrema[2]), normalization_range)
		print "Normalizing from RGB Max and Min Values {}, Extrema {}, Scalar\n {}".format(normalization_range, image_extrema, scalar)
		# Implement Error Checker Later
		# for number in scalar:
		# 	for values in number:
		# 		if values < 0:
		# 			print "Scalar goes into Negative Values"
		# 			raise BaseException
		red, green, blue = input_array[:,:,0], input_array[:,:,1], input_array[:,:,2]
		red = (red - scalar[0][0]) * float(normalization_range[0][1]) / float((image_extrema[0][1] - scalar[0][0]))
		green = (green - scalar[1][0]) * float(normalization_range[1][1])  / float((image_extrema[1][1] - scalar[1][0]))
		blue = (blue - scalar[2][0]) * float(normalization_range[2][1])  / float((image_extrema[2][1] - scalar[2][0]))
		# Have to reassign array since the modifications cause it to no longer be contiguous in memory.
		output_array = numpy.array(input_array).copy()
		output_array[:,:,0] = red
		output_array[:,:,1] = green
		output_array[:,:,2] = blue
		return output_array

	def color_balance_array(self, input_array, targetcolor = (255, 255, 255), 
							saturation_level = .01, normalization_range = (0,255)):
		"""Color Balancing input Image Array
		By converting very dark or very light pixels to White or Black. 
		Overrides allow for conversion to any Strong Color.
			Normalize target color to 0 to 1.0, then set max and lower saturation levels. 
			All pixels past the threshold will be converted.
		255, 255, 255 = White
		0, 0, 0 = Black
		"""
		print "Normalizing Image to Target Color {}".format(targetcolor)
		norm = colors.Normalize(normalization_range[0],normalization_range[1])
		targetcolor = norm(targetcolor)
		normalized_array = norm(input_array)
		red, green, blue = normalized_array.T
		replacement_area = (((red > (targetcolor[0] - saturation_level))
							& (red < (targetcolor[0] + saturation_level))) 
							& ((green > (targetcolor[1] - saturation_level)) 
							& (green < (targetcolor[1] + saturation_level)))
							& ((blue > (targetcolor[2] - saturation_level))
							& (blue < (targetcolor[2] + saturation_level))))
		normalized_array[...][replacement_area.T] = targetcolor
		output_array = numpy.array(input_array).copy() * normalization_range[1]
		return output_array

	def primary_colors(self, targetcolor):
		converter = colors.ColorConverter()
		converter.to_rgb(targetcolor)
		
	
	def loadCSV(self, dbPath):
		with open(dbPath, 'r') as databasefile:
			reader = csv.DictReader(databasefile)
			tempList = []
			for row in reader:	
				print "Appending Values {} {} {}".format(row['colorset_1'], row['colorset_2'], row['colorset_3'])
				tempList.append(row['colorset_1'])
				tempList.append(row['colorset_2'])
				tempList.append(row['colorset_3'])
			tempList = numpy.array(tempList)
			return tempList
	
	def imageToList(self, pix):
		#Input: Pixel Array object, Output: numpy Array
		print "Image Dimensions {0}".format(im.size)
		temp_list = []
		for x in range (0,im.size[0]):
	 		for y in range (0,im.size[1]):
	 			temp_list.append(pix[x,y][0:3])
	 	#print "Picture Access Object converted to RGB list \n{0}".format(pix_array)
	 	return temp_list

if __name__ == '__main__':
	arguments = docopt(__doc__)
	#output_path = arguments['<output>']
	if arguments['<input_database>'] :
		dbPath = arguments['<input_database>']
		datalist = loadCSV(dbPath)
		plotCSVRGBHistogram(datalist, "RGB Histogram of Overall Dataset")
	if arguments['<input_image>'] :
		input_image = arguments['<input_image>']
	verbose = arguments['-v']
	if verbose:
		print(arguments)
	#input is a CSV for now
	a = Analysis()
	im = a.openImage(input_image, verbose) #Open Image
	pix = im.load() # Get the Pixel Access Object
	pix_List = a.imageToList(pix) #Convert Image to List
	pix_array = numpy.asarray(im)
	normalized_array = a.normalize_PIL_array(pix_array)
	#printnormalized_array 
	balanced_normalized_array = a.color_balance_array(normalized_array, (255, 255, 255))
	balanced_normalized_array = a.color_balance_array(balanced_normalized_array, (0, 0, 0))
	new_im = Image.fromarray(balanced_normalized_array)
	new_pix = new_im.load()
	new_pix_List = a.imageToList(new_pix)

	#print pix_array
	#print new_pix
	#new_im = Image.fromarray(numpy.uint8(normalized_array))
	#print new_im
	#plotHistogram(im.histogram(), "Overall Histogram", bins=255)
	im.show()
	new_im.show()
	#print pix_array
	#print "Plotting User Image {}".format(pix_List)
	a.plotRGBHistogram(pix_List, True, False, False, "RGB Histogram of Image {}".format(input_image))
	a.plotRGBHistogram(new_pix_List, True, False, False, "RGB Histogram of Image {}".format(input_image))

	#histogram(input_path)


	#centroid = ([211, 197, 191], [70, 40, 36], [161, 109, 91])
	#plotRGBHistogram(centroid, True, True, True, "RGB Histogram of Centroids of Image {}".format(input_image))
