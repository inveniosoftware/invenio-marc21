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

"""Record serialization."""

from __future__ import absolute_import, print_function

from dojson.contrib.to_marc21 import to_marc21
from invenio_records_rest.serializers.response import record_responsify, \
    search_responsify
from pkg_resources import resource_filename

from .marcxml import MARCXMLSerializer

xslt_dublincore_oai = resource_filename(
    'invenio_marc21', 'xslts/MARC21slim2OAIDC.xsl')
xslt_dublincore_rdf = resource_filename(
    'invenio_marc21', 'xslts/MARC21slim2RDFDC.xsl')
xslt_dublincore_SRW = resource_filename(
    'invenio_marc21', 'xslts/MARC21slim2SRWDC.xsl')
xslt_mods = resource_filename('invenio_marc21', 'xslts/MARC21slim2MODS3-6.xsl')

#: MARCXML serializer.
marcxml_v1 = MARCXMLSerializer(to_marc21)
#: MARCXML record serializer
marcxml_v1_response = record_responsify(marcxml_v1, 'application/marcxml+xml')
#: MARCXML search serializer
marcxml_v1_search = search_responsify(marcxml_v1, 'application/marcxml+xml')

#: DublinCore serializer.
dublincore_v1 = MARCXMLSerializer(to_marc21, xslt_filename=xslt_dublincore_oai)
#: DublinCore record serializer.
dublincore_v1_response = record_responsify(
    dublincore_v1, 'application/xml')
#: DublinCore search serializer.
dublincore_v1_search = search_responsify(
    dublincore_v1, 'application/xml')

#: MODS serializer.
mods_v1 = MARCXMLSerializer(to_marc21, xslt_filename=xslt_mods)
#: DublinCore record serializer.
mods_v1_response = record_responsify(mods_v1, 'application/mods+xml')
#: DublinCore search serializer.
mods_v1_search = search_responsify(mods_v1, 'application/mods+xml')
