#!/usr/bin/env python

# Always follow your dreams, but first follow this path...

import rospy
import math
import tf
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Pose
from nav_msgs.msg import Odometry
from nav_msgs.msg import Path

# Rotation accuracy
ACC = 0.015

# Speeds
ROT_SPEED = 0.2
MOV_SPEED = 0.15

# Publish to '/cmd_vel' for turtlebot3
turtle2_pub = rospy.Publisher('/mobile_base/commands/velocity', Twist, queue_size=10)
turtle3_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)

# Hold the latest position and orientation
pose = Pose()

def findDistanceBetweenAngles(a, b):
    print 'In findDistanceBetweenAngles'
    result = 0


    difference = b - a
    print difference
    
    if difference > math.pi:
      difference = math.fmod(difference, math.pi)
      result = difference - math.pi

    elif(difference < -math.pi):
      result = difference + (2*math.pi)

    else:
      result = difference

    return result







# Enjoy compatability!
def twist_pub(twist):
    turtle2_pub.publish(twist)
    turtle3_pub.publish(twist)

# Callback for the 'odom' topic
def odomCb(data):
    global pose
    pose = data.pose.pose

# Callback for the 'path' topic
def pathCb(data):
    print('Path')
    for p in data.poses:
        print(p)
    for p in data.poses:
        print("My current position is:")
        print('%s Cells: (%s,%s)' % (pose, pose.position.x / 0.05, pose.position.y / 0.05))
        print("My next waypoint is:")
        print('%s Cells: (%s,%s)' % (p.pose.position, p.pose.position.x / 0.05, p.pose.position.y / 0.05))
        moveTo(p.pose.position)
    print("My final position is:")
    print(pose)



# Turn the robot to a specified orientation (in radians)
def turnToTheta(theta, speed):
    print 'In turnToTheta'


    # Use turnRad
    # params: calculate the diff in orientation
    
    # The orientation before we start turning
    thetaStart = tf.transformations.euler_from_quaternion( [pose.orientation.x, 
            pose.orientation.y, pose.orientation.z, pose.orientation.w] )[2]
    print 'thetaStart: %s' % thetaStart

    thetaDist = findDistanceBetweenAngles(theta, thetaStart)
    print 'thetaDist: %s' % thetaDist

    r = rospy.Rate(30)

    thresh = 0.2
    currentTheta = thetaStart

    angleDist = findDistanceBetweenAngles(thetaStart, theta)
    
    t = Twist()
    t.angular.z = 0.5 if angleDist > 0 else -0.5

    while abs(angleDist) > thresh and not rospy.is_shutdown():

        currentTheta = tf.transformations.euler_from_quaternion( 
                [pose.orientation.x, pose.orientation.y, pose.orientation.z, 
                        pose.orientation.w] )[2]
        angleDist = findDistanceBetweenAngles(currentTheta, theta)
        twist_pub(t)
        r.sleep()


# Turn the robot by a specified amount (in radians)
def turnTo(rad, speed):
    global pose
    rad = rad + 5
    # The orientation before we start turning
    thetaCurrent = tf.transformations.euler_from_quaternion( [pose.orientation.x, 
            pose.orientation.y, pose.orientation.z, pose.orientation.w] )[2] + 5
    
    # Rotate efficiently
    if (thetaCurrent > rad):
        speed = -speed

    # Create a twist msg to send
    t = Twist()
    t.linear.x = 0
    t.angular.z = speed

    # Create a rate
    r = rospy.Rate(10)

    print ('thetaCurrent: %s rad: %s acc: %s' % (thetaCurrent, rad, ACC))

    # While the robot has not turned enough
    while not (rad - ACC < thetaCurrent and thetaCurrent < rad + ACC) and not rospy.is_shutdown():

        # Update the current theta
        thetaCurrent = tf.transformations.euler_from_quaternion( 
                [pose.orientation.x, pose.orientation.y, pose.orientation.z, 
                pose.orientation.w] )[2] + 5
        print('Turning while thetaCurrent: %s' % thetaCurrent)
        
        # Publish twist and sleep
        twist_pub(t)
        r.sleep()
    
    # Stop when we reach our destination
    t.angular.z = 0
    twist_pub(t)
    r.sleep()

# Move a specified distance
def moveDist(d, speed):
    global pose

    # The position before we start moving
    p_start = pose.position

    # Create a Twist msg to send
    t = Twist()
    t.linear.x = speed
    t.angular.z = 0

    # Create a rate to send msgs
    r = rospy.Rate(10)

    # Move until we go the distance
    dRelative = 0
    while dRelative < d and not rospy.is_shutdown():

        # Get distance between current position and starting position
        dRelative = math.sqrt( math.pow( pose.position.x - p_start.x,2) + 
                math.pow( pose.position.y - p_start.y,2) )

        # Publish and sleep
        print ('dRelative: %s' % dRelative)
        twist_pub(t)
        r.sleep()
    
    # Stop when we reach our destination
    t.linear.x = 0
    twist_pub(t)
    r.sleep()

# Moves to a specified postion
def moveTo(pos):
    xDiff = pos.x - pose.position.x
    yDiff = pos.y - pose.position.y
    distance = math.sqrt((xDiff ** 2) + (yDiff ** 2))
    angle = math.atan2(yDiff, xDiff)
    print 'angle: %s' % angle
    turnToTheta(angle, ROT_SPEED)
    moveDist(distance, MOV_SPEED)

def main():
    print("Running...")
    # Initialize the ROS node
    rospy.init_node('move_robot', anonymous=True)

    # Subscribers
    sub_odom = rospy.Subscriber('/odom', Odometry, odomCb)
    sub_path = rospy.Subscriber('/path', Path, pathCb)

    # Initial sleep
    rospy.spin()
    print 'Exiting normally'

if __name__ == '__main__':
    main()
