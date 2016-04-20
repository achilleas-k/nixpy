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
        self._init_container("data_array")
        self._init_container("tag")
        self._init_container("multi_tag")
        self._init_container("group")
        self._init_container("source")

    def _init_container(self, childclass):
        setattr(self, "_{}_group".format(childclass),
                self._h5obj.create_group(childclass + "s"))
        setattr(self, "_{}s_id".format(childclass), dict())
        setattr(self, "_{}s_name".format(childclass), dict())
        setattr(self, "_{}s_list".format(childclass), list())

    # DataArray
    def _create_data_array(self, name, type_, data_type, shape):
        util.check_entity_name_and_type(name, type_)
        if name in self._data_array_group:
            raise exceptions.DuplicateName("create_data_array")
        da = DataArray(self._data_array_group, name, type_, data_type, shape)
        self._add_data_array(da)
        return da

    # MultiTag
    def create_multi_tag(self, name, type_, positions):
        util.check_entity_name_and_type(name, type_)
        util.check_entity_input(positions)
        if not isinstance(positions, DataArray):
            raise TypeError("DataArray expected for 'positions'")
        multi_tags = self._h5obj["multi_tags"]
        if name in multi_tags:
            raise exceptions.DuplicateName("create_multi_tag")
        mtag = MultiTag(multi_tags, name, type_, positions)
        self._add_multi_tag(mtag)
        return mtag

    # Tag
    def create_tag(self, name, type_, position):
        util.check_entity_name_and_type(name, type_)
        if name in self._tag_group:
            raise exceptions.DuplicateName("create_tag")
        tag = Tag(self._tag_group, name, type_, position)
        self._add_tag(tag)
        return tag

    # Source
    def create_source(self, name, type_):
        util.check_entity_name_and_type(name, type_)
        if name in self._source_group:
            raise exceptions.DuplicateName("create_source")
        src = Source(self._source_group, name, type_)
        self._add_source(src)
        return src

    # Group
    def create_group(self, name, type_):
        util.check_entity_name_and_type(name, type_)
        if name in self._group_group:
            raise exceptions.DuplicateName("create_group")
        grp = Group(self._group_group, name, type_)
        self._add_group(grp)
        return grp


util.create_container_methods(Block, "data_array")
util.create_container_methods(Block, "tag")
util.create_container_methods(Block, "multi_tag")
util.create_container_methods(Block, "group")
util.create_container_methods(Block, "source")
