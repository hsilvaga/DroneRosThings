#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from std_msgs.msg import UInt32

def callbackA(data):
   print("Showing Topic A Data:  %s", data)

def publisher(number):
    print("Publishing numbers!")
    pub1.publish(number)
def main():
    while not rospy.is_shutdown():
        print("Reading!")
        rospy.Subscriber("topic_a", String, callbackA)
        publisher(69)
        rate.sleep()


if __name__=="__main__":
    rospy.init_node("node_b")
    pub1 = rospy.Publisher("topic_b", UInt32, queue_size=10)
    rate = rospy.Rate(10)
    main()