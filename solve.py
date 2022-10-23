import argparse
from PIL import Image
import time
from mazes import Maze
from factory import SolverFactory
Image.MAX_IMAGE_PIXELS = None

# usage:
#!  python3 solve.py -m depthfirst/breadthfirst ./small.png ./small-copy.png

# Read command line arguments - the python argparse class is convenient here.


def solve(factory, method: str = "breadthfirst", input_file: str = None, output_file: str = None):
    # Load Image
    print("Loading Image")
    im = Image.open(input_file)

    # Create the maze (and time it) - for many mazes this is more time consuming than solving the maze
    print("Creating Maze")
    t0 = time.time()
    maze = Maze(im)
    t1 = time.time()
    print("Node Count:", maze.count)
    total = t1-t0
    print("Time elapsed:", total, "\n")

    # Create and run solver
    [title, solver] = factory.createsolver(method)
    print("Starting Solve:", title)

    t0 = time.time()
    [result, stats] = solver(maze)
    t1 = time.time()

    total = t1-t0

    # Print solve stats
    print("Nodes explored: ", stats[0])
    if (stats[2]):
        print("Path found, length", stats[1])
    else:
        print("No Path Found")
    print("Time elapsed: ", total, "\n")

    """
    Create and save the output image.
    This is simple drawing code that travels between each node in turn, drawing either
    a horizontal or vertical line as required. Line colour is roughly interpolated between
    blue and red depending on how far down the path this section is.
    """

    print("Saving Image")
    im = im.convert('RGB')
    impixels = im.load()

    resultpath = [n.Position for n in result]

    length = len(resultpath)

    for i in range(0, length - 1):
        a = resultpath[i]
        b = resultpath[i+1]

        # Blue - red
        r = int((i / length) * 255)
        px = (r, 0, 255 - r)

        if a[0] == b[0]:
            # Ys equal - horizontal line
            for x in range(min(a[1], b[1]), max(a[1], b[1])):
                impixels[x, a[0]] = px
        elif a[1] == b[1]:
            # Xs equal - vertical line
            for y in range(min(a[0], b[0]), max(a[0], b[0]) + 1):
                impixels[a[1], y] = px

    if not output_file:
        output_file = input_file.split(".")
        output_file[0] = output_file[0] + "OP"
        output_file = ".".join(output_file)

    im.save(output_file)


def main():
    sf = SolverFactory()
    parser = argparse.ArgumentParser(
        description="Maze Solving using Image Processing")
    parser.add_argument("-m", "--method", nargs='?', const=sf.Default, default=sf.Default,
                        choices=sf.Choices, help="Method to be used on solving the maze")
    parser.add_argument("-i", "--input", required=True,
                        help="Image of the maze input file")
    parser.add_argument("-o", "--output", help="Solved output maze file")
    args = parser.parse_args()

    solve(sf, args.method, args.input, args.output)


if __name__ == "__main__":
    main()
