from tikz import *
import networkx as nx
import itertools

#Example assignments
assignments = ["000","100","010","110","001","101","111"]

#Example fitness function: binary number
def fitnessFunction(assignment):
    return sum(int(assignment[i])*pow(2,i) for i in range(3))

#Get Hamming distance 1 directed arcs
edges = [(x,y) for x,y in itertools.product(assignments,assignments) if sum(x[i] != y[i] for i in range(len(x))) == 1 and fitnessFunction(y)>fitnessFunction(x)] 
fitnessGraph = nx.DiGraph(edges)


outputTikz(fitnessGraph)