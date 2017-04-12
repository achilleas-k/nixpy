# Copyright (c) 2016, German Neuroinformatics Node (G-Node)
#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted under the terms of the BSD License. See
# LICENSE file in the root of the Project.
from __future__ import (absolute_import, division, print_function)
import gc
import os
from sys import maxsize as maxint
from warnings import warn
import h5py

from .util import find as finders

try:
    from sys import maxint
except:
    from sys import maxsize as maxint
