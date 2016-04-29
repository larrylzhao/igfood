#!/usr/bin/env python
from docopt import docopt
from PIL import Image, ImageDraw
from numpy import array, std
from scipy.cluster.vq import vq, kmeans, whiten
import csv
import ntpath
import os.path

import json
from pprint import pprint
"""
Usage:
jsonAppend.py [-vh] <json> <csvfile>

Options:
	-h --help                          show this help message
	-v --verbose                       show input and output image
"""

if __name__ == '__main__':
	arguments = docopt(__doc__)
	json_filePath = arguments['<database>']
	csv_filePath = arguments['<csvfile>']
	verbose = arguments['-v']
	if verbose:
		print(arguments)
	json = open(imageInfo.json).read()

	