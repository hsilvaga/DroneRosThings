#!/usr/bin/env python
import rospy
import math
from sensor_msgs.msg import LaserScan
from visualization_msgs.msg import Marker
from geometry_msgs.msg import Point


# Create a global Publisher for visualization_msgs/Marker objects on topic '/visualization_marker'

pointArray = []
#*****************************************************************************************************************
# This function returns object that you can send to Rviz!
#
# Parameter 'points' should be a list of geometry_msgs/Point objects
# Returns a visualization_msgs/Marker object that can be published to Rviz on topic 'visualization_marker'

# Edit the frame_id assignment below if you're using a TB2 (lines 25 and 28)
#*****************************************************************************************************************
def getMarkerWithPoints(points):
	#print 'In plotPoint'
	marker = Marker()
	# TB2
	#marker.header.frame_id = 'camera_depth_frame'
	
	# TB3
	marker.header.frame_id = 'base_scan'
	
	marker.header.stamp = rospy.Time(0)
	marker.ns = ''
	
	# Id of marker will always be 0
	marker.id = 0
	marker.type = 8 # Points
	marker.action = 0 # Add
	
	# Append the point to the points array
	for p in points:
	# Use p as the point. It should be a PointStamped
		marker.points.append(p)
	
	# Set size 
	marker.scale.x = 0.02
	marker.scale.y = 0.02
	marker.scale.z = 0.02
	
	# Set color and then append to colors array
	marker.color.r = 1.0
	marker.color.g = 1.0
	marker.color.b = 1.0
	marker.color.a = 1.0
	marker.colors.append(marker.color)
	
	# Show for 10 seconds. Maybe pass this as a param?
	marker.lifetime = rospy.Duration(10.0)
	
	return marker
	
def subscriber():
	rospy.Subscriber('/scan', LaserScan, callback)
def callback(data):
	fov = data.angle_max - data.angle_min
	
	for i in LaserScan.ranges:
		myPoint = Point()
		myPoint.x = i * math.sin(fov)
		myPoint.y = i * math.cos(fov)
		pointArray.append(myPoint)

def main():
	print 'In main'
	rospy.init_node('laser_parse', anonymous=True)
	#Global pointArray
	
	# Make a subscriber for the /scan topic
	subscriber()
	# The /scan topic has sensor_msgs/LaserScan msgs published on it
	getMarkerWithPoints(pointArray)




if __name__ == '__main__':
	main()
