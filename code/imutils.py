# import packages
import numpy as np
import cv2

def translate(image, x, y):
	# define translation matrix and then perform translation
	M = np.float32([[1, 0, x], [0, 1, y]])
	shifted = cv2.warpAffine(image, M, (image.shape[1], image.shape[0]))

	# return translated image
	return shifted

def rotate(image, angle, center = None, scale = 1.0):
	# get dimensions of the image
	(h, w) = image.shape[:2]

	# if center is None, initialize it as the center of the image
	if center is None:
		center = (w // 2, h // 2)

	# perform rotation
	M = cv2.getRotationMatrix2D(center, angle, scale)
	rotated = cv2.warpAffine(image, M, (w, h))

	# return rotated image
	return rotated

def resize(image, width = None, height = None, inter = cv2.INTER_AREA):
	# initialize dimensions of image to be resized and get image size
	dim = None
	(h, w) = image.shape[:2]

	# if width and height are None, return original image
	if width is None and height is None:
		return image

	# if width is None
	if width is None:
		# calculate ratio of the height and construct image dimensions
		r = height / float(h)
		dim = (int(w * r), height)

	# if height is None
	else:
		# calculate the ratio of the width and construct image dimensions
		r = width / float(w)
		dim = (width, int(h * r))

	# resize the image
	resized = cv2.resize(image, dim, interpolation = inter)

	# return resized image
	return resized
