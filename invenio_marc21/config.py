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

"""Nice defaults for an overlay using MARC21 format."""

import copy

from invenio_records_rest.config import RECORDS_REST_ENDPOINTS
from invenio_records_rest.query import es_search_factory
from invenio_records_ui.config import RECORDS_UI_ENDPOINTS

MARC21_UI_EXPORT_FORMATS = {
    'recid': {
        'marcxml': dict(
            title='MARCXML',
            serializer='invenio_marc21.serializers.marcxml_v1',
            order=1,
        ),
        'mods': dict(
            title='MODS',
            serializer='invenio_marc21.serializers.mods_v1',
            order=2,
        ),
        'dc': dict(
            title='DublinCore',
            serializer='invenio_marc21.serializers.dublincore_v1',
            order=3,
        ),
        'json': dict(
            title='JSON',
            serializer='invenio_records_rest.serializers.json_v1',
            order=4,
        ),
        # Deprecated names
        'hx': False,
        'hm': False,
        'xm': False,
        'xd': False,
        'xe': False,
        'xn': False,
        'xw': False,
    }
}

MARC21_REST_ENDPOINTS = copy.deepcopy(RECORDS_REST_ENDPOINTS)
MARC21_REST_ENDPOINTS['recid']['search_index'] = 'marc21'
MARC21_REST_ENDPOINTS['recid']['default_media_type'] = \
    'application/marcxml+xml'
MARC21_REST_ENDPOINTS['recid']['record_serializers'] = {
    'application/json': 'invenio_records_rest.serializers:json_v1_response',
    'application/marcxml+xml': (
        'invenio_marc21.serializers:marcxml_v1_response'),
    'application/mods+xml': 'invenio_marc21.serializers:mods_v1_response',
    'application/xml': 'invenio_marc21.serializers:dublincore_v1_response',
}
MARC21_REST_ENDPOINTS['recid']['search_serializers'] = {
    'application/json': 'invenio_records_rest.serializers:json_v1_search',
    'application/marcxml+xml': (
        'invenio_marc21.serializers:marcxml_v1_search'),
    'application/mods+xml': 'invenio_marc21.serializers:mods_v1_search',
    'application/xml': 'invenio_marc21.serializers:dublincore_v1_search',
}

MARC21_UI_ENDPOINTS = copy.deepcopy(RECORDS_UI_ENDPOINTS)
MARC21_UI_ENDPOINTS['recid']['template'] = 'invenio_marc21/detail.html'
MARC21_UI_ENDPOINTS['recid_export'] = {
    'pid_type': 'recid',
    'route': '/record/<pid_value>/export/<any({0}):format>'.format(
        ', '.join(list(MARC21_UI_EXPORT_FORMATS['recid'].keys()))),
    'template': 'invenio_marc21/export.html',
    'view_imp': 'invenio_records_ui.views.export',
}
