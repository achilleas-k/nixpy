# Copyright (c) 2016, German Neuroinformatics Node (G-Node)
#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted under the terms of the BSD License. See
# LICENSE file in the root of the Project.

from time import time


class Entity(object):

    _h5attrs = ["created_at", "updated_at", "id"]

    def __init__(self, group):
        self._h5obj = group
        if id_:
            self.entity_group.entity_id = id_
        self.created_at = str(int(time()))
        self.updated_at = str(int(time()))

    def __getattr__(self, item):
        try:
            if item not in self._h5attrs:
                raise AttributeError
            return self._h5obj.attrs.get(item)
        except (KeyError, AttributeError):
            raise AttributeError("{} has no attribute {}".format(
                type(self), item
            ))

    def __setattr__(self, item, value):
        try:
            if item not in self._h5attrs:
                raise AttributeError
            # Check if item in attrs?
            self._h5obj.attrs.modify(item, value)
        except (KeyError, AttributeError):
            raise AttributeError("{} has no attribute {}".format(
                type(self), item
            ))

    def force_created_at(self, t):
        # TODO: Check if convertible to date
        self.created_at = str(t)

    def force_updated_at(self, t):
        # TODO: Check if convertible to date
        self.updated_at = str(t)


class NamedEntity(Entity):

    def __init__(self):
        super(NamedEntity, self).__init__()
        self.name = None
        self.type = None
        self.definition = None


class EntityWithMetadata(NamedEntity):

    def __init__(self):
        super(EntityWithMetadata, self).__init__()
        self.metadata = None


class EntityWithSources(EntityWithMetadata):

    def __init__(self):
        super(EntityWithSources, self).__init__()

    def _source_count(self):
        pass

    def _has_source_by_id(self, id_):
        pass

    def _get_source_by_id(self, id_):
        pass

    def _get_source_by_pos(self, pos):
        pass

    def _add_source_by_id(self, source):
        pass

    def _remove_source_by_id(self, id_):
        pass

