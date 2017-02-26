#!/usr/bin/env python

from bprofile import BProfile

import tempfile
from solve import solve
from factory import SolverFactory

methods = [
    "astar",
    # "breadthfirst",
    # "depthfirst",
    "dijkstra",
    # "leftturn",
]
inputs = [
    # "tiny",
    # "small",
    # "normal",
    # "braid200",
    "logo",
    "combo400",
    "braid2k",
    "perfect2k",
    # "perfect4k",
    # "combo6k",
    # "perfect10k",
    # "vertical15k",
]

def profile():
    for m in methods:
        for i in inputs:
            with tempfile.NamedTemporaryFile(suffix='.png') as tmp:
                solve(SolverFactory(), m, "examples/%s.png" % i, tmp.name)

profiler = BProfile('profiler.png')
with profiler:
    profile()
