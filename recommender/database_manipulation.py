#!/usr/bin/env python
"""
=========================================
Database Manipulation
=========================================
Allows us to change from CSV and JSON to SQL Later.

Usage:
database_manipulation.py [-h]

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
import json
import re

#def findJSON

#def urltoimage(instagram_url='https://www.instagram.com/p/BDc6b1yNyl2/')
#	instagram_url='https://www.instagram.com/p/BDc6b1yNyl2/'
#	match = re.search(r"(?<=www.instagram.com/p/)*", instagram_url)
#	return imagename

def imagetoURL(imagename="BDc6b1yNyl2.jpg"):
	basename = os.path.splitext(imagename)[0]
	instagram_url = 'https://www.instagram.com/p/'+basename+"/"
	return instagram_url

def loadJSON(jsonpath='imageInfo.json'):
	if os.path.isfile(dbpath):
		

def findPopularity(imagename):
	basename = os.path.splitext(imagename)[0]

