# -*- coding: utf-8 -*-
# Copyright © 2014, German Neuroinformatics Node (G-Node)
#
# All rights reserved.
#
# Redistribution and use in section and binary forms, with or without
# modification, are permitted under the terms of the BSD License. See
# LICENSE file in the root of the Project.
import unittest
from nixio.util import names, units


class TestUtil(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_name_sanitizer(self):
        assert names.sanitizer("validName") == "validName"
        assert names.sanitizer("invalid/name") == "invalid_name"

    def test_name_check(self):
        assert names.check("validName")
        assert not names.check("invalid/name")

    def test_unit_sanitizer(self):
        assert units.sanitizer("µV") == "uV"
        assert units.sanitizer("muOhm") == "uOhm"

    def test_unit_is_si(self):
        assert units.is_si('V')
        assert units.is_si('mV')
        assert units.is_si('kV')
        assert not units.is_si('Kv')
        assert not units.is_si('in')
        assert not units.is_si('pt')
        assert not units.is_si('ft')
        assert not units.is_si('yrd')

    def test_unit_is_atomic(self):
        assert units.is_atomic('mV')
        assert units.is_atomic('mV^2')
        assert not units.is_atomic('mV^2/Hz')

    def test_unit_is_compound(self):
        assert units.is_compound('mV^2/Hz')
        assert not units.is_compound('mV')

    def test_unit_split_compound(self):
        unit_1 = "mV^2/Hz"
        unit_2 = "mV^2 * Hz^-1"

        assert len(units.split_compound('mV')) == 1

        atomics = units.split_compound(unit_1)
        assert len(atomics) == 2
        # FIXME the following is not entirely correct should be Hz^-1
        # needs to be fixed in nix!
        assert atomics[0] == "mV^2" and atomics[1] == "Hz^-1"

        atomics = units.split_compound(unit_2)
        assert len(atomics) == 2
        assert atomics[0] == "mV^2" and atomics[1] == "Hz^-1"

    def test_unit_scalable(self):
        base_unit = 'V'
        scalable_1 = 'kV'
        scalable_2 = 'uV'
        inscalable = 'g'

        assert units.scalable([base_unit], [scalable_1])
        assert units.scalable([base_unit], [scalable_2])
        assert units.scalable([base_unit], [base_unit])
        assert not units.scalable([base_unit], [inscalable])
        assert(units.scalable([base_unit, scalable_1],
                              [base_unit, scalable_2]))

    def test_unit_scaling(self):
        base_unit = 'V'
        scalable_1 = 'kV'
        scalable_2 = 'uV'

        assert units.scaling(base_unit, scalable_1) == 1e-03
        assert units.scaling(base_unit, scalable_2) == 1e06

    def test_unit_split(self):
        unit_1 = 'kV'
        unit_2 = 'mV^2'
        unit_3 = 'Hz^-1'

        prefix, base, power = units.split(unit_1)
        assert prefix == 'k' and base == 'V' and power == ''

        prefix, base, power = units.split(unit_2)
        assert prefix == 'm' and base == 'V' and power == '2'

        prefix, base, power = units.split(unit_3)
        assert prefix == '' and base == 'Hz' and power == '-1'
