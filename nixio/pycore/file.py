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

    def __init__(self, path, mode=FileMode.ReadWrite):
        self._h5file = h5py.File(name=path, mode=mode)
        self._h5obj = self._h5file  # convenience synonym
        self.format = np.string_("nix")
        self.version = [1, 0, 0]
        self.created_at = util.nowstr()
        self.updated_at = util.nowstr()
        self._root = self._h5file["/"]
        self._data = self._root.create_group("data")
        self._blocks_ids = dict()
        # self._blocks_names = dict()

    @classmethod
    def open(cls, path, mode=FileMode.ReadWrite):
        return cls(path, mode)

    def force_created_at(self):
        pass

    def force_updated_at(self):
        pass

    def create_block(self, name, type_):
        util.check_entity_name_and_type(name, type_)
        if name in self._data:
            raise ValueError("Block with the given name already exists!")
        block = Block(self, self._data, name, type_)
        self._add_block(block)
        return block

    def _add_block(self, block):
        # Two dictionaries per container indexed by id and name
        self._blocks_ids[block.id] = block
        # self._blocks_names[block.name] = block

    def _block_count(self):
        pass

    def _get_block_by_id(self, id_):
        return self._blocks_ids[id_]

    def _get_block_by_pos(self, pos):
        return list(self._blocks_ids.values())[pos]

    def _delete_block_by_id(self, id_):
        name = self._blocks_ids[id_].name
        # Delete file object and Entity from dictionaries
        del self._data[name]
        del self._blocks_ids[id_]
        # del self._blocks_names[name]

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
        self._h5file.close()

    def validate(self):
        pass

util.create_h5props(File, ("version", "format", "created_at", "updated_at"))
