# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2016-2018 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

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
