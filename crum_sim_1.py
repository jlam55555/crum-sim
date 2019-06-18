import numpy as np
import os
from random import randint
from math import sqrt
from time import sleep
from threading import Thread

# plotting imports
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button

# mockup crum
class MockCRUMInterface(object):
    def __init__(self, n):
        self.iter = 0
        self.n = n
        self.vehicles = [randint(0, 2) for x in range(self.n)]
    def travelTimeEdges(self):
        routeCounts = self.countRoutes()
        travelTimeEdgesMap = {
            0: (routeCounts[0] + routeCounts[1]) / 100,
            1: 45,
            2: (routeCounts[1] + routeCounts[2]) / 100,
            3: 45,
            4: 0
        }
        return travelTimeEdgesMap
    def travelTimeRoutes(self):
        edgeTimes = self.travelTimeEdges()
        travelTimeMap = {
            0: edgeTimes[0] + edgeTimes[1],
            1: edgeTimes[0] + edgeTimes[3],
            2: edgeTimes[2] + edgeTimes[3]
        }
        return travelTimeMap
    def countRoutes(self):
        countMap = { 0: 0, 1: 0, 2: 0, 3: 0, 4: 0 }
        for v in self.vehicles:
            countMap[v] += 1
        return countMap
    def advance(self):
        self.iter += 1
        setIterParamText(self.iter)
        print('Advanced to iteration %i' % self.iter)
        self.vehicles = [randint(0, 2) for x in range(self.n)]
        return {
            'iter': self.iter,
            'routeCounts': self.countRoutes(),
            'edgeTimes': self.travelTimeEdges(),
            'routeTimes': self.travelTimeRoutes()
        }
    def reset(self):
        self.iter = 0
        setIterParamText(self.iter)
crumIntf = MockCRUMInterface(50)
print(crumIntf)

# necessary for showing figures in separate window
import matplotlib
matplotlib.use('Qt5Agg')

simFigure = plt.figure('CRUM Traffic Routing Algorithm')

# draw Braess's network
plt.subplot(1, 2, 1)

# let bx (Braess x-pos) be x-position of left and right points (for convenience)
bx = sqrt(3)/2

ls = '-.k'
labels = ['edge 1', 'edge 2', 'edge 3', 'edge 4', 'edge 5']
colors = ['red', 'orange', 'yellow', 'green', 'blue']
edgeCoords = [
    [[-bx, 0], [0, 0.5]],
    [[bx, 0], [0, 0.5]],
    [[-bx, 0], [0, -0.5]],
    [[bx, 0], [0, -0.5]],
    [[0, 0], [-0.5, 0.5]]
]
edges = [plt.plot(edgeCoords[i][0], edgeCoords[i][1], c=colors[i])[0] for i in range(5)]

plt.scatter([-bx, 0, 0, bx], [0, 0.5, -0.5, 0], c='grey')

plt.legend(edges, labels)
plt.axis('equal')
plt.axis('off')

# controlling the algorithm
gParamAxis = plt.axes([0.525, 0.950, 0.200, 0.03])
pParamAxis = plt.axes([0.775, 0.950, 0.200, 0.03])

gParamSlid = Slider(gParamAxis, 'G', 0, 1, valinit=0.5)
pParamSlid = Slider(pParamAxis, 'p', 0, 1, valinit=0.5)

# controlling the simulation
isPlaying = False
resetActionAxis = plt.axes([0.525, 0.900, 0.075, 0.03])
nextActionAxis = plt.axes([0.650, 0.900, 0.075, 0.03])
playActionAxis = plt.axes([0.775, 0.900, 0.200, 0.03])

resetActionButton = Button(resetActionAxis, 'Reset sim')
nextActionButton = Button(nextActionAxis, 'Next step')
playActionButton = Button(playActionAxis, 'Play/Pause')

def resetActionHandler(val):
    setIsPlayingCtrlText(False)
    crumIntf.reset()
    print('Simulation reset')
resetActionButton.on_clicked(resetActionHandler)

def nextActionHandler(val):
    if not isPlaying:
        getNextStep()
nextActionButton.on_clicked(nextActionHandler)

# loop indefinitely in another thread
def loopCrum():
    while 1:
        if isPlaying:
            getNextStep()
        sleep(1)
loopCrumThread = Thread(target=loopCrum, daemon=True)
loopCrumThread.start()

def playActionHandler(val):
    setIsPlayingCtrlText(not isPlaying)
playActionButton.on_clicked(playActionHandler)

# print out variables
isPlayingCtrlAxis = plt.axes([0.01, 0.97, 0.5, 0.03])
isPlayingCtrlText = plt.text(0, 0, 'isPlaying: %r' % isPlaying)
def setIsPlayingCtrlText(val):
    global isPlaying
    isPlaying = val
    isPlayingCtrlText.set_text('isPlaying: %r' % isPlaying)
    plt.draw()

iterParamAxis = plt.axes([0.01, 0.94, 0.5, 0.03])
iterParamText = plt.text(0, 0, 'iter: %i' % 0)
def setIterParamText(val):
    iterParamText.set_text('iter: %i' % val)
    plt.draw()

isPlayingCtrlAxis.axis('off')
iterParamAxis.axis('off')

# showing charts
# % improvement of car flow vs. rounds
plt.subplot(4, 2, 4)
plt.title('Improvement of Car Flow')
plt.plot([], [])

# % improvement of travel time vs. rounds
plt.subplot(4, 2, 6)
plt.title('Improvement of Travel Time')
plt.plot([], [])

# % car flow distribution vs. rounds
plt.subplot(4, 2, 8)
plt.title('Car Flow')
plt.plot([], [])

# advance
def getNextStep():
    stepData = crumIntf.advance()

    print(stepData)

# show figure
simFigure.tight_layout()
plt.show()

# cleanly close all threads when window closed
def closeActionHandler(val):
    print('Closing simulation')
    os._exit(0)
simFigure.canvas.mpl_connect('close_event', closeActionHandler)
