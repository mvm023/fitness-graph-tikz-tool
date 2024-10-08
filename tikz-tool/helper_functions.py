import numpy as np
import networkx as nx

def nextInterleavedInteger(k):  #Function that returns the next value in the canonical enumeration of interleaved integers (i.e. 0,1,-1,2,-2,3,-3,...)
    if k == 0:
        return 1
    if k > 0:
        return -k
    if k < 0:
        return abs(k)+1