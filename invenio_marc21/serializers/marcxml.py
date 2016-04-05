# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2016 CERN.
#
# Invenio is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# Invenio is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Invenio; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307, USA.
#
# In applying this license, CERN does not
# waive the privileges and immunities granted to it by virtue of its status
# as an Intergovernmental Organization or submit itself to any jurisdiction.

"""MARC21 based serializer."""

from __future__ import absolute_import, print_function

from dojson.contrib.to_marc21.utils import dumps, dumps_etree
from invenio_records.api import Record

from .dojson import DoJSONSerializer


class MARCXMLSerializer(DoJSONSerializer):
    """DoJSON based MARCXML serializer for records.

    Note: This serializer is not suitable for serializing large number of
    records due to high memory usage.
    """

    def __init__(self, dojson_model, xslt_filename=None, schema_class=None,
                 replace_refs=False):
        """."""
        self.dumps_kwargs = dict(xslt_filename=xslt_filename) if \
            xslt_filename else {}

        self.schema_class = schema_class
        super(MARCXMLSerializer, self).__init__(
            dojson_model, replace_refs=replace_refs)

    def dump(self, obj):
        """Dump object."""
        if self.schema_class:
            obj = self.schema_class().dump(obj).data
        return super(MARCXMLSerializer, self).dump(obj)

    def serialize(self, pid, record, links_factory=None):
        """Serialize a single record and persistent identifier.

        :param pid: Persistent identifier instance.
        :param record: Record instance.
        :param links_factory: Factory function for the link generation,
                              which are added to the response.
        """
        return dumps(self.transform_record(pid, record, links_factory),
                     **self.dumps_kwargs)

    def serialize_search(self, pid_fetcher, search_result,
                         item_links_factory=None, **kwargs):
        """Serialize a search result.

        :param pid_fetcher: Persistent identifier fetcher.
        :param search_result: Elasticsearch search result.
        :param item_links_factory: Factory function for the items in result.

        """
        ret = [self.transform_search_hit(pid_fetcher(hit['_id'],
                                         hit['_source']),
                                         hit,
                                         links_factory=item_links_factory)
               for hit in search_result['hits']['hits']]

        return dumps(ret, **self.dumps_kwargs)

    def serialize_oaipmh(self, pid, record):
        """Serialize a single record for OAI-PMH."""
        obj = self.transform_record(pid, record['_source']) \
            if isinstance(record['_source'], Record) \
            else self.transform_search_hit(pid, record)

        return dumps_etree(obj, **self.dumps_kwargs)
