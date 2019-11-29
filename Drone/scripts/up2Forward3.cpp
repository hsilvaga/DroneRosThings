#include <ros/ros.h>
#include "setup.h"
#include <nav_msgs/Odometry.h>
#include <geometry_msgs/TwistStamped.h>


nav_msgs::Odometry odomData;
ros::Publisher posePub;
void odomCall(const nav_msgs::Odometry msg) {
	odomData = msg;
}

geometry_msgs::TwistStamped twistMsg;
void move(double x, double y, double z) {
	twistMsg.twist.linear.x = x;
	twistMsg.twist.linear.y = y;
	twistMsg.twist.linear.z = z;

	posePub.publish(twistMsg);

}

int main(int argc, char **argv) {
	ros::init(argc, argv, "FirstMove");
	ros::NodeHandle h;
	setupc Set;
	ros::Rate rate(30);


	ros::Subscriber odomSub = h.subscribe<nav_msgs::Odometry>
					("/mavros/local_position/odom",10, odomCall);
	posePub = h.advertise<geometry_msgs::TwistStamped>
				("/mavros/setpoint_velocity/cmd_vel",10);

	Set.setup(argc, argv);
	Set.setArm(true);
	Set.setMode();


	while(ros::ok()) {



		while(odomData.pose.pose.position.z <= 5) {
			move(0,0,1);
		}/*
		if(odomData.pose.pose.position.z > 5) {
			move(0,0,0);
		}
		while(odomData.pose.pose.position.x <=4 && odomData.pose.pose.position.z >= 5) {
			move(1,0,0);
		}*/

		ros::spinOnce();
		rate.sleep();
	}


	return 0;
}
