#! /usr/bin/python
from __future__ import absolute_import, division, print_function, unicode_literals

import numpy as np

from .simulator import SimulatorBase

class Xyce(SimulatorBase):
    SIMULATOR = 'LD_LIBRARY_PATH=/usr/local/xyce/serial/lib /usr/local/xyce/serial/bin/Xyce'
    HEADER = '#define XYCE'

    def __init__(self):
        super(Xyce, self).__init__()

    def update_variable(self, dataset, var):
        name = var.name.upper()
        if name in [ 'SWEEP', 'TIME' ]:
            pass
        elif name in [ 'FREQUENCY' ]:
            name = 'SWEEP'
        elif name.endswith('#BRANCH'):
            name = 'I(%s)' % name[:-7]
        elif not name.startswith('V('):
            name = 'V(%s)' % name

        var.name = name

        if 'complex' in dataset.flags:
            var.dt = np.complex128
        else:
            var.dt = np.float64

    def _default_trace(self, s):
        if s.startswith('***** Percent complete'):
            percent = float(s.split()[-2])
            self.progress.percent(percent)
        elif s.startswith('***** Current system time'):
            pass
        elif s.startswith('***** Estimated time to completion'):
            pass
        else:
            super(Xyce, self)._default_trace(s)

    def noise(self, circuit, out, ref, variation, n, fstart, fstop, **kwargs):
        args = [ '.noise', out, ref, variation, n, fstart, fstop, 1 ]
        args = [ self.fix_param(_) for _ in args ]
        s = ' '.join(args)
        s += '\n' + '.PRINT NOISE'
        return self._simulate(circuit, '', s, **kwargs)

Simulator = Xyce
