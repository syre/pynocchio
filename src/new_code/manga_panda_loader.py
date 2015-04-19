# coding=UTF-8
#
# Copyright (C) 2015  Michell Stuttgart

# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option)
# any later version.

# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.

# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.
from lxml import html
import requests


class MangaPandaParser(object):

    _HOST = 'http://www.mangapanda.com'
    _COMIC_INDEX = 'http://www.mangapanda.com/alphabetical'

    def __init__(self, url):
        self._url = url
        self.comics_urls = {}
        self.chapter_urls = {}
        self.pages_urls = []
        self.image_urls = []

    def comic_list(self):
        page = requests.get(MangaPandaParser._COMIC_INDEX)
        tree = html.fromstring(page.text)

        xpath = "//div[@class='series_alpha']/ul[@class='series_alpha']/li/a"
        self.comics_urls = {}

        for comics in tree.xpath(xpath):
            self.comics_urls[comics.text.encode("utf-8")] = \
                'http://www.mangapanda.com'.join(comics.get('href'))

        return self.comics_urls

    def chapters_list(self, comic_url):
        page = requests.get(comic_url)
        tree = html.fromstring(page.text)

        self.chapter_urls = {}
        for chapter in tree.xpath("//table[@id='listing']/tr/td/a"):
            self.chapter_urls[chapter.text.encode("utf-8")] = \
                'http://www.mangapanda.com'.join(chapter.get('href'))

        return self.chapter_urls

    def pages_url(self, chapter_url):
        page = requests.get(chapter_url)
        tree = html.fromstring(page.text)

        self.pages_urls = []

        for option in tree.xpath(
                "//div[@id='selectpage']/select[@id='pageMenu']/option"):
            self.pages_urls.append('http://www.mangapanda.com'.join(
                option.get('value')))

        return self.pages_urls

    def image_url(self, page_url):
        page = requests.get(page_url)
        tree = html.fromstring(page.text)

        self.image_urls = []
        for src in tree.xpath("//div[@id='imgholder']/a/img[@id='img']"):
            self.image_urls .append(src.get('src'))

        return self.image_urls


