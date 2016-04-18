# Copyright (c) 2016, German Neuroinformatics Node (G-Node)
#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted under the terms of the BSD License. See
# LICENSE file in the root of the Project.

from __future__ import absolute_import
from .entity import EntityWithMetadata


class Block(EntityWithMetadata):

    def __init__(self):
        super(Block, self).__init__()
        pass

    def _create_data_array(self, name, type_, data_type, shape):
        pass

    def _data_array_count(self):
        pass

    def _get_data_array_by_id(self, id_):
        pass

    def _get_data_array_by_pos(self, index):
        pass

    def _delete_data_array_by_id(self, id_):
        pass

    def create_multi_tag(self):
        pass

    def _multi_tag_count(self):
        pass

    def _get_multi_tag_by_id(self, id_):
        pass

    def _get_multi_tag_by_pos(self, index):
        pass

    def _delete_multi_tag_by_id(self, id_):
        pass

    def create_tag(self):
        pass

    def _tag_count(self):
        pass

    def _get_tag_by_id(self, id_):
        pass

    def _get_tag_by_pos(self, index):
        pass

    def _delete_tag_by_id(self, id_):
        pass

    def create_source(self):
        pass

    def _source_count(self):
        pass

    def _get_source_by_id(self, id_):
        pass

    def _get_source_by_pos(self, index):
        pass

    def _delete_source_by_id(self, id_):
        pass

    def create_group(self):
        pass

    def _group_count(self):
        pass

    def _get_group_by_id(self, id_):
        pass

    def _get_group_by_pos(self, index):
        pass

    def _delete_group_by_id(self, id_):
        pass

    def __str__(self):
        pass

    def __repr__(self):
        pass

