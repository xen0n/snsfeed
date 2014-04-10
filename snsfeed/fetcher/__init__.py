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

import abc
import six
import requests

UA = 'Mozilla/5.0 (X11; Linux x86_64; rv:27.0) Gecko/20100101 Firefox/27.0'


@six.add_metaclass(abc.ABCMeta)
class BaseFetcher(object):
    def __init__(self, uid):
        self.uid = uid

    @abc.abstractmethod
    def get_url(self):
        raise NotImplementedError

    @abc.abstractmethod
    def fetch(self):
        raise NotImplementedError

    def get_headers(self):
        return {
                'User-Agent': UA,
                }

    def _do_simple_get(self):
        response = requests.get(self.get_url(), headers=self.get_headers())
        if response.ok:
            return response.content


# vim:set ai et ts=4 sw=4 sts=4 fenc=utf-8:
