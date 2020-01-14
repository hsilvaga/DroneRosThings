#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from std_msgs.msg import UInt32

def publish(thing):
    pub.publish(thing)

def callbackB(data):
    print("Number from topic B: %i", data)

def main():
    while not rospy.is_shutdown():
        print("Publishing!")
        publish("what now?")
        rospy.Subscriber("topic_b", UInt32, callbackB)
        rate.sleep()


if __name__ =="__main__":
    rospy.init_node("node_a")
    pub = rospy.Publisher('topic_a', String, queue_size=10)
    rate = rospy.Rate(10)

    main()