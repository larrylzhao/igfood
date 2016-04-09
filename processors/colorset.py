#!/usr/bin/env python
"""
=========================================
RGB Color Set Detection
=========================================
Determine most common 3 colors via clustering (k-means) using scipy libraries

Usage:
colorset.py [-vho] <input_image>
colorset.py [-vho] <input_image> <output_image>

Options:
	-h --help                    show this help message
	-v --verbose                 show input and output image
	-o --output                  colorset.py generates output file
"""
from docopt import docopt
from PIL import Image, ImageDraw
from numpy import array, std
from scipy.cluster.vq import vq, kmeans, whiten

def openImage(filename="test.png", verbose=False):
	im = Image.open(filename)
	print "Loading Image {0} ".format(filename)
	if verbose:
		im.show()
	return im

def cluster(pix_array):
	#Returns 3 colors from k-means clustering on input Picture Array
	#We will ignore A value in RGBA
	#Must whiten first
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

def imageToArray(pix):
	#Input: Pixel Array object, Output: numpy Array
	print "Image Dimensions {0}".format(im.size)
	temp_list = []
	for x in range (0,im.size[0]):
 		for y in range (0,im.size[1]):
 			temp_list.append(pix[x,y][0:3])
 	pix_array = array(temp_list)
 	print "Picture Access Object converted to RGB numpy Array \n{0}".format(pix_array)
 	return pix_array

def colorset_image(colorset, in_filename="test.png", verbose=False, x=600, y=100):
	colorset_im = Image.new("RGB", (x, y))
	im_draw = ImageDraw.Draw(colorset_im)
	colorset_size = len(colorset)
	x_temp = x / colorset_size
	x_old = 0
	for colors in colorset:
		#rounded_color = [int(round(band_value)) for band_value in colors ]
		print "Filling Polygon in from {0} to {1} with color {2}".format(x_old, x_temp, colors)
		im_draw.polygon([(x_old,0),(x_temp,0),(x_temp,y),(x_old,y)],tuple(colors))
		x_old = x_temp
		x_temp = x_temp + (x/colorset_size)
	if verbose:
		colorset_im.show()
	return colorset_im

if __name__ == '__main__':
	arguments = docopt(__doc__)
	in_filename = arguments['<input_image>']
	if arguments['<output_image>']:
		out_filename = arguments['<output_image>']
	else:
		out_filename = "result_" + in_filename
	verbose = arguments['-v']
	if verbose:
		print(arguments)

	im = openImage(in_filename, verbose) #Open Image
	pix = im.load() # Get the Pixel Access Object
	pix_array = imageToArray(pix) 
	colorset = cluster(pix_array)
	colorset_im = colorset_image(colorset, in_filename, verbose)
	print "Creating a color set, saved at {0}".format(out_filename)
	colorset_im.save(out_filename)

