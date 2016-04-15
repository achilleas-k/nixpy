# Copyright (c) 2016, German Neuroinformatics Node (G-Node)
#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted under the terms of the BSD License. See
# LICENSE file in the root of the Project.

from .entity import EntityWithSources
from .data_set import DataSet


class DataArray(EntityWithSources, DataSet):

    def __init__(self):
        EntityWithSources.__init__()
        DataSet.__init__()
        self.label = None
        self.unit = None
        self.expansion_origin = None
        self.polynom_coefficients = None

    def create_set_dimension(self):
        pass

    def create_sampled_dimension(self):
        pass

    def create_range_dimension(self):
        pass

    def append_set_dimension(self):
        pass

    def append_sampled_dimension(self):
        pass

    def append_range_dimension(self):
        pass

    def append_alias_range_dimension(self):
        pass

    def _dimension_count(self):
        pass

    def _delete_dimension_by_pos(self, index):
        pass

    def _get_dimension_by_pos(self, index):
        pass
