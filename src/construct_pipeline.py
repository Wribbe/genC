#!/usr/bin/env python3

import sys
import os

def main(args):
  fname = args[-1]
  with open(fname, 'a'):
    os.utime(fname, None)

if __name__ == "__main__":
  main(sys.argv[1:])
