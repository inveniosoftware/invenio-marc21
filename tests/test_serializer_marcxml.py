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

"""Serializer tests."""

from __future__ import absolute_import, print_function

from dojson.contrib.to_marc21 import to_marc21
from invenio_pidstore.models import PersistentIdentifier
from invenio_records import Record
from marshmallow import Schema, fields

from invenio_marc21.serializers.marcxml import MARCXMLSerializer


class MySchema(Schema):
    """Test marshmallow schema."""

    control_number = fields.Str(attribute='pid.pid_value')


def test_serialize(app):
    """Test JSON serialize."""
    data = MARCXMLSerializer(to_marc21, schema_class=MySchema).serialize(
        PersistentIdentifier(pid_type='recid', pid_value='2'),
        Record({'title': 'test'}))
    expected = u"<?xml version='1.0' encoding='UTF-8'?>\n" \
               u'<record xmlns="http://www.loc.gov/MARC21/slim">\n' \
               u'  <controlfield tag="001">2</controlfield>\n' \
               u'</record>\n'
    assert data.decode('utf8') == expected


def test_serialize_search():
    """Test MARCXML serialize."""
    def fetcher(obj_uuid, data):
        return PersistentIdentifier(pid_type='recid', pid_value=data['pid'])

    s = MARCXMLSerializer(to_marc21, schema_class=MySchema)
    data = s.serialize_search(
        fetcher,
        dict(
            hits=dict(
                hits=[
                    {'_source': dict(pid='1'), '_id': 'a', '_version': 1},
                    {'_source': dict(pid='2'), '_id': 'b', '_version': 1},
                ],
                total=2,
            ),
            aggregations={},
        )
    )
    expected = u"<?xml version='1.0' encoding='UTF-8'?>\n" \
               u'<collection xmlns="http://www.loc.gov/MARC21/slim">\n' \
               u'  <record>\n' \
               u'    <controlfield tag="001">1</controlfield>\n' \
               u'  </record>\n' \
               u'  <record>\n' \
               u'    <controlfield tag="001">2</controlfield>\n' \
               u'  </record>\n' \
               u'</collection>\n'
    assert data.decode('utf8') == expected


def test_serialize_oaipmh():
    """Test MARCXML serialize."""
    s = MARCXMLSerializer(to_marc21, schema_class=MySchema)

    tree = s.serialize_oaipmh(
        PersistentIdentifier(pid_type='recid', pid_value='2'),
        {'_source': Record({'title': 'test'})})

    assert tree.getchildren()[0].text == '2'
