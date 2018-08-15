#! /usr/bin/python
from __future__ import absolute_import, division, print_function, unicode_literals

import spice.unit

class SimulatorBase(object):
    def fix_param(self, v):
        if isinstance(v, spice.unit._Unit):
            suffix = v.suffix
            if suffix == 'M':
                suffix = 'MEG'
            return str(v.value / v.multiplier) + suffix

        return str(v)

    def device_to_spice(self, device):
        a = []
        a.append(device.ref)
        for node in device.nodes:
            a.append(str(node))
        a.append(self.fix_param(device.value))
        for arg in device.args:
            a.append(self.fix_param(arg))
        for k, v in device.kwargs:
            a.append('%s=%s' % (k, self.fix_param(v)))
        return ' '.join(a)

    def circuit_to_spice(self, circuit):
        a = []

        for include in circuit.includes:
            a.append('.include %s' % include)
        for device in circuit.devices.values():
            a.append(self.device_to_spice(device))

        a.append('')

        return '\n'.join(a)
