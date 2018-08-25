#! /usr/bin/python
from __future__ import absolute_import, division, print_function, unicode_literals

import os

from spice.preprocessor import SpicePreprocessor

if __name__ == "__main__":
    fn = 'examples/tia/spice.lib'
    models = 'models'

    pp = SpicePreprocessor()
    pp.add_path(models)
    pp.define('NGSPICE')
    pp.parse(open(fn).read())

    print(pp.output())
