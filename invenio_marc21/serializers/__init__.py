# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2016-2018 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

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
