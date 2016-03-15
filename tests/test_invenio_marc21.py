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


"""Module tests."""

from __future__ import absolute_import, print_function

import mock
import pkg_resources
from dojson.contrib.marc21 import marc21
from dojson.contrib.marc21.utils import load
from flask import Flask
from invenio_db import db
from invenio_indexer.api import RecordIndexer
from invenio_records import Record
from invenio_search import current_search as search

from invenio_marc21 import InvenioMARC21


def test_version():
    """Test version import."""
    from invenio_marc21 import __version__
    assert __version__


def test_init():
    """Test extension initialization."""
    app = Flask('testapp')
    ext = InvenioMARC21(app)
    assert 'invenio-marc21' in app.extensions

    app = Flask('testapp')
    ext = InvenioMARC21()
    assert 'invenio-marc21' not in app.extensions
    ext.init_app(app)
    assert 'invenio-marc21' in app.extensions


def mock_record_validate(self):
    """Mock validation."""
    pass


@mock.patch('invenio_records.api.Record.validate', mock_record_validate)
def load_records(es_app, filename, schema):
    """Try to index records."""
    indexer = RecordIndexer()
    with es_app.test_request_context():
        data_filename = pkg_resources.resource_filename(
            'invenio_records', filename)
        records_data = load(data_filename)
        records = []
        for item in records_data:
            item_dict = dict(marc21.do(item))
            item_dict['$schema'] = schema
            record = Record.create(item_dict)
            records.append(record)
        db.session.commit()

        es_records = []
        for record in records:
            es_records.append(indexer.index(record))

        for record in es_records:
            search.client.get(index=record['_index'],
                              doc_type=record['_type'],
                              id=record['_id'])


def test_authority_data(es_app, request):
    """Test indexation using authority data."""
    schema = ('http://localhost:5000/'
              'marc21/authority/ad-v1.0.0.json')
    load_records(es_app=es_app, filename='data/marc21/authority.xml',
                 schema=schema)


def test_bibliographic_data(es_app, request):
    """Test indexation using bibliographic data."""
    schema = ('http://localhost:5000/'
              'marc21/bibliographic/bd-v1.0.0.json')
    load_records(es_app=es_app, filename='data/marc21/bibliographic.xml',
                 schema=schema)
