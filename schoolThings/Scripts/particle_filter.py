from HelperScripts.particles import Robot
from HelperScripts.particles import resample
from HelperScripts.particles import eval_set
import math




def main():
    hexBungle = Robot()
    hexBungle.set(30.0, 50.0, math.pi / 2.0)  # sets homebois' local
    hexBungle.set_noise(5.0, 0.1, 5.0) # homeboi gets a little noisey
    #Adds noise factors for forward movement, orientation movement, and sensor noise


    hexBungle = hexBungle.move(-math.pi / 2.0, 15.0) #sets homebois' pose to new local
    print(hexBungle.sense())

    hexBungle = hexBungle.move(-math.pi / 2.0, 10.0)
    print(hexBungle.sense())

    mainBungle = Robot() #homeboi gets a bro
    mainBungle.set_noise(.05, .05, 5.0)

    bunglesArray = []

    for x in range(1000): #making more bois for da fam
        newBungle = Robot()
        newBungle.set_noise(.05, .05, 5.0)
        bunglesArray.append(newBungle)
        print(newBungle.to_string()) #locals of all da new bois

    #for x in range(1000):
    #   print(bunglesArray[x].to_string())

    print(" ", bunglesArray[0].x, bunglesArray[5].x)
    turns = [0.1,0.0, 0.0, 0.3, 0.5]
    forwards = [5.0, 5.0, 2.5, 3.0, 5.0]

    for x in range(len(turns)):

        for y in bunglesArray: #move all de bois
            y = y.move(turns[x], forwards[x])

        weights = [len(bunglesArray)]

        for z in bunglesArray: #makin da bois a bit heavy
            weights.append(z.measurement_prob(z.sense())) #Creating weights for each bungle


        bunglesArray = resample(bunglesArray, weights) #resamples particles based off of weights and beta
        for k in range(10): #prints out the first ten robots pose in the particle set
            print(bunglesArray[k].to_string())

        findMaxMain = []
        for w in range(len(bunglesArray)):
            findMaxMain.append(bunglesArray[w].measurement_prob(bunglesArray[w].sense()))

        mainBoi = findMaxMain.index(max(findMaxMain)) #index of the mainBungle in the resampled bunglesArray
        print("", mainBungle.x, mainBungle.y)
        mainBungle.set(bunglesArray[mainBoi].x, bunglesArray[mainBoi].y, bunglesArray[mainBoi].orientation) #


        print(eval_set(mainBungle, bunglesArray))


if __name__== "__main__":
    main()





