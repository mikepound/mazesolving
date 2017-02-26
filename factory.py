# A simple factory class that imports and returns a relevant solver when provided a string
# Not hugely necessary, but reduces the code in solve.py, making it easier to read.

class SolverFactory:
    def __init__(self):
        self.Default = "breadthfirst"
        self.Choices = ["breadthfirst","depthfirst","dijkstra", "astar","leftturn"]

    def createsolver(self, type):
        if type == "leftturn":
            import leftturn
            return ["Left turn only", leftturn.solve]
        elif type == "depthfirst":
            import depthfirst
            return ["Depth first search", depthfirst.solve]
        elif type == "dijkstra":
            import dijkstra
            return ["Dijkstra's Algorithm", dijkstra.solve]
        elif type == "astar":
            import astar
            return ["A-star Search", astar.solve]
        else:
            import breadthfirst
            return ["Breadth first search", breadthfirst.solve]
