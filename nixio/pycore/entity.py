# Copyright (c) 2016, German Neuroinformatics Node (G-Node)
#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted under the terms of the BSD License. See
# LICENSE file in the root of the Project.

from time import time
from . import util
from . import exceptions


class Entity(object):

    def __init__(self, file, h5obj, id_):
        self._file = file
        self._h5obj = h5obj
        self.id = id_
        self.created_at = int(time())
        self.updated_at = int(time())

    def force_created_at(self, t):
        # TODO: Check if convertible to date
        self.created_at = t

    def force_updated_at(self, t):
        # TODO: Check if convertible to date
        self.updated_at = t

util.create_h5props(Entity, ("created_at", "updated_at", "id"))


class NamedEntity(Entity):

    def __init__(self, file, h5obj, id_, name, type_):
        super(NamedEntity, self).__init__(file, h5obj, id_)
        self.name = name
        self.type = type_

    def __str__(self):
        return "{}: {{name = {}, type = {}, id = {}}}".format(
            type(self).__name__, self.name, self.type, self.id
        )

    def __repr__(self):
        return self.__str__()

util.create_h5props(NamedEntity, ("name", "type", "definition"))


class EntityWithMetadata(NamedEntity):

    def __init__(self, file, h5obj, id_, name, type_):
        super(EntityWithMetadata, self).__init__(file, h5obj, id_, name,
                                                 type_)
        self.metadata = None  # TODO: Metadata section


class EntityWithSources(EntityWithMetadata):

    def __init__(self, file, block, h5obj, id_, name, type_):
        super(EntityWithSources, self).__init__(file, h5obj, id_, name, type_)
        self._block = block
