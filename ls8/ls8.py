#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

cpu = CPU()
cpu.trace()
cpu.load(sys.argv[1])
cpu.run()
