# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2016-2018 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Base class for dojson based serializers."""

from __future__ import absolute_import, print_function

from dojson.contrib.marc21.utils import GroupableOrderedDict
from invenio_records_rest.serializers.base import PreprocessorMixin


class DoJSONSerializer(PreprocessorMixin):
    """Base class for marshmallow serializers."""

    def __init__(self, dojson_model, replace_refs=False):
        """Initialize serializer.

        :param dojson_model: The DoJSON model able to convert JSON through the
            ``do()`` function.
        :param replace_refs: Boolean value to configure if the ``$ref`` keys
            are replaced. (Default: ``False``)
        """
        self.dojson_model = dojson_model
        super(DoJSONSerializer, self).__init__(replace_refs=replace_refs)

    def dump(self, obj):
        """Serialize object with schema.

        :param obj: The object to serialize.
        :returns: The object serialized.
        """
        return GroupableOrderedDict(self.dojson_model.do(obj))

    def transform_record(self, pid, record, links_factory=None):
        """Transform record into an intermediate representation.

        :param pid: The :class:`invenio_pidstore.models.PersistentIdentifier`
            instance.
        :param record: The :class:`invenio_records.api.Record` instance.
        :param links_factory: The link factory. (Default: ``None``)
        :returns: The intermediate representation for the record.
        """
        return self.dump(self.preprocess_record(pid, record,
                         links_factory=links_factory))

    def transform_search_hit(self, pid, record_hit, links_factory=None):
        """Transform search result hit into an intermediate representation.

        :param pid: The :class:`invenio_pidstore.models.PersistentIdentifier`
            instance.
        :param record_hit: A dictionary containing a ``'_source'`` key with
            the record data.
        :param links_factory: The link factory. (Default: ``None``)
        :returns: The intermediate representation for the record.
        """
        return self.dump(self.preprocess_search_hit(pid, record_hit,
                         links_factory=links_factory))
