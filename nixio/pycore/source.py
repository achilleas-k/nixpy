# Copyright (c) 2016, German Neuroinformatics Node (G-Node)
#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted under the terms of the BSD License. See
# LICENSE file in the root of the Project.

from .entity import EntityWithMetadata
from . import util
from . import exceptions


class Source(EntityWithMetadata):

    def __init__(self, file, parent, name, type_):
        id_ = util.create_id()
        h5obj = parent._h5obj["sources"].create_group(name)
        super(Source, self).__init__(file, h5obj, id_, name, type_)
        self._source_group = self._h5obj.create_group("sources")
        self._sources_id = dict()
        # self._sources_name = dict()
        # self._sources_list = list()

    # Source
    def create_source(self, name, type_):
        util.check_entity_name_and_type(name, type_)
        if name in self._source_group:
            raise exceptions.DuplicateName("create_source")
        src = Source(self._file, self, name, type_)
        self._add_source(src)
        return src

    def __str__(self):
        pass

    def __repr__(self):
        pass

util.create_container_methods(Source, "source")
