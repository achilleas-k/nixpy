# Copyright (c) 2016, German Neuroinformatics Node (G-Node)
#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted under the terms of the BSD License. See
# LICENSE file in the root of the Project.
from __future__ import (absolute_import, division, print_function)

from . import util
from .section import Section
from .source import Source
from .container import LinkContainer


class Entity(object):

    def __init__(self, nixparent, h5group):
        util.check_entity_id(h5group.get_attr("entity_id"))
        self._h5group = h5group
        self._parent = nixparent

    @classmethod
    def _create_new(cls, nixparent, h5parent, name=None, type_=None):
        if name and type_:
            util.check_entity_name_and_type(name, type_)
            id_ = util.create_id()
        else:
            name = util.create_id()
            id_ = name
        h5group = h5parent.open_group(name)
        h5group.set_attr("name", name)
        h5group.set_attr("type", type_)
        h5group.set_attr("entity_id", id_)
        newentity = cls(nixparent, h5group)
        newentity.force_created_at()
        newentity.force_updated_at()
        return newentity

    @property
    def id(self):
        """
        A property providing the ID of the Entity. The id is generated
        automatically, therefore the property is read-only.

        :rtype: str
        """
        return self._h5group.get_attr("entity_id")

    @property
    def created_at(self):
        """
        The creation time of the entity. This is a read-only property.
        Use `force_created_at` in order to change the creation time.

        :rtype: int
        """
        return util.str_to_time(self._h5group.get_attr("created_at"))

    def force_created_at(self, t=None):
        """
        Sets the creation time `created_at` to the given time
        (default: current time).

        :param t: The time to set.
        :type t: int
        """
        if t is None:
            t = util.now_int()
        else:
            util.check_attr_type(t, int)
        self._h5group.set_attr("created_at", util.time_to_str(t))

    @property
    def updated_at(self):
        """
        The time of the last update of the entity. This is a read-only
        property. Use `force_updated_at` in order to change the update
        time.

        :rtype: int
        """
        return util.str_to_time(self._h5group.get_attr("updated_at"))

    def force_updated_at(self, t=None):
        """
        Sets the update time `updated_at` to the given time.
        (default: current time)

        :param t: The time to set.
        :type t: int
        """
        if t is None:
            t = util.now_int()
        else:
            util.check_attr_type(t, int)
        self._h5group.set_attr("updated_at", util.time_to_str(t))

    @property
    def definition(self):
        """
        The definition of the entity. The definition can contain a textual
        description of the entity. This is an optional read-write
        property, and can be None if no definition is available.

        :type: str
        """
        return self._h5group.get_attr("definition")

    @definition.setter
    def definition(self, d):
        util.check_attr_type(d, str)
        self._h5group.set_attr("definition", d)

    @property
    def name(self):
        """
        The name of an entity. The name serves as a human readable
        identifier. This is a read-only property; entities cannot be
        renamed.

        :type: str
        """
        return self._h5group.get_attr("name")

    @property
    def type(self):
        """
        The type of the entity. The type is used in order to add semantic
        meaning to the entity. This is a read-write property, but it can't
        be set to None.

        :type: str
        """
        return self._h5group.get_attr("type")

    @type.setter
    def type(self, t):
        if t is None:
            raise AttributeError("type can't be None")
        util.check_attr_type(t, str)
        self._h5group.set_attr("type", t)

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

    def __eq__(self, other):
        if hasattr(other, "id"):
            return self.id == other.id
        else:
            return False

    def __hash__(self):
        return hash(self.id)

    def __str__(self):
        return "{}: {{name = {}, type = {}, id = {}}}".format(
            type(self).__name__, self.name, self.type, self.id
        )

    def __repr__(self):
        return self.__str__()


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
