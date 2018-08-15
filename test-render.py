#! /usr/bin/python
from __future__ import absolute_import, division, print_function, unicode_literals

import sys

import matplotlib.pyplot as plt
import numpy as np

from kicad import schema, matplotlib_renderer

def test(fn):
    sch = schema.Sch(fn)

    fig, ax = plt.subplots(figsize = (8, 5.5))

    # fig.subplots_adjust(left = 0.0, right = 1.0, top = 1.0, bottom = 0.0)
    matplotlib_renderer.render_to_ax(ax, sch)
    plt.show()

    fig.savefig('butterworth.png')
    fig.savefig('butterworth.svg')
    fig.savefig('butterworth.pdf')

if  __name__ == '__main__':
    if not sys.argv[0]:
        sys.argv = [ '', 'examples/butterworth/butterworth.sch' ]
    test(sys.argv[1])
