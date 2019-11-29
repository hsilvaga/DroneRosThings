#!/usr/bin/env python2

import rospy
from mavros_msgs.srv import SetMode, CommandBool
from mavros_msgs.msg import State
from urllib3.connectionpool import xrange


class MavrosSetUP():

    def __init__(self):
        print("Mav setup initiating")


    def setUp(self):
        self.state = State()
        timeout = 30

        print("Waiting for ROS Services")

        try:
            rospy.wait_for_service('/mavros/cmd/arming',timeout)
            rospy.wait_for_service('/mavros/set_mode', timeout)
        except rospy.ROSException:
            print("Failed to connect to services")

        self.setModeSRV = rospy.ServiceProxy('/mavros/set_mode', SetMode)
        self.setArmSRV = rospy.ServiceProxy('/mavros/cmd/arming', CommandBool)

        rospy.Subscriber('/mavros/state', State, self.stateCall)

    def set_arm(self, arm, timeout): #Function that arms the quad
        """arm: True to arm or False to disarm, timeout(int): seconds"""
        rospy.loginfo("setting FCU arm: {0}".format(arm))
        old_arm = self.state.armed
        loop_freq = 1  # Hz
        rate = rospy.Rate(loop_freq)
        arm_set = False
        for i in xrange(timeout * loop_freq):
            if self.state.armed == arm:
                arm_set = True
                rospy.loginfo("set arm success | seconds: {0} of {1}".format(
                    i / loop_freq, timeout))
                break
            else:
                try:
                    res = self.setArmSRV(arm)
                    if not res.success:
                        rospy.logerr("failed to send arm command")
                except rospy.ServiceException as e:
                    rospy.logerr(e)

    def set_mode(self, mode, timeout):
        """mode: PX4 mode string, timeout(int): seconds"""
        rospy.loginfo("setting FCU mode: {0}".format(mode))
        old_mode = self.state.mode
        loop_freq = 3  # Hz
        rate = rospy.Rate(loop_freq)
        mode_set = False
        for i in xrange(timeout * loop_freq):
            print(self.state.mode, mode)
            if self.state.mode == mode:
                mode_set = True
                rospy.loginfo("set mode success | seconds: {0} of {1}".format(
                    i / loop_freq, timeout))
                break
            else:
                try:
                    print("setting mode")
                    res = self.setModeSRV(0, mode)  # 0 is custom mode
                    if not res.mode_sent:
                        print("#######################")
                        rospy.logerr("failed to send mode command")
                except rospy.ServiceException as e:
                    rospy.logerr(e)

            try:
                rate.sleep()
            except rospy.ROSException as e:
                self.fail(e)

    def stateCall(self, state_data):
        self.state = state_data