# Copyright (c) 2016, German Neuroinformatics Node (G-Node)
#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted under the terms of the BSD License. See
# LICENSE file in the root of the Project.

from .entity import EntityWithSources
from . import util


class Group(EntityWithSources):

    def __init__(self, h5parent, name, type_):
        id_ = util.create_id()
        h5obj = h5parent.create_group(name)
        super(Group, self).__init__(h5obj, id_, name, type_)

    def _add_data_array_by_id(self):
        pass

    def _has_data_array_by_id(self):
        pass

    def _data_array_count(self):
        pass

    def _get_data_array_by_id(self):
        pass

    def _get_data_array_by_pos(self):
        pass

    def _delete_data_array_by_id(self):
        pass

    def _add_tag_by_id(self):
        pass

    def _has_tag_by_id(self):
        pass

    def _tag_count(self):
        pass

    def _get_tag_by_id(self):
        pass

    def _get_tag_by_pos(self):
        pass

    def _delete_tag_by_id(self):
        pass

    def _add_multi_tag_by_id(self):
        pass

    def _has_multi_tag_by_id(self):
        pass

    def _multi_tag_count(self):
        pass

    def _get_multi_tag_by_id(self):
        pass

    def _get_multi_tag_by_pos(self):
        pass

    def _delete_multi_tag_by_id(self):
        pass

    def __str__(self):
        pass

    def __repr__(self):
        pass
