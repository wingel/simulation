#! /usr/bin/python
from __future__ import absolute_import, division, print_function, unicode_literals

import sys

import kicad.schema

def test(load_fn, save_fn):
    sch = kicad.schema.Sch(load_fn)
    print()

    with open(save_fn, 'w') as f:
        sch.format(f)

if __name__ == '__main__':
    kicad.schema.VERBOSE = 1
    if not sys.argv[0]:
        sys.argv = [ '', 'examples/butterworth/butterworth.sch', 'out.sch' ]
    test(sys.argv[1], sys.argv[2])
