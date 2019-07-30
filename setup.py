# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2016-2018 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Invenio module with nice defaults for MARC21 overlay."""

import os

from setuptools import find_packages, setup


readme = open('README.rst').read()
history = open('CHANGES.rst').read()

tests_require = [
    'check-manifest>=0.25',
    'coverage>=4.5.3',
    'invenio-db>=1.0.0',
    'invenio-i18n>=1.0.0',
    'invenio-indexer>=1.1.0',
    'invenio-pidstore>=1.0.0',
    'invenio-records>=1.0.0',
    'isort>=4.2.2',
    'mock>=1.3.0',
    'pydocstyle>=3.0.0',
    'pytest-cov>=2.7.1',
    'pytest-pep8>=1.0.6',
    'pytest>=4.6.4,<5.0.0',
]

invenio_search_version = '1.2.0'

extras_require = {
    'docs': [
        'Sphinx>=1.5.2',
    ],
    # Elasticsearch version
    'elasticsearch2': [
        'invenio-search[elasticsearch2]>={}'.format(invenio_search_version),
    ],
    'elasticsearch5': [
        'invenio-search[elasticsearch5]>={}'.format(invenio_search_version),
    ],
    'elasticsearch6': [
        'invenio-search[elasticsearch6]>={}'.format(invenio_search_version),
    ],
    'elasticsearch7': [
        'invenio-search[elasticsearch7]>={}'.format(invenio_search_version),
    ],
    'tests': tests_require,
}

extras_require['all'] = []
for name, reqs in extras_require.items():
    if name[0] == ':' or name in (
            'elasticsearch2', 'elasticsearch5', 'elasticsearch6', 'elasticsearch7'):
        continue
    extras_require['all'].extend(reqs)

setup_requires = [
    'Babel>=1.3',
    'pytest-runner>=2.6.2',
]

install_requires = [
    'Flask>=0.11.1',
    'Flask-BabelEx>=0.9.3',
    'dojson>=1.3.0',
    'invenio-jsonschemas>=1.0.0',
    'invenio-records-rest>=1.0.0',
    'invenio-records-ui>=1.0.0',
]

packages = find_packages()


# Get the version string. Cannot be done with import!
g = {}
with open(os.path.join('invenio_marc21', 'version.py'), 'rt') as fp:
    exec(fp.read(), g)
    version = g['__version__']

setup(
    name='invenio-marc21',
    version=version,
    description=__doc__,
    long_description=readme + '\n\n' + history,
    keywords='invenio MARC21',
    license='MIT',
    author='CERN',
    author_email='info@inveniosoftware.org',
    url='https://github.com/inveniosoftware/invenio-marc21',
    packages=packages,
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    entry_points={
        'invenio_base.apps': [
            'invenio_marc21 = invenio_marc21:InvenioMARC21',
        ],
        'invenio_i18n.translations': [
            'messages = invenio_marc21',
        ],
        'invenio_jsonschemas.schemas': [
            'marc21 = dojson.contrib.marc21.schemas',
        ],
        'invenio_search.mappings': [
            'marc21 = invenio_marc21.mappings',
        ],
    },
    extras_require=extras_require,
    install_requires=install_requires,
    setup_requires=setup_requires,
    tests_require=tests_require,
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
        'Development Status :: 5 - Production/Stable',
    ],
)
