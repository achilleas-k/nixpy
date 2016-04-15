# Copyright (c) 2016, German Neuroinformatics Node (G-Node)
#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted under the terms of the BSD License. See
# LICENSE file in the root of the Project.


class Entity(object):

    def __init__(self):
        self.id = None
        self.created_at = None
        self.updated_at = None

    def force_created_at(self, t):
        self.created_at = t

    def force_updated_at(self, t):
        self.updated_at = t


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

