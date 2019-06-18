# math imports
import numpy as np
from math import sqrt

# necessary for showing figures in separate window
import matplotlib
matplotlib.use('Qt5Agg')

# plotting imports
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button

plt.figure('Traffic Algorithm Visualization')

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
resetActionAxis = plt.axes([0.525, 0.900, 0.075, 0.03])
nextActionAxis = plt.axes([0.650, 0.900, 0.075, 0.03])
playActionAxis = plt.axes([0.775, 0.900, 0.200, 0.03])

resetActionButton = Button(resetActionAxis, 'Next Step')
nextActionButton = Button(nextActionAxis, 'Reset Sim')
playActionButton = Button(playActionAxis, 'Play/Pause')

def resetActionHandler():
    pass;
resetActionButton.on_clicked(resetActionHandler)

def nextActionHandler():
    pass;
nextActionButton.on_clicked(nextActionHandler)

def playActionHandler():
    pass;
resetActionButton.on_clicked(playActionHandler)

# show figure
plt.show()
