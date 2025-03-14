#! /usr/bin/env python

# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""
This is an example driver for the simulation. It should soon be refactored to
result in an input file, an input parser, a solver interface, and output
scripts.
"""

import numpy as np

print("Hello World");

from pyrk.utilities.ur import units

t = 1 
t = t * units.seconds
print(t)
