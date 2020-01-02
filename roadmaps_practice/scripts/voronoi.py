#!/usr/bin/env python
#from msg_package.msg import MyMsg
import rospy
from nav_msgs.msg import OccupancyGrid
from roadmaps_practice.msg import GridInfo, ObPixels
from nav_msgs.msg import Odometry
rospy.init_node('voronoi_node')
pub = rospy.Publisher("/voronoi_map",OccupancyGrid,queue_size=100)
result = OccupancyGrid()
voronoi_grid = OccupancyGrid()

def callback(data):
	global result
	result.info.width = data.info.width
	result.info.height = data.info.height
	result.info.resolution =  data.info.resolution
	resetValue(data)

def voronoi():
	rospy.Subscriber('/brushfire_map', OccupancyGrid, callback)
	rospy.spin()

def resetValue(param):
	global result
	data = []
	for value in param.data:
		data.append(127)
	result.data = data
	computeMaxima(param)

def computeMaxima(grid):
	width = grid.info.width
	height = grid.info.height
	data = grid.data
	newData = result.data
	for i in range(0,len(grid.data)):
		if(data[i] != 0):
			localMax = 0
			#check up					
			if(i - width>0):
				if(data[i - width]>localMax):
					localMax = data[i-width]
			#check down
			if (i + width) < width*height:
				if (data[i + width]>localMax):
					localMax = data[i + width]
			#check right
			if(i+1) <width*height:
				if (data[i + 1]>localMax):
					localMax = data[i+1]
			#chekc left
			if (data[i -1]>localMax):
				localMax = data[i-1]
			if(data[i] >= localMax):
				newData[i] = 0

	result.data = newData		
	rospy.sleep(.5)
	pub.publish(result)

voronoi()