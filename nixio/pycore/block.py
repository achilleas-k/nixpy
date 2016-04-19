# Copyright (c) 2016, German Neuroinformatics Node (G-Node)
#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted under the terms of the BSD License. See
# LICENSE file in the root of the Project.

from __future__ import absolute_import
from .entity import EntityWithMetadata
from . import util
from . import exceptions
from . import Group, DataArray, MultiTag, Tag, Source


class Block(EntityWithMetadata):

    def __init__(self, h5parent, name, type_):
        id_ = util.create_id()
        h5obj = h5parent.create_group(name)
        super(Block, self).__init__(h5obj, id_, name, type_)

    # DataArray
    def _create_data_array(self, name, type_, data_type, shape):
        util.check_entity_name_and_type(name, type_)
        data_arrays = self._h5obj["data_arrays"]
        if name in data_arrays:
            raise exceptions.DuplicateName("create_data_array")
        da = DataArray(data_arrays, name, type_, data_type, shape)
        return da

    def _data_array_count(self):
        pass

    def _get_data_array_by_id(self, id_):
        pass

    def _get_data_array_by_pos(self, index):
        pass

    def _delete_data_array_by_id(self, id_):
        self.data_arrays.remove(id_)

    # MultiTag
    def create_multi_tag(self, name, type_, positions):
        util.check_entity_name_and_type(name, type_)
        util.check_entity_input(positions)
        if not positions.is_valid_entity():
            raise exceptions.UninitializedEntity()
        multi_tags = self._h5obj["multi_tags"]
        if name in multi_tags:
            raise exceptions.DuplicateName("create_multi_tag")
        mtag = MultiTag(multi_tags, name, type_, positions)
        return mtag

    def _multi_tag_count(self):
        pass

    def _get_multi_tag_by_id(self, id_):
        pass

    def _get_multi_tag_by_pos(self, index):
        pass

    def _delete_multi_tag_by_id(self, id_):
        pass

    # Tag
    def create_tag(self, name, type_, position):
        util.check_entity_name_and_type(name, type_)
        tags = self._h5obj["tags"]
        if name in self.tags:
            raise exceptions.DuplicateName("create_tag")
        tag = Tag(tags, name, type_, position)
        return tag

    def _tag_count(self):
        pass

    def _get_tag_by_id(self, id_):
        pass

    def _get_tag_by_pos(self, index):
        pass

    def _delete_tag_by_id(self, id_):
        pass

    # Source
    def _create_source(self, name, type_):
        util.check_entity_name_and_type(name, type_)
        sources = self._h5obj["sources"]
        if name in sources:
            raise exceptions.DuplicateName("create_source")
        src = Source(sources, name, type_)
        return src

    def _source_count(self):
        pass

    def _get_source_by_id(self, id_):
        pass

    def _get_source_by_pos(self, index):
        pass

    def _delete_source_by_id(self, id_):
        pass

    # Group
    def create_group(self, name, type_):
        util.check_entity_name_and_type(name, type_)
        groups = self._h5obj["groups"]
        if name in groups:
            raise exceptions.DuplicateName("create_group")
        grp = Group(groups, name, type_)
        return grp

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

