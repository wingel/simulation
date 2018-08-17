#! /usr/bin/python
from __future__ import absolute_import, division, print_function, unicode_literals

import os
import numpy as np

from .simulator import SimulatorBase, Dataset

class LTspice(SimulatorBase):
    SIMULATOR = 'DISPLAY=:0 "%s/.wine/drive_c/Program Files/LTC/LTspiceXVII/XVIIx64.exe"' % os.environ['HOME']
    ENCODING = 'utf_16_le'
    BASE = '..'

    def __init__(self, trace = None):
        super(LTspice, self).__init__(trace)

    def _create_files(self):
        return 'spice.cir', 'spice.raw'

    def _make_cmd(self, cir_path, raw_path):
        return '%s -b %s' % (self.SIMULATOR, cir_path)

    def update_variables(self, dataset):
        dataset.dt = []
        for idx, (name, unit, params) in enumerate(self.variables):
            name = name.upper()

            if idx == 0 and name not in [ 'TIME', 'FREQUENCY' ]:
                print('rename', name)
                name = 'SWEEP'

            elif name.startswith('V') and not name.startswith('V('):
                name = 'V(%s)' % name

            dataset.unit[name] = unit
            dataset.params[name] = params

            if 'complex' in dataset.flags:
                dataset.dt.append(( name, np.complex128 ))
            elif idx != 0:
                dataset.dt.append(( name, np.float32 ))
            else:
                dataset.dt.append(( name, np.float64 ))

    def dc(self, circuit, source, start, stop, step):
        args = [ '.dc', source, start, stop, step ]
        data = self._simulate_simple(circuit, *args)

        return data

    def tran(self, circuit, tstep, tstop, tstart=0, tmax=None, uic=False):
        args = [ '.tran', tstep, tstop, tstart ]
        if tmax is not None:
            args.append(tmax)
        if uic:
            args.append('uic')
        data = self._simulate_simple(circuit, *args)
        data['TIME'] = abs(data['TIME'])
        return data

Simulator = LTspice
