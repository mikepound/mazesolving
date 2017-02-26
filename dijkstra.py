from FibonacciHeap import FibHeap
from priority_queue import FibPQ, HeapPQ, QueuePQ

def solve(maze):
    # Width is used for indexing, total is used for array sizes
    width = maze.width
    total = maze.width * maze.height

    # Start node, end node
    start = maze.start
    startpos = start.Position
    end = maze.end
    endpos = end.Position

    # Visited holds true/false on whether a node has been seen already. Used to stop us returning to nodes multiple times
    visited = [False] * total

    # Previous holds a link to the previous node in the path. Used at the end for reconstructing the route
    prev = [None] * total

    # Distances holds the distance to any node taking the best known path so far. Better paths replace worse ones as we find them.
    # We start with all distances at infinity
    infinity = float("inf")
    distances = [infinity] * total

    # The priority queue. There are multiple implementations in priority_queue.py
    # unvisited = FibHeap()
    unvisited = HeapPQ()
    # unvisited = FibPQ()
    # unvisited = QueuePQ()

    # This index holds all priority queue nodes as they are created. We use this to decrease the key of a specific node when a shorter path is found.
    # This isn't hugely memory efficient, but likely to be faster than a dictionary or similar.
    nodeindex = [None] * total

    # To begin, we set the distance to the start to zero (we're there) and add it into the unvisited queue
    distances[start.Position[0] * width + start.Position[1]] = 0
    startnode = FibHeap.Node(0, start)
    nodeindex[start.Position[0] * width + start.Position[1]] = startnode
    unvisited.insert(startnode)

    # Zero nodes visited, and not completed yet.
    count = 0
    completed = False

    # Begin Dijkstra - continue while there are unvisited nodes in the queue
    while len(unvisited) > 0:
        count += 1

        # Find current shortest path point to explore
        n = unvisited.removeminimum()

        # Current node u, all neighbours will be v
        u = n.value
        upos = u.Position
        uposindex = upos[0] * width + upos[1]

        if distances[uposindex] == infinity:
            break

        # If upos == endpos, we're done!
        if upos == endpos:
            completed = True
            break

        for v in u.Neighbours:
            if v != None:
                vpos = v.Position
                vposindex = vpos[0] * width + vpos[1]

                if visited[vposindex] == False:
                    # The extra distance from where we are (upos) to the neighbour (vpos) - this is manhattan distance
                    # https://en.wikipedia.org/wiki/Taxicab_geometry
                    d = abs(vpos[0] - upos[0]) + abs(vpos[1] - upos[1])

                    # New path cost to v is distance to u + extra
                    newdistance = distances[uposindex] + d

                    # If this new distance is the new shortest path to v
                    if newdistance < distances[vposindex]:
                        vnode = nodeindex[vposindex]
                        # v isn't already in the priority queue - add it
                        if vnode == None:
                            vnode = FibHeap.Node(newdistance, v)
                            unvisited.insert(vnode)
                            nodeindex[vposindex] = vnode
                            distances[vposindex] = newdistance
                            prev[vposindex] = u
                        # v is already in the queue - decrease its key to re-prioritise it
                        else:
                            unvisited.decreasekey(vnode, newdistance)
                            distances[vposindex] = newdistance
                            prev[vposindex] = u

        visited[uposindex] = True


    # We want to reconstruct the path. We start at end, and then go prev[end] and follow all the prev[] links until we're back at the start
    from collections import deque

    path = deque()
    current = end
    while (current != None):
        path.appendleft(current)
        current = prev[current.Position[0] * width + current.Position[1]]

    return [path, [count, len(path), completed]]
