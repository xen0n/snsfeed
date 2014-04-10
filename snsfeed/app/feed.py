#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2014 Wang Xuerui <idontknw.wang@gmail.com>
#
# This file is part of snsfeed.
#
# snsfeed is free software: you can redistribute it and/or modify it under
# the terms of the GNU Affero General Public License as published by the
# Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# snsfeed is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public
# License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with snsfeed.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import unicode_literals, absolute_import

from weiyu.shortcuts import http, renderable, view

from . import misc
from . import provider


@http
@renderable('passthru')
@view
def feed_rss_view(request, source_type, source_id):
    source_type = source_type.decode('utf-8')
    source_id = source_id.decode('utf-8')

    try:
        rss_str = provider.generate_rss(source_type, source_id)
    except provider.ProviderNotSupportedError:
        return misc.get_404_response()

    return 200, rss_str, {'mimetype': 'application/rss+xml', }


@http
@renderable('passthru')
@view
def feed_atom_view(request, source_type, source_id):
    source_type = source_type.decode('utf-8')
    source_id = source_id.decode('utf-8')

    try:
        atom_str = provider.generate_atom(source_type, source_id)
    except provider.ProviderNotSupportedError:
        return misc.get_404_response()

    return 200, atom_str, {'mimetype': 'application/atom+xml', }


# vim:set ai et ts=4 sw=4 sts=4 fenc=utf-8:
