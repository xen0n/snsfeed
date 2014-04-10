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

import pyquery

from . import BaseParser


def _parse_item(elem):
    '''解析一个 #talkList > li 元素里的信息.'''

    sel = pyquery.PyQuery(elem)

    content_elems = sel('.msgCnt')
    content = pyquery.PyQuery(content_elems[0]).text().strip()
    if len(content_elems) > 1:
        reply_elem = pyquery.PyQuery(content_elems[1])
        reply_content = reply_elem.text().strip()
        all_content = '{0} //@{1}'.format(content, reply_content).lstrip()
    else:
        all_content = content

    this_link = sel('.time:last')
    timestamp = int(this_link.attr('rel'))
    url = this_link.attr('href')

    return {
            'title': content,
            'content': all_content,
            'time': timestamp,
            'link': url,
            }


class TXWeiboParser(BaseParser):
    '''腾讯微博用户页面解析模块.'''

    def __init__(self, content):
        super(TXWeiboParser, self).__init__(content)

    def parse_metadata(self):
        title_elem = self._pq('.m_profile_name > .tit > .text_user')
        name = title_elem.text().strip()
        url = title_elem.attr('href')

        summary_elem = self._pq('.m_profile_info > .summary')
        summary = summary_elem.text().strip()

        avatar_elem = self._pq('#userAvatar')
        avatar_url = avatar_elem.attr('src')

        return {
                'name': name,
                'url': url,
                'desc': summary,
                'logo': avatar_url,
                }

    def parse_timeline(self):
        item_list = self._pq('#talkList > li[id]')
        return [_parse_item(elem) for elem in item_list]


# vim:set ai et ts=4 sw=4 sts=4 fenc=utf-8:
