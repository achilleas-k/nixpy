# Copyright (c) 2016, German Neuroinformatics Node (G-Node)
#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted under the terms of the BSD License. See
# LICENSE file in the root of the Project.


class FileMode(object):
    ReadOnly = 'r'
    ReadWrite = 'a'
    Overwrite = 'w'


class File(object):

    def __init__(self):
        self.version = None
        self.format = None
        self.created_at = None
        self.updated_at = None

    def force_created_at(self):
        pass

    def force_updated_at(self):
        pass

    def create_block(self):
        pass

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

    def open(self):
        pass

    def validate(self):
        pass
