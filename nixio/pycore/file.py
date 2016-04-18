# Copyright (c) 2016, German Neuroinformatics Node (G-Node)
#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted under the terms of the BSD License. See
# LICENSE file in the root of the Project.
from __future__ import absolute_import

import h5py
import numpy as np

from . import util
from . import Block


class FileMode(object):
    ReadOnly = 'r'
    ReadWrite = 'a'
    Overwrite = 'w'


class File(object):

    _h5attrs = ["version", "format", "created_at", "updated_at"]

    def __init__(self, path, mode=FileMode.ReadWrite):
        self._h5file = h5py.File(name=path, mode=mode)
        self.format = np.string_("nix")
        self.version = [1, 0, 0]
        self.created_at = util.nowstr()
        self.updated_at = util.nowstr()
        self._root = self._h5file["/"]
        self._data = self._root["data"]

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
            # Check if item in _h5obj.attrs?
            self._h5obj.attrs.modify(item, value)
        except (KeyError, AttributeError):
            raise AttributeError("{} has no attribute {}".format(
                type(self), item
            ))

    @classmethod
    def open(cls, path, mode=FileMode.ReadWrite):
        return cls(path, mode)

    def force_created_at(self):
        pass

    def force_updated_at(self):
        pass

    def create_block(self, name, type_):
        util.check_entity_name_and_type(name, type_)
        if name in self:
            raise ValueError("Block with the given name already exists!")
        h5block = self._data.create_group(name)
        block = Block(h5block, name, type_)
        return block

    def _block_count(self):
        pass

    def _get_block_by_id(self):
        pass

    def _get_block_by_pos(self):
        pass

    def _delete_block_by_id(self):
        pass

    def create_section(self):
        pass

    def _section_count(self):
        pass

    def _get_section_by_id(self):
        pass

    def _get_section_by_pos(self):
        pass

    def _delete_section_by_id(self):
        pass

    def is_open(self):
        pass

    def close(self):
        pass

    def validate(self):
        pass
