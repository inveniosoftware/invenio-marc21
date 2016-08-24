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

"""Invenio module with nice defaults for MARC21 overlay."""

from __future__ import absolute_import, print_function

from . import config
from .views import blueprint


class InvenioMARC21(object):
    """Invenio-MARC21 extension."""

    def __init__(self, app=None):
        """Extension initialization.

        :param app: An instance of :class:`flask.Flask`.
        """
        if app:
            self.init_app(app)

    def init_app(self, app):
        """Flask application initialization.

        :param app: An instance of :class:`flask.Flask`.
        """
        self.init_config(app)
        app.register_blueprint(blueprint)
        app.extensions['invenio-marc21'] = self

    def init_config(self, app):
        """Initialize configuration.

        :param app: An instance of :class:`flask.Flask`.
        """
        app.config.setdefault(
            'MARC21_BASE_TEMPLATE',
            app.config.get('BASE_TEMPLATE',
                           'invenio_marc21/base.html'))
        for k in dir(config):
            if k.startswith('MARC21_'):
                app.config.setdefault(k, getattr(config, k))
