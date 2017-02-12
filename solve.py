import numpy as np;
from PIL import Image;
import time
from mazes import Maze;
from factory import SolverFactory;

# Read command line arguments - the python argparse class is convenient here.
import argparse
sf = SolverFactory();
parser = argparse.ArgumentParser()
parser.add_argument("-m", "--method", nargs='?', const=sf.Default, default=sf.Default,
						choices=sf.Choices)
parser.add_argument("input_file")
parser.add_argument("output_file")
args = parser.parse_args()

method = args.method;

# Load Image
print ("Loading Image");
im = Image.open(args.input_file);

# Create the maze (and time it) - for many mazes this is more time consuming than solving the maze
print ("Creating Maze");
t0 = time.time()
maze = Maze(im);
t1 = time.time()
print ("Node Count:", maze.count);
total = t1-t0
print ("Time elapsed:", total, "\n");

# Create and run solver
[title, solver] = sf.createsolver(args.method);
print ("Starting Solve:", title);

t0 = time.time()
[result, stats] = solver(maze);
t1 = time.time()

total = t1-t0

# Print solve stats
print ("Nodes explored: ", stats[0]);
if (stats[2]):
	print ("Path found, length", stats[1]);
else:
	print ("No Path Found");
print ("Time elapsed: ", total, "\n");

"""
Create and save the output image.
This is simple drawing code that travels between each node in turn, drawing either
a horizontal or vertical line as required. Line colour is roughly interpolated between
blue and red depending on how far down the path this section is. Dependency on numpy
should be easy to remove at some point.
"""

print ("Saving Image");
mazeimage = np.array(im)
imout = np.array(mazeimage);
imout[imout==1] = 255;
out = imout[:,:,np.newaxis];

out = np.repeat(out, 3, axis=2);

resultpath = [n.Position for n in result];

length = len(resultpath);

px = [0, 0, 0];
for i in range(0, length - 1):
	a = resultpath[i];
	b = resultpath[i+1];

	# Blue - red
	px[0] = int((i / length) * 255);
	px[2] = 255 - px[0];

	if a[0] == b[0]:
		# Ys equal - horizontal line
		for x in range(min(a[1],b[1]), max(a[1],b[1])):
			out[a[0],x,:] = px
	elif a[1] == b[1]:
		# Xs equal - vertical line
		for y in range(min(a[0],b[0]), max(a[0],b[0]) + 1):
			out[y,a[1],:] = px

img = Image.fromarray(out);
img.save(args.output_file)
