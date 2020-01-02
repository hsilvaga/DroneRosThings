#!/usr/bin/env python

import rospy 
from sensor_msgs.msg import PointCloud2
from sensor_msgs.msg import Image
from sensor_msgs.msg import LaserScan
from 



#point_data
def subscriberPointCloud():
	rospy.Subscriber('/camera/depth_registered/points', PointCloud2, pointsCallback)

def pointsCallback(points_data): #prints all data in points array
	print(points_data)
#---------------------------------------------------------------------------------------------------------------------------------
#image
def subscriberImage():
	rospy.Subscriber('/camera/rgb/image_raw', Image, imageCallback)

def imageCallback(pixels_data): #Prints pixel values in data array
	print(pixels_data.height)
	print(pixels_data.width)
	for i in pixels_data.data:
		print i
#----------------------------------------------------------------------------------------------------------------------------------
#laser
def subscriberLaser():
	rospy.Subscriber('/scan', LaserScan, laserCallback)

def laserCallback(laser_data): # print field of view for laserscanner and print range/distance values from laser
	fov = (laser_data.angle_max) - (laser_data.angle_min)
	print(fov)
	
	print(laser_data.ranges)

def publisherLaser():
	visualPub = rospy.Publish('visualization_marker', 
#-------------------------------------------------------------------------------------------------------------------------------------------

def main(): 
	rospy.init_node("sensor", anonymous = True)

	#subscriberPointCloud()
	#subscriberImage()
	subscriberLaser()
	publisherLaser()
	rospy.spin()
	
main()