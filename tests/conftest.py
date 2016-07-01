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


"""Pytest configuration."""

from __future__ import absolute_import, print_function

import os
from time import sleep

import pytest
from flask import Flask
from flask_babelex import Babel
from invenio_db import InvenioDB, db
from invenio_indexer import InvenioIndexer
from invenio_jsonschemas import InvenioJSONSchemas
from invenio_records import InvenioRecords
from invenio_search import InvenioSearch

from invenio_marc21 import InvenioMARC21


@pytest.fixture()
def app():
    """Flask application fixture."""
    app = Flask('testapp')
    app.config.update(
        TESTING=True
    )
    return app


@pytest.fixture()
def es_app(request):
    """Flask application with records fixture."""
    app = Flask(__name__)
    app.config.update(
        JSONSCHEMAS_HOST='http://localhost:5000',
        SQLALCHEMY_DATABASE_URI=os.environ.get(
            'SQLALCHEMY_DATABASE_URI', 'sqlite:///test.db'),
    )
    app.config[InvenioJSONSchemas.CONFIG_ENDPOINT] = '/'

    Babel(app)
    if not hasattr(app, 'cli'):
        from flask_cli import FlaskCLI
        FlaskCLI(app)
    InvenioDB(app)
    InvenioRecords(app)
    InvenioMARC21(app)
    search = InvenioSearch(app)
    InvenioIndexer(app)
    InvenioJSONSchemas(app)

    with app.app_context():
        db.create_all()
        list(search.create())
        sleep(10)

    def teardown():
        with app.app_context():
            db.drop_all()
            list(search.delete())

    request.addfinalizer(teardown)

    return app
