#!/usr/bin/python2
# -*- coding: UTF-8 -*-
# Author: Andreas Bock

import sys
import getopt
import numpy as np
from scipy import misc
import scipy.cluster.vq as vq

def usage ():
	print 'Usage: kmeans_it [INPUT_FILE] [OUTPUT_IMAGE] [OPTIONS]'
	print 'OPTIONS : -k [INTEGER]   # The number of clusters'
	print '\t: -g convert to greyscale'
	exit()

def perform_kmeans (input_image, output_image, colours):
	img = misc.imread(input_image)
	ysize, xsize, _ = img.shape
	clustering_pixels = np.reshape(img, (xsize*ysize, 3))
	
	centroids, labels = vq.kmeans2(clustering_pixels, colours)
	labels = np.reshape(labels, (ysize, xsize))

	for i in range(ysize):
		for j in range(xsize):
			img[i,j] = tuple(centroids[labels[i,j]])
	misc.imsave(output_image, img)

def to_greyscale (input_image, output_image):
	def avg(rgb):
		greyscale = np.average(rgb)
		return tuple([greyscale]*3)
	img = misc.imread(input_image)
	ysize, xsize, _ = img.shape
	for i in range(ysize):
		for j in range(xsize):
			img[i,j] = avg(img[i,j])
	misc.imsave(output_image, img)

def main ():
	try:
		opts, args = getopt.gnu_getopt(sys.argv[1:], 'hk:g', ['help','kmeans','greyscale'])
		if opts == [] or len(args) < 2:
			usage()
	except getopt.GetoptError as err:
		print(err)
		usage()
	
	# Get input and output
	try:
		input_image  = args[0]
		output_image = args[1]
	except:
		usage()

	# What to do with the image?
	for switch, val in opts:
		if switch in '-h' or switch in '--help':
			usage()
		if switch in '-k' or switch in '--kmeans':
			perform_kmeans(input_image, output_image, int(val))
		if switch in '-g' or switch in '--greyscale':
			to_greyscale(input_image, output_image)

if __name__ == '__main__':
    main()
