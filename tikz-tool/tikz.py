import numpy as np
import networkx as nx
from helper_functions import *

def outputTikz(fitnessGraph, positioning="horizontal", ascents=[], restrictMutationsToPredSuc = False):
    tikz_code = "\\begin{tikzpicture}[->,>=stealth',shorten >=1pt,auto,node distance=2.5cm, semithick, draw=lightgray]\n"
    
    # Keep track of which nodes have been placed and their positions
    placed_nodes = {}
    current_layer = [list(fitnessGraph.nodes)[0]]  # Start with the root node
    placed_nodes[current_layer[0]] = (0, 0)

    # Position the root node
    tikz_code += f"\\node ({current_layer[0]}) at (0, 0) {{{current_layer[0]}}};\n"

    layer_index = 1  # Start placing from the next layer above the root (now to the right)

    # Traverse layers, placing nodes only once
    while current_layer:
        next_layer = []  # Nodes in the next column
        
        # Collect the unplaced successors for the next layer
        for node in current_layer:
            for neighbor in set(fitnessGraph.successors(node)).union(fitnessGraph.predecessors(node)):  # Adjacent nodes
                if neighbor not in placed_nodes:
                    if restrictMutationsToPredSuc:  #Restricts the construction of the next layer to mutations that increment/decrement a variable's value by 1
                        for i in range(len(node)):
                            differenceIndex = -1  # No difference found
                            if node[i] != neighbor[i]:  # Find the first differing index
                                differenceIndex = i
                            # Now check if the difference in values is exactly 1
                            if differenceIndex != -1 and abs(int(node[differenceIndex]) - int(neighbor[differenceIndex])) == 1:
                                next_layer.append(neighbor)
                                placed_nodes[neighbor] = None  # Mark as found, but not yet positioned
                    else:
                        next_layer.append(neighbor)
                        placed_nodes[neighbor] = None  # Mark as found, but not yet positioned

        
        # Centering: Determine offset to center the next layer
        num_nodes_in_layer = len(next_layer)
        if num_nodes_in_layer > 0:
            # Calculate offset for centering the layer
            spacing_factor = 0
            layer_spacing_factor = 3.5
            if np.log(num_nodes_in_layer) != 0:
                spacing_factor = 5/np.log(num_nodes_in_layer)
            start_y = -(num_nodes_in_layer - 1) * spacing_factor/2  # Start so that nodes are centered vertically
            for i, neighbor in enumerate(next_layer):
                extraStartFormatting = ""
                extraEndFormatting = ""
                if any(neighbor == a[0][len(a[0])-1] for a in ascents): #Add some extra formatting to final step in ascent
                       extraStartFormatting = "\\textbf{" 
                       extraEndFormatting = "}" 
                placed_nodes[neighbor] = (layer_index * layer_spacing_factor, start_y + i * spacing_factor)
                # Add node to TikZ
                if (positioning == "vertical"):
                    tikz_code += f"\\node ({neighbor}) at ({layer_index*layer_spacing_factor},{start_y + i*spacing_factor}) {{{extraStartFormatting}{neighbor}{extraEndFormatting}}};\n"
                elif (positioning == "horizontal"):
                    tikz_code += f"\\node ({neighbor}) at ({start_y + i*spacing_factor},{layer_index*layer_spacing_factor}) {{{extraStartFormatting}{neighbor}{extraEndFormatting}}};\n"
        
        # Move to the next column
        current_layer = next_layer
        layer_index += 1

    # Now add edges between nodes
    tikz_code += "\n\n\\path\n"
    ascentsToDraw = [] # We draw the highlighted ascents last so that their edges are on top of the other edges
    for src, dst in fitnessGraph.edges:
        offsetFactor = 0  # To offset the arrow in case multiple ascents share the same step
        for ascent in ascents:
            for i in range(len(ascent[0]) - 1):
                if src == ascent[0][i] and dst == ascent[0][i+1]:
                    ascentsToDraw.append(((src, dst), f"{ascent[1]}", offsetFactor))
                    offsetFactor = nextInterleavedInteger(offsetFactor)
                    continue
        tikz_code += f"({src}) edge ({dst})\n"
    tikz_code += ";\n\n"
    
    for (src, dst), ascentType, offsetFactor in ascentsToDraw:
        tikz_code += f"\\begin{{scope}}[transform canvas={{xshift={0.25*offsetFactor}cm}}]\n"
        tikz_code += f" \\path[{assignAscentColor(ascentType)}, line width=0.6mm] ({src}) edge ({dst});\n"
        tikz_code += "\\end{scope}\n"

    tikz_code += "\\end{tikzpicture}\n"    
    print(tikz_code)


def assignAscentColor(ascentType):
    ascentColor = "black"
    match ascentType:
        case "steepest":
            ascentColor = "steepestAscentColor"
        case "ordered":
            ascentColor = "orderedAscentColor"
        case _:
            "black"
    return ascentColor
