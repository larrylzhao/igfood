#!/usr/bin/env python
from docopt import docopt
from PIL import Image, ImageDraw
from numpy import array, std
from scipy.cluster.vq import vq, kmeans, whiten
import csv
import ntpath
import os.path
import colorset
import json
from pprint import pprint

"""
Input values, output histogram and histogram image
Usage:
histogram.py [-vh] <input> <output>

Options:
	-h --help                          show this help message
	-v --verbose                       show input and output image
"""

def histogram(input_array, bins=10):
	numpy.histogram(input_array, bins)
	pass

if __name__ == '__main__':
	arguments = docopt(__doc__)
	output_path = arguments['<output>']
	input_path = arguments['<input>']
	verbose = arguments['-v']
	if verbose:
		print(arguments)
