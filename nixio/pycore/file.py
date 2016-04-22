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
        block = Block._create_new(self._data, name, type_)
        return block

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

util.create_h5props(File, ["version", "format", "created_at", "updated_at"])
util.create_container_methods(File, Block, "block")
