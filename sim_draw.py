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
# TODO: make this more efficient: can treat original objects as a list?
class ScatterList:
    def __init__(self, nodes):
        self.xy = [[node.x, node.y] for node in nodes]

    @staticmethod
    def split_categories(nodes, cat):
        # TODO: change to switch or something later
        res = []

        # option 0: sort by CRUM / not CRUM
        if cat == 0:
            res.append(filter(lambda node : node.is_crum, nodes))
            res.append(filter(lambda node : not node.is_crum, nodes))

        return res

# main drawing class
class NetworkPlot:
    def __init__(self, nodes, cars):
        print('Starting simulation')
        self.nodes = PlotList(nodes)
        self.cars = PlotList(cars)
        self.sim_figure = plt.figure('Network simulation')

        self.ax = plt.gca()
        self.nodes_plt = self.ax.scatter(self.nodes.x, self.nodes.y, s=1000)
        # self.cars_plt = self.ax.scatter(self.cars.x, self.cars.y, s=100)
        self.cars_plt = []
        datasets = ScatterList.split_categories(cars, 0)
        for dataset in datasets:
            plot_list = PlotList(dataset)
            self.cars_plt.append(self.ax.scatter(plot_list.x, plot_list.y, s=100))

        plt.axis('off')
        plt.show()
        self.sim_figure.canvas.mpl_connect('close_event', self.close_handler)

    # TODO: expand datasets ability
    def update_and_draw(self, cars):
        # self.cars = ScatterList(cars)
        # self.cars_plt.set_offsets(self.cars.xy)
        datasets = ScatterList.split_categories(cars, 0)
        for i, dataset in enumerate(datasets):
            # TODO: fix error with this line
            self.cars_plt[i].set_offsets(ScatterList(dataset).xy)
        plt.draw()

    def close_handler(self, val):
        print('Closing simulation')
        _exit(0)