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

from __future__ import unicode_literals

import os

from weiyu import init


# weiyu init
_PROJECT_PATH = os.path.join(os.path.dirname(__file__), '../..')
os.chdir(_PROJECT_PATH)

# calm lint
application = None

# real application is here
init.inject_app()


# Sentry init
if 'SENTRY_DSN' in os.environ:
    from raven import Client
    from raven.middleware import Sentry

    sentry_client = Client()
    application = Sentry(application, client=sentry_client)


# vim:set ai et ts=4 sw=4 sts=4 fenc=utf-8:
