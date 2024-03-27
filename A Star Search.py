# -*- coding: utf-8 -*-
"""Only A* (from week 3)

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1_bWd-BV2mky0SxnDERKkRcOEihc7JA6a
"""

# Commented out IPython magic to ensure Python compatibility.
import math
import numpy as np
# %matplotlib inline
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib import lines

from ipywidgets import interact
import ipywidgets as widgets
from IPython.display import display
import time
import math
import heapq

class Problem(object):
    def __init__(self, initial, goal=None):
        self.initial = initial
        self.goal = goal
    def is_in(self,elt, seq):
        return any(x is elt for x in seq)

    def actions(self, state):
        raise NotImplementedError

    def result(self, state, action):
        raise NotImplementedError

    def goal_test(self, state):
        if isinstance(self.goal, list):
            return self.is_in(state, self.goal)
        else:
            return state == self.goal

    def path_cost(self, c, state1, action, state2):
        return c + 1

    def value(self, state):
        raise NotImplementedError

class Node:
    def __init__(self, state, parent=None, action=None, path_cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.depth = 0
        if parent:
            self.depth = parent.depth + 1

    def __repr__(self):
        return "<Node {}>".format(self.state)

    def __lt__(self, node):
        return self.state < node.state

    def expand(self, problem):
        return [self.child_node(problem, action)
                for action in problem.actions(self.state)]

    def child_node(self, problem, action):
        next_state = problem.result(self.state, action)
        next_node = Node(next_state, self, action,
                    problem.path_cost(self.path_cost, self.state,
                                      action, next_state))
        return next_node

    def solution(self):
        return [node.action for node in self.path()[1:]]

    def path(self):
        node, path_back = self, []
        while node:
            path_back.append(node)
            node = node.parent
        return list(reversed(path_back))
    def __eq__(self, other):
        return isinstance(other, Node) and self.state == other.state

    def __hash__(self):
        return hash(self.state)

class GraphProblem(Problem):
    def __init__(self, initial, goal, graph):
        Problem.__init__(self, initial, goal)
        self.graph = graph
        self.infinity=math.inf
    def distance(self,a, b):
        xA, yA = a
        xB, yB = b
        return np.hypot((xA - xB), (yA - yB))
    def actions(self, A):
        return list(self.graph.get(A).keys())

    def result(self, state, action):
        return action

    def path_cost(self, cost_so_far, A, action, B):
        return cost_so_far + (self.graph.get(A, B) or self.infinity)

    def find_min_edge(self):
        m = self.infinity
        for d in self.graph.graph_dict.values():
            local_min = min(d.values())
            m = min(m, local_min)

        return m

    def h(self, node):
        """h function is straight-line distance from a node's state to goal."""
        locs = getattr(self.graph, 'locations', None)
        if locs:
            if type(node) is str:
                return int(self.distance(locs[node], locs[self.goal]))

            return int(self.distance(locs[node.state], locs[self.goal]))
        else:
            return self.infinity

class Graph:
    def __init__(self, graph_dict=None, directed=True):
        self.graph_dict = graph_dict or {}
        self.directed = directed
        if not directed:
            self.make_undirected()

    def make_undirected(self):
        for a in list(self.graph_dict.keys()):
            for (b, dist) in self.graph_dict[a].items():
                self.connect1(b, a, dist)

    def connect(self, A, B, distance=1):
        self.connect1(A, B, distance)
        if not self.directed:
            self.connect1(B, A, distance)

    def connect1(self, A, B, distance):
        self.graph_dict.setdefault(A, {})[B] = distance

    def get(self, a, b=None):
        links = self.graph_dict.setdefault(a, {})
        if b is None:
            return links
        else:
            return links.get(b)

    def nodes(self):
        s1 = set([k for k in self.graph_dict.keys()])
        s2 = set([k2 for v in self.graph_dict.values() for k2, v2 in v.items()])
        nodes = s1.union(s2)
        return list(nodes)


def UndirectedGraph(graph_dict=None):
    return Graph(graph_dict=graph_dict, directed=False)

# Define the Melbourne map as an undirected graph with distances in km
local_map = UndirectedGraph(dict(
    Royal_Gardens=dict(Roudabout_2=56),
    Cranbourne_Park_Shopping_Centre=dict(Roudabout_2=29, Public_Toilet_2 = 16),
    Intersection_1=dict(Roundabout_1=26, ALDI=19),
    Broad_Oak_Centre=dict(Roundabout_1=7, Intersection_3 = 7),
    Roundabout_1=dict(ALDI=21),
    Roudabout_2=dict(Intersection_1 = 17),
    Intersection_2=dict(Roudabout_2 =13, Monash_Health_Centre=3, Stem_Academic_College=2,Elite_Computer = 0.4, Police_Station=1, Community_Information_Center = 19),
    APCO=dict(Coles_Springhill=19),
    Coles_Springhill=dict(ALDI=37),
    Monash_Health_Centre =dict(Royal_Gardens=48, Hearing_Australia =15),
    ALDI=dict(Woolworths=2),
    Hearing_Australia=dict(Stem_Academic_College=2),
    Elite_Computer=dict(Police_Station=1),
    Public_Toilet=dict(Police_Station=4, Intersection_2=5),
    Public_Toilet_2=dict(Intersection_1 = 18),
    Intersection_3=dict(ALDI=13),
    Shopping_Center_Parking=dict(Cranbourne_Park_Shopping_Centre = 16, Intersection_2 = 14)
))


# Define the locations of each suburb in Melbourne
local_map.locations = dict(
    Royal_Gardens=(145.2691829, -36.7304496),
    Cranbourne_Park_Shopping_Centre=(145.2841866, -36.1089868),
    Intersection_1= (145.2933633, -35.5063795),
    Broad_Oak_Centre=(145.3064638, -37.1015526),
    Roundabout_1=(145.3019334, -34.1033545),
    Roudabout_2=  (145.2899518, -33.1138384),
    Intersection_2=  (145.2829935, -32.1130201),
    APCO=(145.2947391, -32.0941597),
    Coles_Springhill=(145.2928501, -30.0849908),
    Monash_Health_Centre=(145.2716139, -29.1130723),
    Woolworths=(145.2937496, -27.6002),
    ALDI= (145.2988979, -27.100051),
    Hearing_Australia= (145.2721944, -26.1127),
    Stem_Academic_College= (145.2742891, -24.1127675),
    Elite_Computer= (145.2856696,-18.113131),
    Police_Station=  (145.2875418, -23.1133387),
    Community_Information_Center= (145.2781971, -22.193562),
    Public_Toilet= (145.2942854, -21.1144225),
    Public_Toilet_2= (145.2928705, -38.1062415),
    Intersection_3= (145.3021679, -19.0997019),
    Shopping_Center_Parking =(145.28152, -38.11188)
)

# Define the Melbourne problem
local_problem = GraphProblem('Cranbourne_Park_Shopping_Centre', 'Royal_Gardens', local_map)

local_locations = local_map.locations
print(local_locations)

# node colors, node positions and node label positions
node_colors = {node: 'white' for node in local_map.locations.keys()}
node_positions = local_map.locations
node_label_pos = { k:[v[0],v[1]-10]  for k,v in local_map.locations.items() }
edge_weights = {(k, k2) : v2 for k, v in local_map.graph_dict.items() for k2, v2 in v.items()}

local_graph_data = {  'graph_dict' : local_map.graph_dict,
                        'node_colors': node_colors,
                        'node_positions': node_positions,
                        'node_label_positions': node_label_pos,
                         'edge_weights': edge_weights
                     }

def show_map(graph_data, node_colors=None):
    G = nx.Graph(graph_data['graph_dict'])
    node_colors = node_colors or graph_data['node_colors']
    node_positions = graph_data['node_positions']
    node_label_pos = graph_data['node_label_positions']
    edge_weights = graph_data['edge_weights']

    # set the size of the plot
    plt.figure(figsize=(10, 7))
    # draw the graph (both nodes and edges) with locations
    nx.draw(G, pos={k: node_positions[k] for k in G.nodes()},
            node_color=[node_colors[node] for node in G.nodes()], linewidths=0.3, edgecolors='k',with_labels = True)

    # add edge lables to the graph
    nx.draw_networkx_edge_labels(G, pos=node_positions, edge_labels=edge_weights, font_size=14)

    # add a legend
    white_circle = lines.Line2D([], [], color="white", marker='o', markersize=15, markerfacecolor="white")
    orange_circle = lines.Line2D([], [], color="orange", marker='o', markersize=15, markerfacecolor="orange")
    red_circle = lines.Line2D([], [], color="red", marker='o', markersize=15, markerfacecolor="red")
    gray_circle = lines.Line2D([], [], color="gray", marker='o', markersize=15, markerfacecolor="gray")
    green_circle = lines.Line2D([], [], color="green", marker='o', markersize=15, markerfacecolor="green")
    plt.legend((white_circle, orange_circle, red_circle, gray_circle, green_circle),
               ('Un-explored', 'Frontier', 'Currently Exploring', 'Explored', 'Final Solution'),
               numpoints=1, prop={'size': 16}, loc=(.9, .75))

    # show the plot. No need to use in notebooks. nx.draw will show the graph itself.
    plt.show()

show_map(local_graph_data)

def euclidean_distance(self, a, b):
  return math.dist(a, b)

def final_path_colors(initial_node_colors, problem, solution):
    "Return a node_colors dict of the final path provided the problem and solution."

    # get initial node colors
    final_colors = dict(initial_node_colors)
    # color all the nodes in solution and starting node to green
    final_colors[problem.initial] = "green"
    for node in solution:
        final_colors[node] = "green"
    return final_colors

def display_visual(graph_data, user_input, algorithm=None, problem=None):
    initial_node_colors = graph_data['node_colors']
    if user_input is False:
        def slider_callback(iteration):
            # don't show graph for the first time running the cell calling this function
            try:
                show_map(graph_data, node_colors=all_node_colors[iteration])
            except:
                pass

        def visualize_callback(visualize):
            if visualize is True:
                button.value = False

                global all_node_colors

                iterations, all_node_colors, node = algorithm(problem)
                solution = node.solution()
                all_node_colors.append(final_path_colors(all_node_colors[0], problem, solution))

                slider.max = len(all_node_colors) - 1

                for i in range(slider.max + 1):
                    slider.value = i
                    time.sleep(.5)

        slider = widgets.IntSlider(min=0, max=1, step=1, value=0)
        slider_visual = widgets.interactive(slider_callback, iteration=slider)
        display(slider_visual)

        button = widgets.ToggleButton(value=False)
        button_visual = widgets.interactive(visualize_callback, visualize=button)
        display(button_visual)

    if user_input is True:
        node_colors = dict(initial_node_colors)
        if isinstance(algorithm, dict):
            assert set(algorithm.keys()).issubset({"Breadth First Search",
                                                   "Depth First Search",})

            algo_dropdown = widgets.Dropdown(description="Search algorithm: ",
                                             options=sorted(list(algorithm.keys())),
                                             value="Breadth First Tree Search")
            display(algo_dropdown)
        elif algorithm is None:
            print("No algorithm to run.")
            return 0

        def slider_callback(iteration):
            # don't show graph for the first time running the cell calling this function
            try:
                show_map(graph_data, node_colors=all_node_colors[iteration])
            except:
                pass

        def visualize_callback(visualize):
            if visualize is True:
                button.value = False

                problem = GraphProblem(start_dropdown.value, end_dropdown.value, local_map)
                global all_node_colors

                user_algorithm = algorithm[algo_dropdown.value]

                iterations, all_node_colors, node = user_algorithm(problem)
                solution = node.solution()
                all_node_colors.append(final_path_colors(all_node_colors[0], problem, solution))

                slider.max = len(all_node_colors) - 1

                for i in range(slider.max + 1):
                    slider.value = i
                    time.sleep(.5)

        start_dropdown = widgets.Dropdown(description="Start location: ",
                                          options=sorted(list(node_colors.keys())), value="A")
        display(start_dropdown)

        end_dropdown = widgets.Dropdown(description="Goal location: ",
                                        options=sorted(list(node_colors.keys())), value="F")
        display(end_dropdown)

        button = widgets.ToggleButton(value=False)
        button_visual = widgets.interactive(visualize_callback, visualize=button)
        display(button_visual)

        slider = widgets.IntSlider(min=0, max=1, step=1, value=0)
        slider_visual = widgets.interactive(slider_callback, iteration=slider)
        display(slider_visual)

import functools

def memoize(fn, slot=None, maxsize=32):
    """Memoize fn: make it remember the computed value for any argument list.
    If slot is specified, store result in that slot of first argument.
    If slot is false, use lru_cache for caching the values."""

    # Define the memoized function that will be returned
    if slot:
        def memoized_fn(obj, *args):
            # If the object has a slot with the specified name, return its value
            if hasattr(obj, slot):
                return getattr(obj, slot)
            # Otherwise, compute the value of fn and store it in the slot
            else:
                val = fn(obj, *args)
                setattr(obj, slot, val)
                return val
    else:
        # Use the lru_cache decorator to cache the values
        @functools.lru_cache(maxsize=maxsize)
        def memoized_fn(*args):
            return fn(*args)

    # Return the memoized function
    return memoized_fn

def best_first_graph_search_for_vis(problem, f):
    """Search the nodes with the lowest f scores first.
    You specify the function f(node) that you want to minimize; for example,
    if f is a heuristic estimate to the goal, then we have greedy best
    first search; if f is node.depth then we have breadth-first search.
    There is a subtlety: the line "f = memoize(f, 'f')" means that the f
    values will be cached on the nodes as they are computed. So after doing
    a best first search you can examine the f values of the path returned."""

    # we use these two variables at the time of visualisations
    iterations = 0
    all_node_colors = []
    node_colors = {k : 'white' for k in problem.graph.nodes()}

    f = memoize(f, 'f')

    node = Node(problem.initial)

    node_colors[node.state] = "red"
    iterations += 1
    all_node_colors.append(dict(node_colors))

    if problem.goal_test(node.state):#early
        node_colors[node.state] = "green"
        iterations += 1
        all_node_colors.append(dict(node_colors))
        return(iterations, all_node_colors, node)

    frontier = PriorityQueue('min', f)
    frontier.append(node)

    node_colors[node.state] = "orange"
    iterations += 1
    all_node_colors.append(dict(node_colors))

    explored = set()
    while frontier:
        node = frontier.pop()

        node_colors[node.state] = "red"
        iterations += 1
        all_node_colors.append(dict(node_colors))

        #goal test before the expansion of child nodes
        if problem.goal_test(node.state):
            node_colors[node.state] = "green"
            iterations += 1
            all_node_colors.append(dict(node_colors))
            return(iterations, all_node_colors, node)

        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
                node_colors[child.state] = "orange"
                iterations += 1
                all_node_colors.append(dict(node_colors))
            elif child in frontier:
              #the currently best-known solution node-incumbent
                incumbent = frontier[child]
                if f(child) < incumbent:
                    del frontier[child]
                    frontier.append(child)
                    node_colors[child.state] = "orange"
                    iterations += 1
                    all_node_colors.append(dict(node_colors))

        node_colors[node.state] = "gray"
        iterations += 1
        all_node_colors.append(dict(node_colors))
    return None

class PriorityQueue:
    """A Queue in which the minimum (or maximum) element (as determined by f and
    order) is returned first.
    If order is 'min', the item with minimum f(x) is
    returned first; if order is 'max', then it is the item with maximum f(x).
    Also supports dict-like lookup."""

    def __init__(self, order='min', f=lambda x: x):
        self.heap = []
        if order == 'min':
            self.f = f
        elif order == 'max':  # now item with max f(x)
            self.f = lambda x: -f(x)  # will be popped first
        else:
            raise ValueError("Order must be either 'min' or 'max'.")

    def append(self, item):
        """Insert item at its correct position. single element"""
        heapq.heappush(self.heap, (self.f(item), item))

    def extend(self, items):
        """Insert each item in items at its correct position.multiple element"""
        for item in items:
            self.append(item)

    def pop(self):
        """Pop and return the item (with min or max f(x) value)
        depending on the order."""
        if self.heap:
            return heapq.heappop(self.heap)[1]
        else:
            raise Exception('Trying to pop from empty PriorityQueue.')

    def __len__(self):
        """Return current capacity of PriorityQueue."""
        return len(self.heap)

    def __contains__(self, key):
        """Return True if the key is in PriorityQueue."""
        return any([item == key for _, item in self.heap])

    def __getitem__(self, key):
        """Returns the first value associated with key in PriorityQueue.
        Raises KeyError if key is not present."""
        for value, item in self.heap:
            if item == key:
                return value
        raise KeyError(str(key) + " is not in the priority queue")

    def __delitem__(self, key):
        """Delete the first occurrence of key."""
        try:
            del self.heap[[item == key for _, item in self.heap].index(True)]
        except ValueError:
            raise KeyError(str(key) + " is not in the priority queue")
        heapq.heapify(self.heap)

def astar_search(problem, h=None):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    iterations, all_node_colors, node = best_first_graph_search_for_vis(problem,lambda node: node.path_cost + h(node))
    return(iterations, all_node_colors, node)

all_node_colors = []
#startLocation = input("Starting Location?: ")   #start point input
#endLocation = input("Destination?: ")   #end point input
#local_problem = GraphProblem(startLocation, endLocation, local_map)
local_problem = GraphProblem('Cranbourne_Park_Shopping_Centre', 'Royal_Gardens', local_map)
display_visual(local_graph_data, user_input=False,
               algorithm=astar_search,
               problem=local_problem)