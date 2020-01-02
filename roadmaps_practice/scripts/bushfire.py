#!/usr/bin/env python

import rospy
from roadmaps_practice.msg import GridInfo, ObPixels
from nav_msgs.msg import OccupancyGrid
import numpy as np
import sys

map = [[0 for i in range(40)] for j in range(40)]

def callback(grid_data): #takes in array and creates brushfire 2d array
	global map
	np.set_printoptions(threshold=sys.maxsize)

	#print(grid_data.grid.data)
	count = 0
	for i in range(40): #this sets the map with boundaries to 1 and obstacles to 100
		for j in range(40):
			map[i][j] = grid_data.grid.data[count]

			if i == 0 or j ==  0 or i == 39 or j == 39: #makes a
				map[i][j] = 1

			#if 8-way next to 100 then set to 1
			#if map[i + 1][j]  == 100 or map[i][j + 1]  == 100 or map[i - 1][j]  == 100 or map[i][j - 1]  == 100 or map[i + 1][j + 1]  == 100 or map[i - 1][j - 1]  == 100 or map[i + 1][j - 1]  == 100 or map[i - 1][j + 1]  == 100:#L, U, R, D and diagonals
				#	map[i][j] = 1

			count += 1

		i  =1
		j = 1
		for i in range(39): #this sets the map with boundaries to 1 and obstacles to 100
			for j in range(39):
			#if 8-way next to 100 then set to 1
				if map[i + 1][j]  == 100 or map[i][j + 1]  == 100 or map[i - 1][j]  == 100 or map[i][j - 1]  == 100 or map[i + 1][j + 1]  == 100 or map[i - 1][j - 1]  == 100 or map[i + 1][j - 1]  == 100 or map[i - 1][j + 1]  == 100:#L, U, R, D and diagonals
					map[i][j] = 1
	
	setTo = 1
	
	while findZero(): #keep looping while map contains zeros
		x = 1
		y = 1
		for x in range(39):
			for y in range(39):
				#if 8-way contains setTo then set the element to setTo + 1
				if map[x][y] != 0 and map[x + 1][y]  == setTo or map[x][y + 1]  == setTo or map[x - 1][y]  == setTo or map[x][y - 1]  == setTo  or map[x + 1][y + 1]  == setTo or map[x - 1][y - 1]  == setTo or map[x + 1][y - 1]  == setTo or map[x - 1][y + 1]  == setTo: #L, U, R,D and diagonals
					map[x][y] = 3
		setTo += 1
			
	print(np.matrix(map))

def findZero():
	global map
	for i in range(40):
		for j in range(40):
			if map[i][j] == 0:
				return True
	return False
	
def subscriber():
	rospy.Subscriber('/mapInfo', GridInfo, callback)
	rospy.spin()

def publisher():
	pub = rospy.Publisher('/brushfire_map', OccupancyGrid, queue_size = 10)
	
#def brushFire():
	#while True:
		
if __name__ == '__main__':
	rospy.init_node('brushfire', anonymous=True)

	subscriber()
	publisher()
	brushFire()