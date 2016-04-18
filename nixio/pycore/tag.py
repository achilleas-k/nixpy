# Copyright (c) 2016, German Neuroinformatics Node (G-Node)
#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted under the terms of the BSD License. See
# LICENSE file in the root of the Project.

from .entity import EntityWithSources


class Tag(EntityWithSources):

    def __init__(self):
        super(Tag, self).__init__()
        self.units = None
        self.position = None
        self.extent = None

    def _add_reference_by_id(self):
        pass

    def _has_reference_by_id(self):
        pass

    def _reference_count(self):
        pass

    def _get_reference_by_id(self):
        pass

    def _get_reference_by_pos(self):
        pass

    def _delete_reference_by_id(self):
        pass

    def create_feature(self):
        pass

    def _has_feature_by_id(self):
        pass

    def _feature_count(self):
        pass

    def _get_feature_by_id(self):
        pass

    def _get_feature_by_pos(self):
        pass

    def _delete_feature_by_id(self):
        pass

    def retrieve_data(self):
        pass

    def retrieve_feature_data(self):
        pass

    def __str__(self):
        pass

    def __repr__(self):
        pass
