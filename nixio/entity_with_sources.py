# Copyright (c) 2016, German Neuroinformatics Node (G-Node)
#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted under the terms of the BSD License. See
# LICENSE file in the root of the Project.
from __future__ import (absolute_import, division, print_function)

from .entity import Entity
from .section import Section
from .source import Source
from .container import LinkContainer
from . import util


class SourceLinkContainer(LinkContainer):

    # TODO: Sources returned from this container have an incorrect _parent
    # This is the same issue that we have with Sections. It should probably be
    # solved the same way

    def append(self, item):
        if util.is_uuid(item):
            item = self._inst_item(self._backend.get_by_id(item))

        if not hasattr(item, "id"):
            raise TypeError("NIX entity or id string required for append")

        if not self._itemstore._parent.find_sources(
                filtr=lambda x: x.id == item.id
        ):
            raise RuntimeError("This item cannot be appended here.")

        self._backend.create_link(item, item.id)

class EntityWithSources(EntityWithMetadata):

class EntityWithSources(Entity):

    def __init__(self, nixparent, h5group):
        super(EntityWithSources, self).__init__(nixparent, h5group)
        self._sources = None

    @classmethod
    def _create_new(cls, nixparent, h5parent, name, type_):
        newentity = super(EntityWithSources, cls)._create_new(
            nixparent, h5parent, name, type_
        )
        return newentity

    @property
    def sources(self):
        """
        A property containing all Sources referenced by the group. Sources
        can be obtained by index or their id. Sources can be removed from the
        list, but removing a referenced Source will not remove it from the
        file. New Sources can be added using the append method of the list.
        This is a read only attribute.
        """
        if self._sources is None:
            self._sources = SourceLinkContainer("sources", self, Source,
                                                self._parent.sources)
        return self._sources

    @property
    def metadata(self):
        """
        Associated metadata of the entity. Sections attached to the entity
        via this attribute can provide additional annotations. This is an
        optional read-write property, and can be None if no metadata is
        available.

        :type: Section
        """
        if "metadata" in self._h5group:
            return Section(None, self._h5group.open_group("metadata"))
        else:
            return None

    @metadata.setter
    def metadata(self, sect):
        if not isinstance(sect, Section):
            raise TypeError("Error setting metadata to {}. Not a Section."
                            .format(sect))
        self._h5group.create_link(sect, "metadata")
