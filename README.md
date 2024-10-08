# TikZ Tool for Representing Fitness Graphs

A simple tool that outputs TikZ code for representing fitness graphs.
The fitness graph is represented in layers:
- Layer 1: starting assignment.
- Layer n+1: all adjacent variables (that haven't been placed yet) to assignments in Layer n.



## Documentation

**Input:**
- The fitness graph as a networkx digraph
- (Optional) string specifying whether the layers should be arranged horizontally or vertically. *Standard input:* "horizontal"
- (Optional) list of ascents to be highlighted. Ascent should be a tuple of (1) list of assignments, (2) string specifying ascent type.
- (Optional) boolean specifying whether the construction should restrict to steps that increment or decrement the value of a variable by 1. **N.B.**: only works when the neighbourhood structure is given by (restricted) unit Hamming ball.



**Output:**\
The TikZ code is printed to the console.