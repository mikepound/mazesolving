from PIL import Image
import time
from mazes import Maze
from factory import SolverFactory
from concurrent.futures import ThreadPoolExecutor
Image.MAX_IMAGE_PIXELS = None

# Read command line arguments - the python argparse class is convenient here.
import argparse

MAX_DRAWING_WORKERS = 5

def solve(factory, method, input_file, output_file):
    # Load Image
    print ("Loading Image")
    im = Image.open(input_file)

    # Create the maze (and time it) - for many mazes this is more time consuming than solving the maze
    print ("Creating Maze")
    t0 = time.time()
    maze = Maze(im)
    t1 = time.time()
    print ("Node Count:", maze.count)
    total = t1-t0
    print ("Time elapsed:", total, "\n")

    # Create and run solver
    [title, solver] = factory.createsolver(method)
    print ("Starting Solve:", title)

    t0 = time.time()
    [result, stats] = solver(maze)
    t1 = time.time()

    total = t1-t0

    # Print solve stats
    print ("Nodes explored: ", stats[0])
    if (stats[2]):
        print ("Path found, length", stats[1])
    else:
        print ("No Path Found")
    print ("Time elapsed: ", total, "\n")

    """
    Create and save the output image.
    This is simple drawing code that travels between each node in turn, drawing either
    a horizontal or vertical line as required. Line colour is roughly interpolated between
    blue and red depending on how far down the path this section is.
    """

    print ("Saving Image")
    im = im.convert('RGB')
    resultpath = [n.Position for n in result]

    drawPathOnImage(im,resultpath)#threaded draw line 
    
    im.save(output_file)

def draw_line(impixels, a, b, px): 
    if a[0] == b[0]:
            # Ys equal - horizontal line
            for x in range(min(a[1],b[1]), max(a[1],b[1])):
                impixels[x,a[0]] = px
        elif a[1] == b[1]:
            # Xs equal - vertical line
            for y in range(min(a[0],b[0]), max(a[0],b[0]) + 1):
                impixels[a[1],y] = px

def drawPathOnImage(imageObj: Image, ResultPath: list):
    impixels = imageObj.load()
    length = len(ResultPath)

    with ThreadPoolExecutor(max_workers=MAX_DRAWING_WORKERS) as executor:
        futures = []
        for i in range(length - 1):
            a = ResultPath[i]
            b = ResultPath[i + 1]

            # Gradient color (Blue -> Red)
            r = int((i / length) * 255)
            px = (r, 0, 255 - r)

            futures.append(executor.submit(draw_line, impixels, a, b, px))

        # join all threads
        for future in futures:
            future.result()


def main():
    sf = SolverFactory()
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--method", nargs='?', const=sf.Default, default=sf.Default,
                        choices=sf.Choices)
    parser.add_argument("input_file")
    parser.add_argument("output_file")
    args = parser.parse_args()

    solve(sf, args.method, args.input_file, args.output_file)

if __name__ == "__main__":
    main()

