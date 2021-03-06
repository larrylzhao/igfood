#!/usr/bin/env python
"""
End all be all
Input values, output histogram and histogram image
Usage:
igFood.py [-vhl] <input_image> 
igFood.py [-vhl] <input_image> <output_path>
igFood.py [-vhl] <input_image> --database=<dbPath>

Options:
	-h --help							show this help message
	-v --verbose						show input and output image
	-l --learning 						enable storing of values
"""
from docopt import docopt
from PIL import Image, ImageDraw
from numpy import array, std
from scipy.cluster.vq import vq, kmeans, whiten
import csv
import ntpath
import os.path
import json
import numpy
import math
from pprint import pprint
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import re

def image2_flat_array(pix, im):
	"""Input: Pixel Array object and Image Object
	Output: Flat Numpy Array
	This function needs to be changed to not be flat. 
	Keeping it around for Legacy calls that I haven't fixed yet"""
	#print "Image Dimensions {0}".format(im.size)
	temp_list = []
	for x in range (0,im.size[0]):
		for y in range (0,im.size[1]):
			temp_list.append(pix[x,y][0:3])
	pix_array = array(temp_list)
	#print "Picture Access Object converted to RGB numpy Array \n{0}".format(pix_array)
	return pix_array

def image2_list(pix, im):
		#Input: Pixel Array object, Output: numpy Array
		print "Image Dimensions {0}".format(im.size)
		temp_list = []
		for x in range (0,im.size[0]):
	 		for y in range (0,im.size[1]):
	 			temp_list.append(pix[x,y][0:3])
	 	#print "Picture Access Object converted to RGB list \n{0}".format(pix_array)
	 	return temp_list

def check_duplicate(dbPath, in_filename):
	"""check for duplicates in database"""
	if os.path.isfile(dbPath):
		print "Checking for duplicates in {}".format(dbPath)
		databasefile = csv.reader(open(dbPath, 'rb'))
		for row in databasefile:
			if row[0] == in_filename:
				return True
	else:
		return False

class igFood(object):
	"""igFood Base Class"""
	def __init__(self, filepath = "test.png", verbose = False):
		self.filepath = filepath
		self.filename = ntpath.basename(filepath)
		self.im = Image.open(filepath).convert('RGB')
		self.pix = self.im.load()
		self.pix_array = image2_flat_array(self.pix, self.im)
		self.pix_asarray = numpy.asarray(self.im)

	def get_image():
		"""Get PIL.Image Object"""
		return self.im

	def get_pix():
		return self.pix	

	def get_pix_array():
		return self.pix_array

	def get_rgb_visualization(self, rgb_sets, verbose=False, x=600, y=100):
		"""Generate RGB Visualization of input rgb_sets
		Input : RGB Values 
		Output : Image of the RGB values"""
		colorset_im = Image.new("RGB", (x, y))
		im_draw = ImageDraw.Draw(colorset_im)
		colorset_size = len(rgb_sets)
		x_temp = x / colorset_size
		x_old = 0
		for colors in rgb_sets:
			#rounded_color = [int(round(band_value)) for band_value in colors ]
			print "Filling Polygon in from {0} to {1} with color {2}".format(x_old, x_temp, colors)
			im_draw.polygon([(x_old,0),(x_temp,0),(x_temp,y),(x_old,y)],tuple(colors))
			x_old = x_temp
			x_temp = x_temp + (x/colorset_size)
		if verbose:
			colorset_im.show()
		return colorset_im
	
	def get_JSON_values(self, json_path = "./../../lztest/imageInfo2.json"):
		"""Get Ratings from JSON""" 
		if os.path.exists(json_path):
			print "Fetching JSON from {} ".format(json_path)
		else:
			print "JSON Doesn't exist"
			return False	
		self.in_json_file = open(json_path, 'r')
		self.in_json_data = json.load(self.in_json_file)
		#self.json_dict = dict

		#print len(self.json_data['data'])
		for photo_number in range(0,len(self.in_json_data['data'])):
			#print self.json_data['data'][photo_number]['link']
			link_name = re.split('/+', self.in_json_data['data'][photo_number]['link'])[3]
			#print link_photoname
			#self.json_dict.update(self.json_data['data'][photo].iteritems())
			#print os.path.splitext(self.filename)[0] + link_name
			if os.path.splitext(self.filename)[0] == link_name:
				print "Match Found in Dataset at Element Number {}".format(photo_number)
				for photo_keys, photo_values in self.in_json_data['data'][photo_number].iteritems():
					print photo_keys, photo_values
				self.likes = self.in_json_data['data'][photo_number]['likes']
				return True
		
		return False

class ColorSet(igFood):
	"""Color Set Determination
	Written before I discovered matplotlib.colors.
	Could be refactored in the future"""

	def __init__(self, filepath = "test.png", verbose=False):
		super(ColorSet, self).__init__(filepath)
		self.kmeans_centroids = self.kmeans_cluster(self.pix_array)
		self.kmeans_colorset_im = self.get_rgb_visualization(self.kmeans_centroids, verbose)

	# def save_JSON_values(self, json_path = "./../../lztest/learning.json"):
	# 	"""Save ColorSets to JSON"""
	# 	if os.path.exists(json_path):
	# 		print "Saving JSON at {} ".format(json_path)
	# 	else:
	# 		print "JSON Doesn't exist, making new JSON"
	# 		with open(json_path, 'w', encoding='utf-8') as out_json_file:
	# 			self.out_json_data = json.load(out_json_file)
	# 			out_json_data['name'] = os.path.splitext(self.filename)[0]
	# 			out_json_file.close()
	# 	with open(json_path, 'r+', encoding='utf-8') as out_json_file:	
	# 		self.out_json_data = json.load(out_json_file)
	# 		data['name'] = os.path.splitext(self.filename)[0]
	# 		out_json_file.close()

	def get_kmeans_centroids(self):
		"""Get Color Set Values"""
		return self.kmeans_centroids

	def kmeans_cluster(self, pix_array):
		"""Returns 3 colors from k-means clustering on input Array
		We will ignore A value in RGBA
		Must whiten first"""
		whitened = whiten(pix_array)
		#kmeans(obs, k_or_guess, iter=20, thresh=1e-05, check_finite=True)[source]
		#Then, must rescale centroids from whitened values with standard deviation
		centroids = kmeans(whitened,3)[0] * std(pix_array, 0)
		print "K-Means Cluster Centroids at \n{0}".format(centroids)
		rounded_centroid = []
		for colors in centroids:
			rounded_color = [int(round(band_value)) for band_value in colors ]
			rounded_centroid.append(rounded_color)
		print "Rounded Centroids at \n{0}".format(rounded_centroid)
		return rounded_centroid
	
	def show_images(self):
		"""Show All Image Results"""
		self.im.show()
		self.kmeans_colorset_im.show()

	def save_images(self, output_path = "colorset_test.png"):
		"""Save All Image Results to Path"""
		self.kmeans_colorset_im.save(output_path + 'kmeans_colorset_im_' + self.filename)

class ColorBalancing(ColorSet):
	"""Simple Color Balancing and Normalizing on Input Ranges and Colors"""

	def __init__(self, filepath = "test.png", verbose = False, balance_colors = [(255, 255, 255), (0, 0, 0)], 
				saturation_level = 1, normalization_range = (0,255)):
		"""Input Balance Colors"""
		super(ColorBalancing, self).__init__(filepath, verbose)
		self.balance_colors = balance_colors
		self.saturation_level = saturation_level
		self.red_range = None
		self.green_range = None 
		self.blue_range = None
		self.color_balanced_array = self.bw_color_balancing(self.pix_asarray, self.saturation_level)
		self.unscaled_distributed_array = self.rescale_array(self.color_balanced_array, [self.red_range,
												self.green_range, self.blue_range])
		self.scaled_color_balanced_array = (self.unscaled_distributed_array.copy() * normalization_range[1]).astype('uint8')
		
		self.color_balanced_im = Image.fromarray(self.color_balanced_array)
		self.scaled_color_balanced_im = Image.fromarray(self.scaled_color_balanced_array)
		
		self.pix_list = image2_list(self.pix, self.im)
		self.color_balanced_list = image2_list(self.color_balanced_im.load(), self.color_balanced_im)
		self.scaled_color_balanced_list = image2_list(self.scaled_color_balanced_im.load(), self.scaled_color_balanced_im)

	def get_scaled_colorbalanced_list(self):
		print self.scaled_color_balanced_list

	def save_histograms(self, output_path):
		"""Saves Histograms to output_path
		TBD - Move Save Function here, and restore Plot function in plot_RGB_histogram"""
		#self.color_balanced_histogram = self.plot_RGB_histogram(self.pix_list, self.color_balanced_list, output_path, "color_balanced_list")
		self.scaled_color_balanced_histogram = self.plot_RGB_histogram(self.pix_list, self.scaled_color_balanced_list, output_path, "scaled_color_balanced_list")


	def rescale_array(self, input_array, color_range = ((0, 255), (0, 255), (0, 255)), normalization_range = ((0, 255), (0, 255), (0, 255))):
		"""normalize_PIL_array / Scale Array to fit Range
		input: numpy Array, RGB Range for Normalization
		output: Array of normalized values
		Normalize an input Array over a range. Probably will only work on image Arrays
		"""
		norm = colors.Normalize(normalization_range[0][0],normalization_range[0][1])
		#targetcolor = norm(targetcolor)

		##### Multiple Colors requires this to be changed ######
		normalized_array = norm(input_array)
		normalization_range = norm(normalization_range)
		#image_extrema = self.im.getextrema()
		scalar = numpy.subtract((color_range[0], color_range[1], color_range[2]), normalization_range)
		print "Normalizing from RGB Max and Min Values {}, \nExtrema {}, \nScalar\n {}".format(normalization_range, color_range, scalar)
		# Implement Error Checker Later
		# for number in scalar:
		# 	for values in number:
		# 		if values < 0:
		# 			print "Scalar goes into Negative Values"
		# 			raise BaseException

		red, green, blue = normalized_array[:,:,0], normalized_array[:,:,1], normalized_array[:,:,2]
		red = (red - scalar[0][0]) * float(normalization_range[0][1]) / float((color_range[0][1] - scalar[0][0]))
		green = (green - scalar[1][0]) * float(normalization_range[1][1])  / float((color_range[1][1] - scalar[1][0]))
		blue = (blue - scalar[2][0]) * float(normalization_range[2][1])  / float((color_range[2][1] - scalar[2][0]))
		# Have to reassign array since the modifications cause it to no longer be contiguous in memory.
		output_array = numpy.array(normalized_array).copy()
		output_array[:,:,0] = red
		output_array[:,:,1] = green
		output_array[:,:,2] = blue
		return output_array

	def rebalance_colors(self, pix_asarray, balance_colors = [(255, 255, 255), (0, 0, 0)], 
				saturation_level = 1, normalization_range = (0,255)):
		trigger = True
		self.balance_colors = balance_colors
		self.saturation_level = saturation_level
		temp_pix_asarray = pix_asarray
		print "Running Color Balancing with these Colors {} and Saturation Level {}".format(self.balance_colors, self.saturation_level)
		for color_choice in balance_colors:
			#if trigger: 
			#	color_balanced_array = self.color_balancing(color_balanced_array, self.saturation_level, color_choice, normalization_range)
			#	trigger = False
			#else :
			temp_pix_asarray = self.color_balancing(temp_pix_asarray, color_choice, self.saturation_level, normalization_range)
		return temp_pix_asarray

	def get_balance_colors(self):
		return self.balance_colors

	def save_images(self, output_path = "colorset_test.png"):
		"""Save All Image Results to path"""
		super(ColorBalancing, self).save_images(output_path)
		self.color_balanced_im.save(output_path + 'color_balanced_im_' + self.filename)
		self.scaled_color_balanced_im.save(output_path + "scaled_color_balanced_im_" + self.filename)

	def show_images(self):
		"""Show All Image Results"""
		self.im.show()
		self.color_balanced_im.show()
		self.scaled_color_balanced_im.show()

	def color_balancing(self, input_array, targetcolor = (255, 255, 255), 
							saturation_level = 1, normalization_range = (0,255)):
		"""Color Balancing Input Image Array
		By converting very dark or very light pixels to White or Black. 
		Overrides allow for conversion to any Strong Color.
			Normalize target color to 0 to 1.0, then set max and lower saturation levels. 
			All pixels past the threshold will be converted.
		255, 255, 255 = White
		0, 0, 0 = Black
		Saturation level is from 0 to 100
		"""
		print "Normalizing Image to Target Color {}".format(targetcolor)
		norm = colors.Normalize(normalization_range[0],normalization_range[1])
		targetcolor = norm(targetcolor)
		normalized_array = norm(input_array)
		red, green, blue = normalized_array.T
		#self.red_range = numpy.percentile(red, (saturation_level/2, 100-(saturation_level/2)))
		#self.green_range = numpy.percentile(green, (saturation_level/2, 100-(saturation_level/2)))
		#self.blue_range = numpy.percentile(blue, (saturation_level/2, 100-(saturation_level/2)))
		#print "Red {} Green {} Blue {} Saturation Levels".format(red_range, green_range, blue_saturation_level)
		replacement_area = (((red > (targetcolor[0] - saturation_level))
							& (red < (targetcolor[0] + saturation_level))) 
							& ((green > (targetcolor[1] - saturation_level)) 
							& (green < (targetcolor[1] + saturation_level)))
							& ((blue > (targetcolor[2] - saturation_level))
							& (blue < (targetcolor[2] + saturation_level))))
		normalized_array[...][replacement_area.T] = targetcolor
		print "Target Color {} Saturation Level {}".format(targetcolor, saturation_level)
		#print replacement_area
		output_array = (numpy.array(normalized_array).copy() * normalization_range[1]).astype('uint8')
		#print output_array
		return output_array

	def bw_color_balancing(self, input_array, 
							saturation_level = 1, normalization_range = (0,255)):
		"""BW Color Balancing Input Image Array
		By converting very dark or very light pixels to White or Black. 
		Overrides allow for conversion to any Strong Color.
			Normalize target color to 0 to 1.0, then set max and lower saturation levels. 
			All pixels past the threshold will be converted.
		255, 255, 255 = White
		0, 0, 0 = Black
		Saturation level is from 0 to 100
		"""
		targetcolor = [(255, 255, 255), (0, 0, 0)]
		print "Normalizing Image to Black and White {}".format(targetcolor)
		norm = colors.Normalize(normalization_range[0],normalization_range[1])
		targetcolor = norm(targetcolor)
		normalized_array = norm(input_array)
		red, green, blue = normalized_array.T
		image_extrema = self.im.getextrema()
		print "Extrema {}".format(image_extrema)
		self.red_range = numpy.percentile(red, (saturation_level/2, 100-(saturation_level/2)))
		self.green_range = numpy.percentile(green, (saturation_level/2, 100-(saturation_level/2)))
		self.blue_range = numpy.percentile(blue, (saturation_level/2, 100-(saturation_level/2)))
		print "Red {} Green {} Blue {} Saturation Levels".format(self.red_range, self.green_range, self.blue_range)
		black_replacement_area = (((red > self.red_range[1]))
							& ((green > self.green_range[1])) 
							& ((blue > self.blue_range[1])))
		normalized_array[...][black_replacement_area.T] = targetcolor[0]
		white_replacement_area = (((red < self.red_range[0]))
							& ((green < self.green_range[0])) 
							& ((blue < self.blue_range[0])))
		normalized_array[...][white_replacement_area.T] = targetcolor[1]

		print "Target Color \n{} \nSaturation Level {}".format(targetcolor, saturation_level)
		#print replacement_area
		output_array = (numpy.array(normalized_array).copy() * normalization_range[1]).astype('uint8')
		#print output_array
		return output_array

	def plot_RGB_histogram(self, original_pix_list, new_pix_list, output_path, name_of_list, 
							red=True, green=True , blue=True, histogramtitle="RGB Histogram of Overall Dataset", popularity=False, bins=255):
		"""UGLY - To be repaired later from before we started using numpy arrays properly"""
		redList=[]
		greenList=[]
		blueList=[]
		n=0
		for row in original_pix_list:
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

		redList_2 = []
		greenList_2 = []
		blueList_2 = []
		n=0
		
		for row in new_pix_list:
			#print "row[{}] {}".format(n,row)
			n+=1
			tempList=row
			#print "tempList {}".format(tempList)
			intsonly = re.compile('\d+(?:\.\d+)?')
			#print int(intsonly.findall(tempList[1])[0])
			#print tempList
			redList_2.append((tempList[0]))
			greenList_2.append((tempList[1]))
			blueList_2.append((tempList[2]))
		if popularity:
			histogramtitle = "Popularity Weighted Data " + histogramtitle			
		if red:
			output_filename = os.path.splitext(self.filename)[0] + ".png"
			plt.figure()
			plt.title(histogramtitle)
			plt.hist(redList, bins, color = 'pink', histtype='step')
			plt.hist(redList_2, bins, color = 'red', histtype='step')
			output_filename = "histogram_" + name_of_list + str(self.saturation_level) + str(self.balance_colors) + "red_" + output_filename
			plt.savefig(output_path + output_filename, bbox_inches = 'tight')
			plt.close()
		if green:
			output_filename = os.path.splitext(self.filename)[0] + ".png"
			plt.figure()
			plt.title(histogramtitle)
			plt.hist(greenList, bins, color = 'lightgreen', histtype='step')
			plt.hist(greenList_2, bins , color = 'green', histtype='step')
			output_filename = "histogram_" + name_of_list + str(self.saturation_level) + str(self.balance_colors) + "green_" + output_filename
			plt.savefig(output_path + output_filename, bbox_inches = 'tight')
			plt.close()
		if blue:
			output_filename = os.path.splitext(self.filename)[0] + ".png"
			plt.figure()
			plt.title(histogramtitle)
			plt.hist(blueList, bins, color = 'lightblue', histtype='step')
			plt.hist(blueList_2, bins, color = 'blue', histtype='step')
			output_filename = "histogram_" + name_of_list + str(self.saturation_level) + str(self.balance_colors) + "blue_" + output_filename
			plt.savefig(output_path + output_filename, bbox_inches = 'tight')
			plt.close()

		#plt.show()

	#append_database(kmeans_centroids, likes, red_range, green_range, blue_range, filename)
	def append_database(self, dbPath="./../../database/learningDB.csv"):
		"""Append to DataBase"""
		##TODO : Check Duplicate
		#add checkDuplicate(dbPath, in_filename) to if statement		
		if os.path.isfile(dbPath):
			print "Appending to database at {}".format(dbPath)
			with open(dbPath, 'a') as databasefile:
				fields=['in_filename', 'likes', 'colorset_1_r', 'colorset_1_g', 'colorset_1_b', 'colorset_2_r', 'colorset_2_g', 'colorset_2_b', 
						'colorset_3_r', 'colorset_3_g', 'colorset_3_b', 'red_range_l', 'red_range_h', 'green_range_l', 'green_range_h', 'blue_range_l', 'blue_range_h']
				writer = csv.DictWriter(databasefile, fieldnames=fields)
				writer.writerow({'in_filename':self.filename, 'likes':self.likes, 
								'colorset_1_r':self.kmeans_centroids[0][0], 'colorset_1_g':self.kmeans_centroids[0][0], 'colorset_1_b':self.kmeans_centroids[0][0], 
								'colorset_2_r':self.kmeans_centroids[1][0], 'colorset_2_g':self.kmeans_centroids[1][0], 'colorset_2_b':self.kmeans_centroids[1][0], 
								'colorset_3_r':self.kmeans_centroids[2][0], 'colorset_3_g':self.kmeans_centroids[2][0], 'colorset_3_b':self.kmeans_centroids[2][0], 
								'red_range_l':self.red_range[0], 'red_range_h':self.red_range[1], 'green_range_l':self.green_range[0], 'green_range_h':self.green_range[1], 
								'blue_range_l':self.blue_range[0], 'blue_range_h':self.blue_range[1]}),
		else:
			print "Database does not exist, creating file at {}".format(dbPath)
			with open(dbPath, 'w') as databasefile:
				print "Appending value to database at {0}".format(dbPath)
				fields=['in_filename', 'likes', 'colorset_1_r', 'colorset_1_g', 'colorset_1_b', 'colorset_2_r', 'colorset_2_g', 'colorset_2_b', 
						'colorset_3_r', 'colorset_3_g', 'colorset_3_b', 'red_range_l', 'red_range_h', 'green_range_l', 'green_range_h', 'blue_range_l', 'blue_range_h']
				writer = csv.DictWriter(databasefile,fieldnames=fields)
				writer.writeheader()
				writer.writerow({'in_filename':self.filename, 'likes':self.likes, 
								'colorset_1_r':self.kmeans_centroids[0][0], 'colorset_1_g':self.kmeans_centroids[0][0], 'colorset_1_b':self.kmeans_centroids[0][0], 
								'colorset_2_r':self.kmeans_centroids[1][0], 'colorset_2_g':self.kmeans_centroids[1][0], 'colorset_2_b':self.kmeans_centroids[1][0], 
								'colorset_3_r':self.kmeans_centroids[2][0], 'colorset_3_g':self.kmeans_centroids[2][0], 'colorset_3_b':self.kmeans_centroids[2][0], 
								'red_range_l':self.red_range[0], 'red_range_h':self.red_range[1], 'green_range_l':self.green_range[0], 'green_range_h':self.green_range[1], 
								'blue_range_l':self.blue_range[0], 'blue_range_h':self.blue_range[1]}),
				
if __name__ == '__main__':
	arguments = docopt(__doc__)
	input_filepath = os.path.dirname(arguments['<input_image>'])
	input_filename = ntpath.basename(arguments['<input_image>'])
	if arguments['<output_path>']:
		output_path = arguments['<output_path>']
	else:
		#output_path = "." + input_filepath + "/output/" + os.path.splitext(input_filename)[0] + "/"
		output_path = "./public/output/" + os.path.splitext(input_filename)[0] + "/"
	try:
		os.makedirs(output_path)
	except OSError:
		if os.path.exists(output_path):
			print "PATH ALREADY EXISTS - Will Probably Overwrite Exisiting Images"
		else:
			raise
	print "input {} output {} ".format(input_filepath, output_path)
	verbose = arguments['-v']
	if verbose:
		print(arguments)

	color_balancing_test = ColorBalancing(arguments['<input_image>'], verbose)

	#######Results
	if arguments['--database']:
		print "Pointing to Custom DB"
		dbPath = arguments['--database']
	else:
		dbPath="./../../database/learningDB.csv"

	if arguments['-l']:
		print "Adding to Learning DB"
		if color_balancing_test.get_JSON_values():
			print "Number of Likes {}".format(color_balancing_test.likes)
			color_balancing_test.append_database(dbPath)

	color_balancing_test.show_images()
	
	color_balancing_test.save_images(output_path)
	color_balancing_test.save_histograms(output_path)

	#color_balancing_test.show_images()
	print "output path {}".format(output_path)

