#!/usr/bin/env python
import rospy
import random
from nav_msgs.msg import OccupancyGrid
from roadmaps_practice.msg import GridInfo, ObPixels



# Creates an OccupancyGrid object with specified width, height, and resolution
def createGrid(width, height, resolution=0.5):
    # Create the object
    grid = OccupancyGrid()

    # Set the fields
    grid.info.width = width
    grid.info.height = height
    grid.info.resolution = resolution

    # Populate the data array with all 0s
    for r in range(0,height):
        for c in range(0,width):
            v = 0
            grid.data.append(v)

    # Return the grid
    return grid


# Changes the grid given obstacle info
# Returns an ObPixels object containing indices of the obstacle pixels
def setRectOb(grid, x, y, width, height):
    #print 'In setRectOb, x: %s y: %s width: %s height: %s' % (x, y, width, height)

    # Create object
    obPixels = ObPixels()

    # For width and height
    for r in range(0,width):
        for c in range(0,height):
            # Get index on map
            i = ((r+y)*grid.info.width)+c+x
            print 'r: %s c: %s i: %s' % (r, c, i)

            # Check for bounds, set the pixel on the grid, and store the index
            if (i < len(grid.data)):
                grid.data[i] = 100
                obPixels.i_pixels.append(i)

    # Return the obstacle pixel information
    return obPixels
            

def main():
    print 'In main'
    rospy.init_node('pubGrid', anonymous=False)

    # Make two Publisher objects
    pub = rospy.Publisher('/map', OccupancyGrid, queue_size=100)
    pub_info = rospy.Publisher('/mapInfo', GridInfo, queue_size=100)

    # 400 - 20m square
    # 200 - 10m square
    # 100 - 5m square
    grid = createGrid(40,40,0.05)

    # Create some random obstacles
    num_obs = 2
    obs = []
    for i in range(0,num_obs):

        # Create an obstacle with random (x,y), width, and height
        w = random.randint(3, 10)
        h = random.randint(3, 10)
        x = random.randint(0, grid.info.width-w-1)
        y = random.randint(0, grid.info.height-h-1)

        # Set the pixels
        pixels = setRectOb(grid, x, y, w, h)
        obs.append(pixels)

    # Create the GridInfo object
    gridInfo = GridInfo()

    # Set the fields
    gridInfo.grid = grid
    gridInfo.obs = obs

    # Sleep
    rospy.sleep(0.5)

    # Publish to /mapInfo (GridInfo) and /map (OccupancyGrid)
    pub.publish(gridInfo.grid)
    pub_info.publish(gridInfo)




if __name__ == '__main__':
    main()
    print('\nExiting normally')
