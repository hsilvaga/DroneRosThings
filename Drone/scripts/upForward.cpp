#include <ros/ros.h>
#include <geometry_msgs/PoseStamped.h>
#include <mavros_msgs/CommandBool.h>
#include <mavros_msgs/State.h>
#include <mavros_msgs/SetMode.h>


mavros_msgs::State currentState;
void stateCall(const mavros_msgs::State::ConstPtr& msg) {
	currentState = *msg; //stores all state data in currentState
}
int main(int argc, char **argv) {
	ros::init(argc, argv,"setupDrone");
	ros::NodeHandle nh;
	ros::Rate rate(30.0);

	ros::Subscriber stateSub = nh.subscribe<mavros_msgs::State>("/mavros/state", 10, stateCall);
	ros::Publisher posPub = nh.advertise<geometry_msgs::PoseStamped>("/mavros/setpoint_position/local", 10);
	ros::ServiceClient armSrv = nh.serviceClient<mavros_msgs::CommandBool>("/mavros/cmd/arming");
	ros::ServiceClient modeSrv = nh.serviceClient<mavros_msgs::SetMode>("mavros/set_mode");



	while(ros::ok() && !currentState.connected) {
		ros::spinOnce();
		rate.sleep();
	}

	geometry_msgs::PoseStamped sendPose;
	sendPose.pose.position.x = 0;
	sendPose.pose.position.y = 0;
	sendPose.pose.position.z = 2;

	for(int i = 0; ros::ok() && i < 100; i++) {
		posPub.publish(sendPose);
		ros::spinOnce();
		rate.sleep();
	}

	mavros_msgs::SetMode setMode;
	setMode.request.custom_mode = "OFFBOARD"; //Creates a SetMode srv-msg with offboard string

	mavros_msgs::CommandBool setArm;
	setArm.request.value = true;

	ros::Time lastRequest = ros::Time::now();

	while(ros::ok()) {
		if(currentState.mode != "OFFBOARD" //if mode hasnt been set yet and its been longer than X seconds
				&& (ros::Time::now() - lastRequest > ros::Duration(1.0))) {
			if(modeSrv.call(setMode) && setMode.response.mode_sent) { //send the mode and if received
				ROS_INFO("Offboard enabled");
			}
			lastRequest = ros::Time::now();
		}
		else {
			if(!currentState.armed &&
					(ros::Time::now() - lastRequest) > ros::Duration(1.0)) {
				if(armSrv.call(setArm) && setArm.response.success) {
					ROS_INFO("Drone Armed");
				}
				lastRequest = ros::Time::now();
			}

		}
		ros::spinOnce();
		rate.sleep();
	}

	return 0;
}

