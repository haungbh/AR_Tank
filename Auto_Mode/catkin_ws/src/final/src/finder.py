import cv2
import random
import numpy as np
import copy

#img = cv2.imread('test.bmp')
#img2 = copy.copy(img)


def find_target(img):
	img2 = copy.copy(img)
	rows = len(img)
	cols = len(img[0])


	for i in range(rows): 
		for j in range(cols):
			if img[i][j][0] > 100 and img[i][j][2] > 100 and img[i][j][1] > 100:
				img2[i][j] = 0
			else:
				img2[i][j] = 255
        
	kernel = np.ones((50,50),np.uint)  
	opening = cv2.morphologyEx(img2, cv2.MORPH_OPEN, kernel)
	center_x = 0
	center_y = 0
	size = 1
	for i in range(rows): 
		for j in range(cols):
			if opening[i][j][0] > 1:
				center_x += j
				center_y -= i
				size += 1
			

	center_y *= -1
	center_x /= size
	center_y /= size
	print(center_x, center_y)
	cv2.imshow("window", opening)
	#cv2.imwrite('output.bmp',img)
	return center_x,center_y

