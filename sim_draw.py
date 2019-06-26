from os import _exit

import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Qt5Agg')


# plotlist to make easily plottable using pyplot.plot()
# converts from [(x, y), (x, y), (x, y) ...] to [[x1, x2, ...], [y1, y2, ...]]
class PlotList:
    def __init__(self, nodes):
        self.x = [node.x for node in nodes]
        self.y = [node.y for node in nodes]


# for use in scatter plot in set_offsets()
# converts x and y to lists
# TODO: make this more efficient: can treat original objects as float[]?
class ScatterList:
    def __init__(self, nodes):
        self.xy = [[node.x, node.y] for node in nodes]


# main drawing class
class NetworkPlot:
    def __init__(self, nodes, cars):
        self.nodes = PlotList(nodes)
        self.cars = PlotList(cars)
        self.sim_figure = plt.figure('Network simulation')
        self.nodes_plt = plt.scatter(self.nodes.x, self.nodes.y, s=1000)
        self.cars_plt = plt.scatter(self.cars.x, self.cars.y, s=100)

        plt.show()
        # TODO: fix following line; doesn't work
        self.sim_figure.canvas.mpl_connect('close_event', self.close_handler)

    def update_and_draw(self, cars):
        self.cars = ScatterList(cars)
        self.cars_plt.set_offsets(self.cars.xy)
        plt.draw()

    def close_handler(self, val):
        print('Closing simulation')
        _exit(0)