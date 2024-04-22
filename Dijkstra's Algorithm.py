# -*- coding: utf-8 -*-
"""222486984_assignment1_solution

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1_bWd-BV2mky0SxnDERKkRcOEihc7JA6a
"""

# Commented out IPython magic to ensure Python compatibility.
#First, import the necessary libraries
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
import functools

import sys

##Code Reference: (nolfonzo, 2010)

def shortestDijkstraPath(graph, start, end, visited=[], distances={}, predecessors={}):
    """Find the shortest path between start & end nodes in a graph using Dijkstra's algorithm"""
    # detect if first time through, set current distance to zero
    if not visited:
        distances[start] = 0
    # if we've found our end node, find the path to it, and return
    if start == end:
        path = []
        while end is not None:
            path.append(end)
            end = predecessors.get(end, None)
        return distances[start], path[::-1]
    # process neighbors as per algorithm, keep track of predecessors
    for neighbor in graph[start]:
        if neighbor not in visited:
            neighbordist = distances.get(neighbor, sys.maxsize)
            tentativedist = distances[start] + graph[start][neighbor]
            if tentativedist < neighbordist:
                distances[neighbor] = tentativedist
                predecessors[neighbor] = start
    # neighbors processed, now mark the current node as visited
    visited.append(start)
    # finds the closest unvisited node to the start
    unvisiteds = {k: distances.get(k, sys.maxsize) for k in graph if k not in visited}
    closestnode = min(unvisiteds, key=unvisiteds.get)
    # now take the closest node and recurse, making it current
    return shortestDijkstraPath(graph, closestnode, end, visited, distances, predecessors)

# Define the local_map, representing locations and their connected nodes with distances in between them.
#This is a dictionary for a directed graph
local_map = {
    'Royal_Gardens': {'Roundabout_2': 56, 'Monash_Health_Centre': 48},
    'Cranbourne_Park_Shopping_Centre': {'Roundabout_2': 29, 'Public_Toilet_2': 16, 'Shopping_Center_Parking': 16},
    'Intersection_1': {'Roundabout_1': 26, 'ALDI': 19, 'Roundabout_2': 17,'Public_Toilet_2': 18},
    'Broad_Oak_Centre': {'Roundabout_1': 7, 'Intersection_3': 7},
    'Roundabout_1': {'ALDI': 21, 'Intersection_1': 26, 'Broad_Oak_Centre': 7},
    'Roundabout_2': {'Intersection_1': 17, 'Royal_Gardens': 56, 'Cranbourne_Park_Shopping_Centre': 29, 'Intersection_2': 13},
    'Intersection_2': {
        'Roundabout_2': 13, 'Monash_Health_Centre': 3, 'Stem_Academic_College': 2,
        'Elite_Computer': 4, 'Police_Station': 1, 'Community_Information_Center': 19, 'Hearing_Australia': 2,
        'Public_Toilet': 5, 'Shopping_Center_Parking': 14
    },
    'Police_Station': {'Intersection_2': 1, 'Elite_Computer': 1, 'Public_Toilet': 4},
    'Community_Information_Center': {'Intersection_2': 19, 'Elite_Computer': 4, 'Girl_Guides_Hall': 1},
    'Woolworths': {'ALDI': 2,'Public_Toilet': 30, 'Retirement_Home': 11},
    'APCO': {'Coles_Springhill': 19},
    'St_Agatha_Primary_School': {'Saint_Agatha_Parish': 8, 'Girl_Guides_Hall': 4},
    'Coles_Springhill': {'ALDI': 37, 'APCO': 19},
    'Stem_Academic_College': {'Hearing_Australia': 2, 'Intersection_2': 2},
    'Monash_Health_Centre': {
        'Royal_Gardens': 48, 'Hearing_Australia': 15, 'Saint_Agatha_Parish': 6, 'Intersection_2': 3
    },
    'ALDI': {'Woolworths': 2, 'Intersection_1': 19, 'Roundabout_1': 21, 'Coles_Springhill': 37, 'Intersection_3': 13},
    'Hearing_Australia': {'Stem_Academic_College': 2, 'Intersection_2': 2, 'Monash_Health_Centre': 15},
    'Elite_Computer': {'Police_Station': 1, 'Community_Information_Center': 4, 'Intersection_2': 4},
    'Public_Toilet': {'Police_Station': 4, 'Intersection_2': 5, 'Woolworths': 30},
    'Public_Toilet_2': {'Intersection_1': 18, 'Cranbourne_Park_Shopping_Centre': 16},
    'Intersection_3': {'ALDI': 13, 'Broad_Oak_Centre': 7, 'Retirement_Home': 18},
    'Shopping_Center_Parking': {'Cranbourne_Park_Shopping_Centre': 16, 'Intersection_2': 14},
    'Saint_Agatha_Parish': {'St_Agatha_Primary_School': 8, 'Monash_Health_Centre': 6, 'Girl_Guides_Hall': 5},
    'Girl_Guides_Hall': {
        'Community_Information_Center': 1, 'Saint_Agatha_Parish': 5, 'St_Agatha_Primary_School': 4
    },
    'Retirement_Home': {'Woolworths': 11, 'Intersection_3': 18}
}

# Define the coordinate locations of each facility or landmark in the area
local_map_locations = {
    'Royal_Gardens': (145.2691829, -36.7304496),
    'Cranbourne_Park_Shopping_Centre': (145.2841866, -36.1089868),
    'Intersection_1': (145.2933633, -35.5063795),
    'Broad_Oak_Centre': (145.3064638, -37.1015526),
    'Roundabout_1': (145.3019334, -34.1033545),
    'Roundabout_2': (145.2899518, -33.1138384),
    'Intersection_2': (145.2829935, -32.1130201),
    'APCO': (145.2947391, -32.0941597),
    'Coles_Springhill': (145.2928501, -30.0849908),
    'Monash_Health_Centre': (145.2716139, -29.1130723),
    'Woolworths': (145.2937496, -27.6002),
    'ALDI': (145.2988979, -27.100051),
    'Hearing_Australia': (145.2721944, -26.1127),
    'Stem_Academic_College': (145.2742891, -24.1127675),
    'Elite_Computer': (145.2856696, -18.113131),
    'Police_Station': (145.2875418, -23.1133387),
    'Community_Information_Center': (145.2781971, -22.193562),
    'Public_Toilet': (145.2942854, -21.1144225),
    'Public_Toilet_2': (145.2928705, -38.1062415),
    'Intersection_3': (145.3021679, -19.0997019),
    'Shopping_Center_Parking': (145.28152, -38.11188),
    'Saint_Agatha_Parish': (145.2636139, -28.1130723),
    'St_Agatha_Primary_School': (145.2636139, -24.1130723),
    'Girl_Guides_Hall': (145.2716139, -20.1130723),
    'Retirement_Home': (145.2980496, -23.6002)
}

def display_visual_2(graph_data):
    """This method defined how the visual will be presented, it also calls the shortestDijkstraPath to exceute"""
    # Define dropdown widgets for selecting start and end nodes
    start_dropdown = widgets.Dropdown(
        options=list(graph_data.keys()),
        description='Start Location:',
        value="Cranbourne_Park_Shopping_Centre"
    )

    end_dropdown = widgets.Dropdown(
        options=list(graph_data.keys()),
        description='End Location:',
        value="Royal_Gardens"
    )

    # Define a button to trigger the shortest path calculation
    calculate_button = widgets.Button(description='Calculate Path')

    # Define output widget for displaying result
    output = widgets.Output()

    def on_button_click(b):
        with output:
            output.clear_output()
            start_node = start_dropdown.value
            end_node = end_dropdown.value
            distance, path = shortestDijkstraPath(graph_data, start_node, end_node)
            print(f"Shortest path has the total cost: {distance} wheelchair accessible minutes")

            # Create a directed graph
            G = nx.DiGraph()

            # Add nodes and edges with weights to the graph
            for node, neighbors in graph_data.items():
                for neighbor, weight in neighbors.items():
                    G.add_edge(node, neighbor, weight=weight)

            # Draw the graph
            plt.figure(figsize=(20, 7))  # Adjust the figure size here

            # Draw nodes
            nx.draw_networkx_nodes(G, local_map_locations, node_size=1000, node_color="white")

            # Draw edges
            for u, v, d in G.edges(data=True):
                if (u, v) in zip(path, path[1:]):  # Highlight the shortest path
                    nx.draw_networkx_edges(G, local_map_locations, edgelist=[(u, v)], width=3, alpha=0.7, edge_color='green')
                else:
                    nx.draw_networkx_edges(G, local_map_locations, edgelist=[(u, v)], width=1, alpha=0.5, edge_color='black')

            # Draw labels
            nx.draw_networkx_labels(G, local_map_locations, font_size=12)

            # Display edge weights
            edge_labels = nx.get_edge_attributes(G, 'weight')
            nx.draw_networkx_edge_labels(G, local_map_locations, edge_labels=edge_labels, font_size=10)

            # Highlight the solution path
            nx.draw_networkx_nodes(G, local_map_locations, nodelist=path, node_size=1000, node_color="green")

            # Show the plot
            plt.axis('off')  # Turn off axis
            plt.show()

    calculate_button.on_click(on_button_click)

    # Display widgets
    display(start_dropdown, end_dropdown, calculate_button, output)

# Call the function to display the widgets
display_visual_2(local_map)