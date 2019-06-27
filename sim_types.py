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

    def get_coords(self, routePos):
        return [
            self.start.x + routePos*(self.end.x - self.start.x),
            self.start.y + routePos*(self.end.y - self.start.y)
        ]

    # routePos is a number in the interval [0, 1]
    def next_coords(self, routePos, interval):
        routePos += self.currentStep * interval
        return [routePos, *self.get_coords(routePos)]


class Route:
    def __init__(self, edges):
        self.edges = edges
        self.length = len(edges)


class Car(Node):
    def __init__(self, route, is_crum):
        # TODO: change coordinates to network origin
        super().__init__(0, 0)
        self.route = route
        self.route_edge = 0
        self.route_pos = 0
        self.is_crum = is_crum
        self.finished = False

    def advance(self, interval):
        current_edge = self.route.edges[self.route_edge]
        # TODO: make this more efficient (don't fully recalculate after every step)
        self.route_pos, self.x, self.y = current_edge.next_coords(self.route_pos, interval)

        if self.route_pos >= 1:
            if self.route_edge >= self.route.length - 1:
                self.finished = True
            else:
                # TODO: improve this to include moving after it reaches the intersection
                self.route_edge += 1
                self.route_pos = 0
