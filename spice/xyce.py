#! /usr/bin/python
from __future__ import absolute_import, division, print_function, unicode_literals

import numpy as np

from .simulator import SimulatorBase

class Xyce(SimulatorBase):
    SIMULATOR = 'LD_LIBRARY_PATH=/usr/local/xyce/serial/lib /usr/local/xyce/serial/bin/Xyce'

    def __init__(self, trace = None):
        super(Xyce, self).__init__(trace)

    def update_variables(self, dataset):
        dataset.dt = []
        for idx, (name, unit, params) in enumerate(self.variables):
            name = name.upper()
            if name.startswith('V') and not name.startswith('V('):
                name = 'V(%s)' % name
            elif name.startswith('I') and not name.startswith('I('):
                name = 'I(%s)' % name

            dataset.unit[name] = unit
            dataset.params[name] = params

            if 'complex' in dataset.flags:
                dataset.dt.append(( name, np.complex128 ))
            else:
                dataset.dt.append(( name, np.float64 ))

Simulator = Xyce
