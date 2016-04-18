# Copyright (c) 2016, German Neuroinformatics Node (G-Node)
#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted under the terms of the BSD License. See
# LICENSE file in the root of the Project.

import numpy as np
from .entity import Entity


class DataType(object):
    # TODO: Check type equivalence with NIX
    Bool = np.bool_
    Char = np.string_  # NOTE: Perhaps S1?
    Float = np.float_
    Double = np.double
    Int8 = np.int8
    Int16 = np.int16
    Int32 = np.int32
    Int64 = np.int64
    UIntu8 = np.uint8
    UInt16 = np.uint16
    UInt32 = np.uint32
    UInt64 = np.uint64
    String = np.string_
    Nothing = None


class Property(Entity):

    def __init__(self):
        super(Property, self).__init__()
        self.name = None
        self.property = None
        self.mapping = None
        self.unit = None
        self.data_type = None
        self.values = None

    def delete_values(self):
        pass

    def __str__(self):
        pass

    def __repr__(self):
        pass
