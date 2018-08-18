#! /usr/bin/python
from __future__ import absolute_import, division, print_function, unicode_literals

import sys

from kicad import schema
from kicad import spice_converter
from spice.ltspice import Simulator

def test(fn):
    from spice import unit

    sch = schema.Sch(fn)
    circuit = spice_converter.sch_to_circuit(sch)

    sim = Simulator()

    print(sim.circuit_to_spice(circuit))

    data = sim.dc(circuit, 'v101', -2, 2, 1 * unit.m)

    print(data.keys())

    print(data['SWEEP'])
    print(data['V(VOUT)'])

if  __name__ == '__main__':
    if not sys.argv[0]:
        sys.argv = [ '', 'examples/butterworth/butterworth.sch' ]
    test(sys.argv[1])
