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

print "hi"