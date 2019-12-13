#!/usr/bin/env python
import rospy, math
import random
from nav_msgs.msg import Path
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from geometry_msgs.msg import PoseStamped
import tf.transformations
from tf.transformations import euler_from_quaternion, quaternion_from_euler

currentOdom = Odometry()
testRobot = Odometry()



def main():
	print 'In main'
	rospy.init_node('path_follow', anonymous=True)

	rospy.Subscriber("/path",Path, callback)
	rospy.Subscriber('/odom', Odometry, odomCb)
	rospy.spin()


	print 'Exiting normally'

# Callback function for odometry data
def odomCb(data):
	global currentOdom
	currentOdom = data


def callback(data):
	global odist
	#rospy.loginfo(data.pose.position.x)
	for pnt in data.poses:
		pubVel = rospy.Publisher('cmd_vel', Twist, queue_size=10)

		distance = math.sqrt(math.pow(pnt.pose.position.x - currentOdom.pose.pose.position.x,2) + math.pow(pnt.pose.position.y - currentOdom.pose.pose.position.y,2) )

		angular = math.atan2(pnt.pose.position.y - currentOdom.pose.pose.position.y, pnt.pose.position.x - currentOdom.pose.pose.position.x)


		turnTo(angular, pubVel)
		driveDist(distance, pubVel)


def driveDist(dist, pub):
	rate = rospy.Rate(30)
	tempOdom = currentOdom

	tempDist = 0

	# Create the Twist msg
	vel = Twist()
	vel.linear.x = 0.33 # Speed could be a parameter
	vel.angular.z = 0

	# While we haven't moved the specified distance
	while tempDist < dist and not rospy.is_shutdown():
		pub.publish(vel)

		# Update distance
		tempDist = math.sqrt( math.pow(tempOdom.pose.pose.position.x - currentOdom.pose.pose.position.x,2) + math.pow(tempOdom.pose.pose.position.y - currentOdom.pose.pose.position.y,2) )

		# Sleep
		rate.sleep()

	# Stop robot by publishing 1 more Twist with 0 speed
	vel.linear.x = 0
	pub.publish(vel)

def turnTo(theta, pub):

	thetaStart = tf.transformations.euler_from_quaternion( [currentOdom.pose.pose.orientation.x, currentOdom.pose.pose.orientation.y, currentOdom.pose.pose.orientation.z, currentOdom.pose.pose.orientation.w] )[2]

	# Get the angle between the robot's current orientation and the target orientation
	thetaDist = findDistanceBetweenAngles(theta, thetaStart)

	# Make a rate
	rate = rospy.Rate(30)

	# Create the Twist msg
	vel = Twist()
	vel.linear.x = 0
	vel.angular.z = 0.785 # Speed could be a parameter

	# Make a threshold to check for stopping the robot
	threshold = 0.10

	# While the robot is not at the specified orientation (or within a small threshold)
	while abs(thetaDist) > threshold and not rospy.is_shutdown():
		
		if(thetaDist > 0):
			vel.angular.z = 0.785
		else:
			vel.angular.z = 0.785 * -1
		# Drive the robot
		pub.publish(vel)

		# Get the robot's current orientation
		thetaNow = tf.transformations.euler_from_quaternion( [currentOdom.pose.pose.orientation.x, currentOdom.pose.pose.orientation.y, currentOdom.pose.pose.orientation.z, currentOdom.pose.pose.orientation.w] )[2]

		# Update the angle between
		thetaDist = findDistanceBetweenAngles(thetaNow, theta)
		#print('thetaNow: %s thetaDist: %s' % (thetaNow, thetaDist))

		# Sleep
		rate.sleep()

	# Stop robot by publishing 1 more Twist with 0 speed
	vel.angular.z=0
	pub.publish(vel)


def findDistanceBetweenAngles(a, b):
    
	result = 0
	difference = b - a
	val = 3.141592
	if difference > math.pi:
		difference = math.fmod(difference, val)
		result = difference - val

	elif(difference < -math.pi):
		result = difference + (2*math.pi)

	else:
		result = difference

	return result





if __name__ == '__main__':
	main()
