# imports
from math import sqrt
from random import randint, random
from threading import Thread
from time import sleep

# define network types
from sim_types import Node, Edge, Route, Car

# drawing class
from sim_draw import NetworkPlot

# define the network
# this can be adjusted to create different networks
# TODO: rename nodes to intersections (inters?)
nodes = [
    Node(-1, 0),
    Node(0, 1),
    Node(1, 0),
    Node(0, -1)
]
edges = [
    Edge(nodes[0], nodes[1]),
    Edge(nodes[1], nodes[2]),
    Edge(nodes[0], nodes[3]),
    Edge(nodes[3], nodes[2]),
    Edge(nodes[1], nodes[3])
]
routes = [
    Route([edges[0], edges[1]]),
    Route([edges[2], edges[3]]),
    Route([edges[0], edges[4], edges[3]])
]

# cars the array of vehicles currently in the simulation
# note that this cannot be all n cars because their timings are different
cars = []

# play one step of the simulation
# let latencies be defined in number of time-steps
# play_step is supposed to be called with every new car entering
rate = 5            # adjustable rate of car input (# per second)
fps = 30            # adjustable rate of animation update
                    # make sure rate is a factor of fps
interval = 1/fps
cnt = 0


def play_step(car, networkData):
    # update latencies
    # for i, latency in enumerate(networkData.latencies):
    #     edges[i].latency = latency

    # add new car if correct timing (once per second)
    if (cnt * rate) % fps == 0:
        cars.append(car)

    # move cars, delete if finished
    for i, car in enumerate(cars):
        car.advance(interval)
        if car.finished:
            del cars[i]

    # draw
    network_plot.update_and_draw(cars)


# set arbitrary edge latencies for testing
edges[0].set_latency(10)
edges[1].set_latency(5)
edges[2].set_latency(3)
edges[3].set_latency(10)
edges[4].set_latency(2)

# run drawing (on main thread)
network_plot = NetworkPlot(nodes, cars)


# begin simulation on another thread
def loop_step():
    global cnt
    while 1:
        # right now create cars randomly (also random CRUM with arbitrary p=0.1)
        play_step(Car(routes[randint(0, 2)], random() > 0.9), None)
        cnt += 1
        sleep(interval)
loop_step_thread = Thread(target=loop_step, daemon=True)
loop_step_thread.start()
