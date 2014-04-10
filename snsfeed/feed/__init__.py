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

from feedgen.feed import FeedGenerator


@six.add_metaclass(abc.ABCMeta)
class BaseFeed(object):
    FETCHER_CLASS = None
    PARSER_CLASS = None

    def __init__(self, uid):
        assert self.FETCHER_CLASS is not None
        assert self.PARSER_CLASS is not None

        self.uid = uid
        self._parser = None

    def _fetch_content(self):
        fetcher = self.FETCHER_CLASS(self.uid)
        return fetcher.fetch()

    def _ensure_parser(self):
        if self._parser is not None:
            return

        self._parser = self.PARSER_CLASS(self._fetch_content())

    def _reset_parser(self):
        self._parser = None

    def read_metadata(self):
        self._ensure_parser()
        return self._parser.parse_metadata()

    def read_timeline(self):
        self._ensure_parser()
        return self._parser.parse_timeline()

    @abc.abstractmethod
    def set_feed_metadata(self, fg):
        raise NotImplementedError

    @abc.abstractmethod
    def translate_timestamp(self, ts):
        raise NotImplementedError

    def generate_feed(self):
        # 首先是获取和解析原始网页
        # 这里强制删除 parser 对象, 使得每次调用都会进行一次网络请求
        self._reset_parser()
        metadata = self.read_metadata()
        timeline = self.read_timeline()

        fg = FeedGenerator()

        # 设置频道元数据的公共部分
        fg.id(metadata['url'])
        fg.title(metadata['name'])
        fg.link(href=metadata['url'], rel='alternate')
        fg.description(metadata['desc'])

        try:
            fg.logo(metadata['logo'])
        except KeyError:
            pass

        # 设置来源特异元数据
        self.set_feed_metadata(fg)

        # 添加条目
        for item in timeline:
            fe = fg.add_entry()

            # 设置条目信息
            fe.id(item['link'])
            fe.title(item['title'])
            fe.content(item['content'])
            fe.published(self.translate_timestamp(item['time']))
            fe.link(href=item['link'], rel='alternate')

        return fg


# vim:set ai et ts=4 sw=4 sts=4 fenc=utf-8:
