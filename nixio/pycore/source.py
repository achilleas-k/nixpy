# Copyright (c) 2016, German Neuroinformatics Node (G-Node)
#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted under the terms of the BSD License. See
# LICENSE file in the root of the Project.

from .entity import EntityWithMetadata
from . import util


class Source(EntityWithMetadata):

    def __init__(self, h5parent, name, type_):
        id_ = util.create_id()
        h5obj = h5parent.create_group(name)
        super(Source, self).__init__(h5obj, id_, name, type_)

    def create_source(self):
        pass

    def _source_count(self):
        pass

    def _has_source_by_id(self):
        pass

    def _get_source_by_id(self):
        pass

    def _get_source_by_pos(self):
        pass

    def _delete_source_by_id(self):
        pass

    def __str__(self):
        pass

    def __repr__(self):
        pass


