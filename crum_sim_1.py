import numpy as np
import os
from math import sqrt
from time import sleep
from threading import Thread

# plotting imports
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button

# mockup crum
class CRUMInterface:
    iter = 0
    def advance(self):
        self.iter += 1
        print('Advanced to iteration %i' % self.iter)
    def reset(self):
        self.iter = 0
crumIntf = CRUMInterface()

# necessary for showing figures in separate window
import matplotlib
matplotlib.use('Qt5Agg')

simFigure = plt.figure('Traffic Algorithm Visualization')

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
    global isPlaying
    isPlaying = False
    crumIntf.reset()
    print('Simulation reset')
resetActionButton.on_clicked(resetActionHandler)

def nextActionHandler(val):
    if not isPlaying:
        crumIntf.advance()
nextActionButton.on_clicked(nextActionHandler)

# loop indefinitely in another thread
def loopCrum():
    while 1:
        if isPlaying:
            crumIntf.advance()
        sleep(1)
loopCrumThread = Thread(target=loopCrum, daemon=True)
loopCrumThread.start()

def playActionHandler(val):
    global isPlaying
    isPlaying = not isPlaying
    print('Changed isPlaying: %r' % isPlaying)
playActionButton.on_clicked(playActionHandler)

# show figure
plt.show()

# cleanly close all threads when window closed
def closeActionHandler(val):
    print('Closing simulation')
    os._exit(0)
simFigure.canvas.mpl_connect('close_event', closeActionHandler)
