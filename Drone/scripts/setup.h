#ifndef __SETUP_INCLUDED__
#define __SETUP_INCLUDED__

#include <ros/ros.h>
#include <geometry_msgs/PoseStamped.h>
#include <mavros_msgs/CommandBool.h>
#include <mavros_msgs/State.h>
#include <mavros_msgs/SetMode.h>
#include <string.h>

class setupc {
public:
	mavros_msgs::State currentState;

	ros::Subscriber stateSub;
	ros::Publisher posPub;
	ros::ServiceClient armSrv;
	ros::ServiceClient modeSrv;


	void stateCall(const mavros_msgs::State::ConstPtr& msg) {
		currentState = *msg; //stores all state data in currentState
	}

	void setup(int argc, char **argv) {
		ros::init(argc,argv, "Drone_Setup");
		ros::NodeHandle nh;
		ros::Rate rate(30);

		stateSub = nh.subscribe<mavros_msgs::State>("/mavros/state", 10, &setupc::stateCall,this);
		posPub = nh.advertise<geometry_msgs::PoseStamped>("/mavros/setpoint_position/local", 10);
		armSrv = nh.serviceClient<mavros_msgs::CommandBool>("/mavros/cmd/arming");
		modeSrv = nh.serviceClient<mavros_msgs::SetMode>("mavros/set_mode");




	}


	void setMode(){ //const std::string& mode
		ros::Rate rate(30);
		bool exit = true;

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
		setMode.request.custom_mode = "OFFBOARD";

		ros::Time lastRequest = ros::Time::now();

		while(ros::ok() && exit) {
			if(currentState.mode != "OFFBOARD" //if mode hasnt been set yet and its been longer than X seconds
					&& (ros::Time::now() - lastRequest > ros::Duration(5.0))) {
				if(modeSrv.call(setMode) && setMode.response.mode_sent) { //send the mode and if received
					ROS_INFO("Offboard enabled");
					exit = false;
				}
				lastRequest = ros::Time::now();
			}
			ROS_INFO("fuck!?!?!??!");
			//ros::spinOnce();
			rate.sleep();
		}
	}

	void setArm(bool arm) {
		ros::Rate rate(30);

		mavros_msgs::CommandBool setArm;
		setArm.request.value = arm;

		ros::Time lastRequest = ros::Time::now();
		bool exit = true;

		while(ros::ok() && exit) {
			if(!currentState.armed && (ros::Time::now() - lastRequest) > ros::Duration(5.0)) {
				if(armSrv.call(setArm) && setArm.response.success) {
					ROS_INFO("Drone Armed");
					exit = false;
				}
				lastRequest = ros::Time::now();
			}
			ROS_INFO("WHY!?!?!?!?");
			ros::spinOnce();
			rate.sleep();
		}


	}

//	void setOff&Arm() {


	//}
};
#endif
