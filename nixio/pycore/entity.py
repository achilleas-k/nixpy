# Copyright (c) 2016, German Neuroinformatics Node (G-Node)
#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted under the terms of the BSD License. See
# LICENSE file in the root of the Project.

from time import time
from . import util


class Entity(object):

    def __init__(self, h5obj, id_):
        self._h5obj = h5obj
        self.id = id_
        self.created_at = str(int(time()))
        self.updated_at = str(int(time()))

    def force_created_at(self, t):
        # TODO: Check if convertible to date
        self.created_at = str(t)

    def force_updated_at(self, t):
        # TODO: Check if convertible to date
        self.updated_at = str(t)

util.create_h5props(Entity, ("created_at", "updated_at", "id"))


class NamedEntity(Entity):

    def __init__(self, h5obj, id_, name, type_):
        super(NamedEntity, self).__init__(h5obj, id_)
        self.name = name
        self.type = type_

util.create_h5props(NamedEntity, ("name", "type", "definition"))


class EntityWithMetadata(NamedEntity):

    def __init__(self, h5obj, id_, name, type_):
        super(EntityWithMetadata, self).__init__(h5obj, id_, name, type_)
        self.metadata = None  # TODO: Metadata section


class EntityWithSources(EntityWithMetadata):

    def __init__(self, h5obj, id_, name, type_):
        super(EntityWithSources, self).__init__(h5obj, id_, name, type_)
        self.sources = None  # TODO: Sources

    def _source_count(self):
        return len(self._h5obj["sources"])

    def _get_source_by_id(self, id_):
        return self._h5obj["sources"][id_]

    def _get_source_by_pos(self, pos):
        # TODO: Check if h5py ordering guaranteed stable
        return list(self._h5obj["sources"].values())[pos]

    def _add_source_by_id(self, source):
        pass

    def _remove_source_by_id(self, id_):
        pass

