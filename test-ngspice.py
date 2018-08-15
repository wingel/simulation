#! /usr/bin/python
from __future__ import absolute_import, division, print_function, unicode_literals

import sys

from kicad.schema import Sch
from kicad.spice_converter import sch_to_circuit
from spice.unit import *
from spice.ngspice import Simulator

def test(fn):
    sch = Sch(fn)
    circuit = sch_to_circuit(sch)

    sim = Simulator(trace = sys.stdout.write)

    print(sim.circuit_to_spice(circuit))

    data = sim.dc(circuit, 'v101', -2, 2, 1 * m)

    print(data['v(v-sweep)'])
    print(data['v(vout)'])

if  __name__ == '__main__':
    if not sys.argv[0]:
        sys.argv = [ '', 'examples/butterworth/butterworth.sch' ]
    test(sys.argv[1])
