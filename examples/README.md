# examples
A few example mazes compatible with this solver. A brief desciption:

- tiny: Very small!
- small: Quite small!
- normal: I used this for testing a lot - 41x41 perfect maze (with one solution).

- logo: A maze that includes the computerphile logo, it still has a few solutions I believe, though I had to hack about with it so there may now only be one.

- perfect2k/4k/10k: Perfect mazes, only one solution to each, various sizes. The 10k image is 100 megapixels, so use with care.

- braid200: A small braid maze. Braid mazes have multiple solutions.
- braid2k: Much larger braid maze with multiple solutions.

- combo400: A braid maze that has had some paths replaced with dead ends - for a slightly more interesting maze overall. Still has multiple solutions.
- combo6k: A larger version of this combo maze. Since this has multiple solutions, the path taken isn't that exciting, but it'll demonstrate the difference between depth first and optimal solutions like astar or breadth first.

- vertical15k: I started running short on ram here. I created a maze with a vertical bias, so there are generally longer vertical corridors. This reduces the node count somewhat, and as such reduced the RAM. If you have the computer for it, you can probably attempt a 15 or 20k maze without bias. Bear in mind that a 15k squared image is 225 megapixels, this is very big! I also had problems saving the image once the algorithm completed - could be RAM, could just be the Image class doesn't like files of this size! More testing needed.