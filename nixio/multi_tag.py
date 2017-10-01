# Copyright (c) 2016, German Neuroinformatics Node (G-Node)
#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted under the terms of the BSD License. See
# LICENSE file in the root of the Project.
from __future__ import (absolute_import, division, print_function)

from .metadata_reference import create_metadata_prop
from .tag import BaseTag
from .data_array import DataArray
from .source_link_container import SourceLinkContainer
from .data_view import DataView
from .link_type import LinkType
from .exceptions import (OutOfBounds, IncompatibleDimensions,
                         UninitializedEntity)

from .tag import ReferenceProxyList, FeatureProxyList


class MultiTag(BaseTag):

    def __init__(self, nixparent, h5group):
        super(MultiTag, self).__init__(nixparent, h5group)
        self.metadata = create_metadata_prop()
        self._sources = None

    @classmethod
    def _create_new(cls, nixparent, h5parent, name, type_, positions):
        newentity = super(MultiTag, cls)._create_new(nixparent, h5parent,
                                                     name, type_)
        newentity.positions = positions
        return newentity

    @property
    def positions(self):
        """
        The positions defined by the tag. This is a read-write property.

        :type: DataArray
        """
        return DataArray(self._parent, self._h5group.open_group("positions"))

    @positions.setter
    def positions(self, da):
        if da is None:
            raise TypeError("MultiTag.positions cannot be None.")
        if "positions" in self._h5group:
            del self._h5group["positions"]
        self._h5group.create_link(da, "positions")
        self.force_updated_at()

    @property
    def extents(self):
        """
        The extents defined by the tag. This is an optional read-write
        property and may be set to None.

        :type: DataArray or None
        """
        if "extents" in self._h5group:
            return DataArray(self._parent, self._h5group.open_group("extents"))
        else:
            return None

    @extents.setter
    def extents(self, da):
        if da is None:
            del self._h5group["extents"]
        else:
            self._h5group.create_link(da, "extents")

    def _get_slice(self, data, index):
        offset, count = self._get_offset_and_count(data, index)
        sl = tuple(slice(o, o+c) for o, c in zip(offset, count))
        return sl

    def _get_offset_and_count(self, data, index):
        offsets = []
        counts = []
        positions = self.positions
        extents = self.extents

        pos_size = positions.data_extent if positions else tuple()
        ext_size = extents.data_extent if extents else tuple

        if not positions or index >= pos_size[0]:
            raise OutOfBounds("Index out of bounds of positions!")

        if extents and index >= ext_size[0]:
            raise OutOfBounds("Index out of bounds of extents!")

        if len(pos_size) == 1 and len(data.dimensions) != 1:
            raise IncompatibleDimensions(
                "Number of dimensions in positions does not match "
                "dimensionality of data",
                "MultiTag._get_offset_and_count"
            )

        if len(pos_size) > 1 and pos_size[1] > len(data.dimensions):
            raise IncompatibleDimensions(
                "Number of dimensions in positions does not match "
                "dimensionality of data",
                "MultiTag._get_offset_and_count"
            )

        if (extents and len(ext_size) > 1 and
                ext_size[1] > len(data.dimensions)):
            raise IncompatibleDimensions(
                "Number of dimensions in extents does not match "
                "dimensionality of data",
                "MultiTag._get_offset_and_count"
            )

        offset = positions[index, 0:len(data.dimensions)]

        units = self.units
        for idx in range(len(offset)):
            dim = data.dimensions[idx]
            unit = None
            if idx <= len(units) and len(units):
                unit = units[idx]
            offsets.append(self._pos_to_idx(offset[idx], unit, dim))

        if extents:
            extent = extents[index, 0:len(data.dimensions)]
            for idx in range(len(extent)):
                dim = data.dimensions[idx]
                unit = None
                if idx <= len(units) and len(units):
                    unit = units[idx]
                c = self._pos_to_idx(offset[idx] + extent[idx],
                                     unit, dim) - offsets[idx]
                counts.append(c if c > 1 else 1)

        return offsets, counts

    def retrieve_data(self, posidx, refidx):
        references = self.references
        positions = self.positions
        extents = self.extents
        if len(references) == 0:
            raise OutOfBounds("There are no references in this multitag!")

        if (posidx >= positions.data_extent[0] or
                extents and posidx >= extents.data_extent[0]):
            raise OutOfBounds("Index out of bounds of positions or extents!")

        if refidx >= len(references):
            raise OutOfBounds("Reference index out of bounds.")

        ref = references[refidx]
        dimcount = len(ref.dimensions)
        if len(positions.data_extent) == 1 and dimcount != 1:
            raise IncompatibleDimensions(
                "Number of dimensions in position or extent do not match "
                "dimensionality of data",
                "MultiTag.retrieve_data")
        if len(positions.data_extent) > 1:
            if (positions.data_extent[1] > dimcount or
                    extents and extents.data_extent[1] > dimcount):
                raise IncompatibleDimensions(
                    "Number of dimensions in position or extent do not match "
                    "dimensionality of data",
                    "MultiTag.retrieve_data")
        offset, count = self._get_offset_and_count(ref, posidx)

        if not self._position_and_extent_in_data(ref, offset, count):
            raise OutOfBounds("References data slice out of the extent of the "
                              "DataArray!")
        sl = self._get_slice(ref, posidx)
        return DataView(ref, sl)

    def retrieve_feature_data(self, posidx, featidx):
        if self._feature_count() == 0:
            raise OutOfBounds(
                "There are no features associated with this tag!"
            )
        if featidx > self._feature_count():
            raise OutOfBounds("Feature index out of bounds.")
        feat = self.features[featidx]
        da = feat.data
        if da is None:
            raise UninitializedEntity()
        if feat.link_type == LinkType.Tagged:
            offset, count = self._get_offset_and_count(da, posidx)
            if not self._position_and_extent_in_data(da, offset, count):
                raise OutOfBounds("Requested data slice out of the extent "
                                  "of the Feature!")
            sl = self._get_slice(da, posidx)
            return DataView(da, sl)
        elif feat.link_type == LinkType.Indexed:
            if posidx > da.data_extent[0]:
                raise OutOfBounds("Position is larger than the data stored "
                                  "in the Feature!")
            offset = [0] * len(da.data_extent)
            offset[0] = posidx
            count = list(da.data_extent)
            count[0] = 1

            if not self._position_and_extent_in_data(da, offset, count):
                OutOfBounds("Requested data slice out of the extent of the "
                            "Feature!")
            sl = tuple(slice(o, o+c) for o, c in zip(offset, count))
            return DataView(da, sl)
        # For untagged return the full data
        sl = tuple(slice(0, c) for c in da.data_extent)
        return DataView(da, sl)

    @property
    def references(self):
        """
        A property containing all data arrays referenced by the tag. Referenced
        data arrays can be obtained by index or their id. References can be
        removed from the list, removing a referenced DataArray will not remove
        it from the file. New references can be added using the append method
        of the list.
        This is a read only attribute.

        :type: RefProxyList of DataArray
        """
        if not hasattr(self, "_references"):
            setattr(self, "_references", ReferenceProxyList(self))
        return self._references

    @property
    def features(self):
        """
        A property containing all features of the tag. Features can be obtained
        via their index or their id. Features can be deleted from the list.
        Adding new features to the tag is done using the create_feature method.
        This is a read only attribute.

        :type: ProxyList of Feature.
        """
        if not hasattr(self, "_features"):
            setattr(self, "_features", FeatureProxyList(self))
        return self._features

    @property
    def sources(self):
        """
        A property containing all Sources referenced by the MultiTag. Sources
        can be obtained by index or their id. Sources can be removed from the
        list, but removing a referenced Source will not remove it from the
        file. New Sources can be added using the append method of the list.
        This is a read only attribute.
        """
        if self._sources is None:
            self._sources = SourceLinkContainer(self)
        return self._sources
