
import cv2
import sys
import numpy as np
from sklearn.cluster import MeanShift
from mpl_toolkits.mplot3d import Axes3D
from counter import count


img = cv2.imread('Picture/08-dice.jpg')

img = cv2.resize(img,(500,500))


gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.equalizeHist(gray)

blur = cv2.GaussianBlur(gray, (5, 5),1)


binary = cv2.Canny(blur,70,100)

binary = cv2.dilate(binary,None)
cv2.imshow('canny',binary)
cv2.floodFill(binary,None,(0,0),255)
binary = cv2.dilate(binary,None)
binary = cv2.erode(binary,None,iterations = 2)
binary = cv2.bitwise_not(binary)

dot_mask = np.zeros((binary.shape[0],binary.shape[1]),np.uint8)

num_dot,markers = cv2.connectedComponents(binary)
num_dot -=1
positions = []
for dot in range(num_dot):
	index = np.where(markers==dot+1)
	pos_x =	int((index[0].min()+index[0].max())/2+0.5)
	pos_y = int((index[1].min()+index[1].max())/2+0.5)
	len_x = int(np.abs(index[1].min()-index[1].max()))
	len_y = int(np.abs(index[0].min()-index[0].max()))
	radius = np.maximum(len_y,len_x)
	positions.append([pos_x,pos_y,radius])
	dot_mask[pos_x-int(radius/2):pos_x+int(radius/2),pos_y-int(radius/2):pos_y+int(radius/2)]=255


dot_mask = cv2.erode(dot_mask,None,iterations = 10)
dot_mask = cv2.dilate(dot_mask,None,iterations = 15)
cv2.imshow('this',dot_mask)
num_dot,markers = cv2.connectedComponents(dot_mask)
for dot in range(num_dot-1):

	index = np.where(markers==dot+1)
	this_mask = np.zeros((markers.shape[0],markers.shape[1],3),np.uint8)
	this_mask[markers==dot+1]=255
	this_mask = cv2.bitwise_and(this_mask,img)
	# cv2.imshow(str(dot),this_mask)
	# cv2.waitKey()
	dot_img = np.zeros((index[0].max()-index[0].min(),index[1].max()-index[1].min(),3),np.uint8)
	dot_img = this_mask[index[0].min():index[0].max(),index[1].min():index[1].max()]

	img = count(img,this_mask,index[0].min(),index[1].min())
	# cv2.imshow(str(dot),dot_img)
	# cv2.waitKey()

print(num_dot)
cv2.imshow('num',img)

cv2.waitKey(0)

