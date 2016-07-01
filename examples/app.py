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


r"""Minimal Flask application example for development.

Usage:

1. Install requrements for this example app by running:

    .. code-block:: console

        $ cd examples
        $ pip install -r requirements.txt
        $ export FLASK_APP=app.py

2. Create database and tables:

    .. code-block:: console

        $ flask db init
        $ flask db create

You can find the database in `examples/app.db`.

3. Load demo records from invenio-records (see
invenio_records/data/marc21/bibliographic.xml):

    .. code-block:: console

        $ wget "https://github.com/inveniosoftware/invenio-records/raw/\
            master/invenio_records/data/marc21/bibliographic.xml"
        $ dojson -i bibliographic.xml -l marcxml do marc21 | \
            flask records create --pid-minter recid

4. Download javascript and css libraries:

    .. code-block:: console

        flask npm
        cd static
        npm install
        cd ..
        npm install -g node-sass clean-css requirejs uglify-js

5. Collect static files and build bundles

    .. code-block:: console

        flask collect -v
        flask assets build


6. Run the development server:

    .. code-block:: console

        flask run -h 0.0.0.0 -p 5000


7. Open in a browser the page `http://0.0.0.0:5000/example/[:pid]`.

   E.g. open `http://0.0.0.0:5000/example/1`

"""

from __future__ import absolute_import, print_function

import os

from flask import Flask, render_template
from flask_babelex import Babel
from invenio_assets import InvenioAssets, NpmBundle
from invenio_db import InvenioDB, db
from invenio_pidstore import InvenioPIDStore
from invenio_pidstore.minters import recid_minter
from invenio_pidstore.models import PersistentIdentifier
from invenio_records import InvenioRecords
from invenio_records.models import RecordMetadata
from invenio_search import InvenioSearch
from invenio_theme import InvenioTheme

from invenio_marc21 import InvenioMARC21

# Create Flask application
app = Flask(__name__)
app.config.update(
    APP_BASE_TEMPLATE="app/base.html",
    SQLALCHEMY_DATABASE_URI=os.getenv('SQLALCHEMY_DATABASE_URI',
                                      'sqlite:///app.db'),
)
Babel(app)
if not hasattr(app, 'cli'):
    from flask_cli import FlaskCLI
    FlaskCLI(app)
InvenioDB(app)
InvenioTheme(app)
assets = InvenioAssets(app)
InvenioRecords(app)
InvenioPIDStore(app)
InvenioSearch(app)
InvenioMARC21(app)

# register CSS bundle
css = NpmBundle(
    # my scss file
    'app/scss/app.scss',
    filters='scss, cleancss',
    output='gen/styles.%(version)s.css',
)
# register my stylesheets
assets.env.register('app_css', css)


@app.route('/example/<string:index>', methods=['GET'])
def example(index):
    """Index page."""
    pid = PersistentIdentifier.query.filter_by(id=index).one()
    record = RecordMetadata.query.filter_by(id=pid.object_uuid).first()

    return render_template("app/detail.html", record=record.json, pid=pid,
                           title="Demosite Invenio Org")
