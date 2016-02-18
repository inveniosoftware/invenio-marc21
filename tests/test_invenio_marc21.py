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

import pkg_resources
from dojson.contrib.marc21.utils import load
from flask import Flask
from flask_babelex import Babel
from invenio_indexer.api import RecordIndexer
from invenio_records import Record
from invenio_search import InvenioSearch

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


def test_view(app):
    """Test view."""
    Babel(app)
    InvenioMARC21(app)
    with app.test_client() as client:
        res = client.get("/")
        assert res.status_code == 200
        assert 'Welcome to Invenio-MARC21' in str(res.data)


def test_authority_data(es_app):
    """Test indexation using authority data."""
    search = InvenioSearch(es_app)
    search.create()
    indexer = RecordIndexer()
    with es_app.test_request_context():
        data_filename = pkg_resources.resource_filename(
            'invenio_records', 'data/marc21/authority.xml')
        records_data = load(data_filename)
        records = []
        for item in records_data:
            record = Record.create(item)
            record['$schema'] = "mappings/marc21_authority.json"
            es_record = indexer.index(record)
            records.append(es_record)

    for record in records:
        search.client.get(index=record['_index'],
                          doc_type=record['_type'],
                          id=record['_id'])
    search.delete()


def test_bibliographic_data(es_app):
    """Test indexation using bibliographic data."""
    search = InvenioSearch(es_app)
    search.create()
    indexer = RecordIndexer()
    with es_app.test_request_context():
        data_filename = pkg_resources.resource_filename(
            'invenio_records', 'data/marc21/bibliographic.xml')
        records_data = load(data_filename)
        records = []
        for item in records_data:
            record = Record.create(item)
            record['$schema'] = "mappings/marc21_holdings.json"
            es_record = indexer.index(record)
            records.append(es_record)

    for record in records:
        search.client.get(index=record['_index'],
                          doc_type=record['_type'],
                          id=record['_id'])
    search.delete()
