class Maze:
    class Node:
        def __init__(self, position):
            self.Position = position
            self.Neighbours = [None, None, None, None]
            #self.Weights = [0, 0, 0, 0]

    def __init__(self, im):

        width = im.size[0]
        height = im.size[1]
        data = list(im.getdata(0))

        self.start = None
        self.end = None

        # Top row buffer
        topnodes = [None] * width
        count = 0

        # Start row
        for x in range (1, width - 1):
            if data[x] > 0:
                self.start = Maze.Node((0,x))
                topnodes[x] = self.start
                count += 1
                break

        for y in range (1, height - 1):
            #print ("row", str(y)) # Uncomment this line to keep a track of row progress

            rowoffset = y * width
            rowaboveoffset = rowoffset - width
            rowbelowoffset = rowoffset + width

            # Initialise previous, current and next values
            prv = False
            cur = False
            nxt = data[rowoffset + 1] > 0

            leftnode = None

            for x in range (1, width - 1):
                # Move prev, current and next onwards. This way we read from the image once per pixel, marginal optimisation
                prv = cur
                cur = nxt
                nxt = data[rowoffset + x + 1] > 0

                n = None

                if cur == False:
                    # ON WALL - No action
                    continue

                if prv == True:
                    if nxt == True:
                        # PATH PATH PATH
                        # Create node only if paths above or below
                        if data[rowaboveoffset + x] > 0 or data[rowbelowoffset + x] > 0:
                            n = Maze.Node((y,x))
                            leftnode.Neighbours[1] = n
                            n.Neighbours[3] = leftnode
                            leftnode = n
                    else:
                        # PATH PATH WALL
                        # Create path at end of corridor
                        n = Maze.Node((y,x))
                        leftnode.Neighbours[1] = n
                        n.Neighbours[3] = leftnode
                        leftnode = None
                else:
                    if nxt == True:
                        # WALL PATH PATH
                        # Create path at start of corridor
                        n = Maze.Node((y,x))
                        leftnode = n
                    else:
                        # WALL PATH WALL
                        # Create node only if in dead end
                        if (data[rowaboveoffset + x] == 0) or (data[rowbelowoffset + x] == 0):
                            #print ("Create Node in dead end")
                            n = Maze.Node((y,x))

                # If node isn't none, we can assume we can connect N-S somewhere
                if n != None:
                    # Clear above, connect to waiting top node
                    if (data[rowaboveoffset + x] > 0):
                        t = topnodes[x]
                        t.Neighbours[2] = n
                        n.Neighbours[0] = t

                    # If clear below, put this new node in the top row for the next connection
                    if (data[rowbelowoffset + x] > 0):
                        topnodes[x] = n
                    else:
                        topnodes[x] = None

                    count += 1

        # End row
        rowoffset = (height - 1) * width
        for x in range (1, width - 1):
            if data[rowoffset + x] > 0:
                self.end = Maze.Node((height - 1,x))
                t = topnodes[x]
                t.Neighbours[2] = self.end
                self.end.Neighbours[0] = t
                count += 1
                break

        self.count = count
        self.width = width
        self.height = height
