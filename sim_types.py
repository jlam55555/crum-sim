from math import sqrt


# node is synonymous with point
# named node b/c of use with intersections, but can also be used with cars
class Node:
    def __init__(self, x, y):
        self.set_xy(x, y)

    def dist_from(self, p2):
        return sqrt((self.x - p2.x)**2 + (self.y - p2.y)**2)

    def set_xy(self, x, y):
        self.x = x
        self.y = y


class Edge:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.length = start.dist_from(end)
        self.latency = None
        self.currentStep = None

    def set_latency(self, latency):
        self.latency = latency
        self.currentStep = 1 / self.latency

    # routePos is a number in the interval [0, 1]
    def getCoords(self, routePos):
        routePos += self.currentStep
        x = self.start.x + routePos*(self.end.x - self.start.x)
        y = self.start.y + routePos*(self.end.y - self.start.y)
        return [routePos, x, y]


class Route:
    def __init__(self, edges):
        self.edges = edges
        self.length = len(edges)


class Car(Node):
    def __init__(self, route, is_crum=False):
        # TODO: change coordinates to network origin
        super().__init__(0, 0)
        self.route = route
        self.routeEdge = 0
        self.routePos = 0
        self.is_crum = is_crum
        self.finished = False

    def advance(self):
        currentEdge = self.route.edges[self.routeEdge]
        # TODO: make this more efficient (don't fully recalculate after every step)
        self.routePos, self.x, self.y = currentEdge.getCoords(self.routePos)

        if self.routePos >= 1:
            if self.routeEdge >= self.route.length - 1:
                self.finished = True
            else:
                self.routeEdge += 1
                self.edgePos = 0
