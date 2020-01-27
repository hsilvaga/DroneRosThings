#!/usr/bin/env python


import rospy
import numpy as np
import tf2_ros
from geometry_msgs.msg import TransformStamped
import tf_conversions
import math

def main():
    print "Starting"

    # rotation around z-axis
    transMat = np.mat('1.0 0.0 0.0 2.0;0.0 1.0 0.0 3.0; 0.0 0.0 1.0 0.0; 0.0 0.0 0.0 1.0')
    transMat[0, 0] = math.cos(math.radians(45))
    transMat[0, 1] = -math.sin(math.radians(45))
    transMat[1, 0] = math.sin(math.radians(45))
    transMat[1, 1] = math.cos(math.radians(45))
    #basic rotation about z-axis
    tranny = convertMatToTf(transMat)
    tranny.header.frame_id= "World"
    tranny.child_frame_id = "My_ID"

    #translation function
    tranny2 = translate(1,2,1)
    tranny2.header.frame_id="World"
    tranny2.child_frame_id= "tranTest"

    #transformation 3: Rotates about x axis
    tranny3 = convertMatToTf(rotateX(math.radians(45.0))) #rotate matrix 45 degress about x-axis
    tranny3.header.frame_id="World"
    tranny3.child_frame_id= "rotateX"

    #transformation 4: Rotates about every axis
    tranny4 = convertMatToTf(rotateXYZ(math.radians(45.0),math.radians(45.0),math.radians(45.0)))
    tranny4.header.frame_id = "World"
    tranny4.child_frame_id = "RotateAll"

    tranny5 = convertMatToTf((transform(1.0, 2.0, 0.0, 45.0, 0.0,45.0)))
    tranny5.header.frame_id= "World"
    tranny5.child_frame_id="Transformer"

    print("Sending Transformation...")
    while not rospy.is_shutdown():
        #br.sendTransform(tranny)
        #br.sendTransform(tranny2)
        br.sendTransform(tranny3)
        #br.sendTransform(tranny4)
        br.sendTransform(tranny5)
        rate.sleep()


def transform(x, y, z, rotX, rotY, rotZ):
    mat = rotateXYZ(math.radians(rotX), math.radians(rotY), math.radians(rotZ))

    mat[0,3] = x
    mat[1,3] = y
    mat[2,3] = z

    return mat

#Rotates about the X axis
def rotateX(theta):
    xRot = np.mat('1.0 0.0 0.0 0.0; 0.0 1.0 0.0 0.0; 0.0 0.0 1.0 0.0; 0.0 0.0 0.0 1.0')

    xRot[1,1] = math.cos(theta)
    xRot[1,2] = -math.sin(theta)
    xRot[2,1] = math.sin(theta)
    xRot[2,2] = math.cos(theta)

    return xRot

#rotates about the Y axis
def rotateY(theta):
    yRot = np.mat('1.0 0.0 0.0 0.0; 0.0 1.0 0.0 0.0; 0.0 0.0 1.0 0.0; 0.0 0.0 0.0 1.0')

    yRot[0,0] = math.cos(theta)
    yRot[0,2] = math.sin(theta)
    yRot[2,0] = -math.sin(theta)
    yRot[2,2] = math.cos(theta)

    return yRot

#Rotates about the Z axis
def rotateZ(theta):
    zRot = np.mat('1.0 0.0 0.0 0.0; 0.0 1.0 0.0 0.0; 0.0 0.0 1.0 0.0; 0.0 0.0 0.0 1.0')

    zRot[0,0]= math.cos(theta)
    zRot[0,1] = -math.sin(theta)
    zRot[1,0] = math.sin(theta)
    zRot[1,1] = math.cos(theta)

    return zRot

#Rotates about the X, Y, and Z axis
def rotateXYZ(rotX, rotY, rotZ):
    rotXYZ = np.mat('1.0 0.0 0.0 0.0; 0.0 1.0 0.0 0.0; 0.0 0.0 1.0 0.0; 0.0 0.0 0.0 1.0')

    matZ = rotateZ(rotZ)
    matY = rotateY(rotY)
    matX = rotateX(rotX)

    matZ = np.matmul(matZ,  matY)
    matX = np.matmul(matZ, matX)

    return matX

#Moves in the X, Y, and Z position; returns a translated matrix
def translate(x, y, z):
    translation = np.mat('1.0 0.0 0.0 0.0; 0.0 1.0 0.0 0.0; 0.0 0.0 1.0 0.0; 0.0 0.0 0.0 1.0')
    translation[0,3] = x
    translation[1,3] = y
    translation[2,3] = z

    tranny2 = convertMatToTf(translation)

    return tranny2

# mat is a 4x4 numpy array
def convertMatToTf(mat):
    result = TransformStamped()

    # Translation is set based on position vector in transformation matrix
    result.transform.translation.x = mat[0, 3]
    result.transform.translation.y = mat[1, 3]
    result.transform.translation.z = mat[2, 3]

    ###########################################################
    # Get the rotation values around each axis
    ###########################################################

    # If rotation around y is 90 or -90
    if (mat[2, 0] >= -1.01 and mat[2, 0] <= -0.99) or (mat[2, 0] >= 0.99 and mat[2, 0] <= 1.01):

        # Set rot_z to anything, usually 0 is selected
        rot_z = 0.0
        if (mat[2, 0] >= -1.01 and mat[2, 0] <= -0.99):
            rot_y = math.pi / 2.0
            rot_x = rot_z + math.atan2(mat[0, 1], mat[0, 2])
        else:
            rot_y = -math.pi / 2.0
            rot_x = -rot_z + math.atan2(-mat[0, 1], -mat[0, 2])

    # Else, rot around y is not 90,-90
    else:
        rot_y = -math.asin(mat[2, 0])
        # rot_y_2 = math.pi - rot_y

        rot_x = math.atan2(mat[2, 1] / math.cos(rot_y), mat[2, 2] / math.cos(rot_y))
        # rot_x_2 = math.atan2(mat[2][1] / math.cos(rot_y_2), mat[2][2] / math.cos(rot_y_2))

        rot_z = math.atan2(mat[1, 0] / math.cos(rot_x), mat[0, 0] / math.cos(rot_x))
        # rot_z_2 = math.atan2( mat[1][0] / math.cos(rot_x_2), mat[0][0] / math.cos(rot_x_2))

    # Get a Quaternion based on the euler angle rotations
    q = tf_conversions.transformations.quaternion_from_euler(rot_x, rot_y, rot_z)

    # Set rotation
    result.transform.rotation.x = q[0]
    result.transform.rotation.y = q[1]
    result.transform.rotation.z = q[2]
    result.transform.rotation.w = q[3]

    return result

if __name__=='__main__':
    rospy.init_node("geo_trans", anonymous=True)
    rate = rospy.Rate(30)

    br =tf2_ros.TransformBroadcaster()
    main()
