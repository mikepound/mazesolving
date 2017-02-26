from FibonacciHeap import FibHeap
from priority_queue import FibPQ, HeapPQ, QueuePQ

# This implementatoin of A* is almost identical to the Dijkstra implementation. So for clarity I've removed all comments, and only added those
# Specifically showing the difference between dijkstra and A*

def solve(maze):
    width = maze.width
    total = maze.width * maze.height

    start = maze.start
    startpos = start.Position
    end = maze.end
    endpos = end.Position

    visited = [False] * total
    prev = [None] * total

    infinity = float("inf")
    distances = [infinity] * total

    # The priority queue. There are multiple implementations in priority_queue.py
    # unvisited = FibHeap()
    unvisited = HeapPQ()
    # unvisited = FibPQ()
    # unvisited = QueuePQ()

    nodeindex = [None] * total

    distances[start.Position[0] * width + start.Position[1]] = 0
    startnode = FibHeap.Node(0, start)
    nodeindex[start.Position[0] * width + start.Position[1]] = startnode
    unvisited.insert(startnode)

    count = 0
    completed = False

    while len(unvisited) > 0:
        count += 1

        n = unvisited.removeminimum()

        u = n.value
        upos = u.Position
        uposindex = upos[0] * width + upos[1]

        if distances[uposindex] == infinity:
            break

        if upos == endpos:
            completed = True
            break

        for v in u.Neighbours:
            if v != None:
                vpos = v.Position
                vposindex = vpos[0] * width + vpos[1]

                if visited[vposindex] == False:
                    d = abs(vpos[0] - upos[0]) + abs(vpos[1] - upos[1])

                    # New path cost to v is distance to u + extra. Some descriptions of A* call this the g cost.
                    # New distance is the distance of the path from the start, through U, to V.
                    newdistance = distances[uposindex] + d

                    # A* includes a remaining cost, the f cost. In this case we use manhattan distance to calculate the distance from
                    # V to the end. We use manhattan again because A* works well when the g cost and f cost are balanced.
                    # https://en.wikipedia.org/wiki/Taxicab_geometry
                    remaining = abs(vpos[0] - endpos[0]) + abs(vpos[1] - endpos[1])

                    # Notice that we don't include f cost in this first check. We want to know that the path *to* our node V is shortest
                    if newdistance < distances[vposindex]:
                        vnode = nodeindex[vposindex]

                        if vnode == None:
                            # V goes into the priority queue with a cost of g + f. So if it's moving closer to the end, it'll get higher
                            # priority than some other nodes. The order we visit nodes is a trade-off between a short path, and moving
                            # closer to the goal.
                            vnode = FibHeap.Node(newdistance + remaining, v)
                            unvisited.insert(vnode)
                            nodeindex[vposindex] = vnode
                            # The distance *to* the node remains just g, no f included.
                            distances[vposindex] = newdistance
                            prev[vposindex] = u
                        else:
                            # As above, we decrease the node since we've found a new path. But we include the f cost, the distance remaining.
                            unvisited.decreasekey(vnode, newdistance + remaining)
                            # The distance *to* the node remains just g, no f included.
                            distances[vposindex] = newdistance
                            prev[vposindex] = u


        visited[uposindex] = True

    from collections import deque

    path = deque()
    current = end
    while (current != None):
        path.appendleft(current)
        current = prev[current.Position[0] * width + current.Position[1]]

    return [path, [count, len(path), completed]]
