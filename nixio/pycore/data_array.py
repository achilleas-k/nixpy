# Copyright (c) 2016, German Neuroinformatics Node (G-Node)
#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted under the terms of the BSD License. See
# LICENSE file in the root of the Project.

from . import util
from .entity import EntityWithSources


class DataArray(EntityWithSources):

    def __init__(self, h5parent, name, type_, data, shape):
        id_ = util.create_id()
        h5obj = h5parent.create_dataset(name=name, data=data)
        super(DataArray, self).__init__(h5obj, id_, name, type_)
        self._h5attrs.extend(["label", "unit", "expansion_origin",
                              "polynom_coefficients"])

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


class DataSet(object):
    pass
