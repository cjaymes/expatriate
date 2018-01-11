# Copyright 2016 Casey Jaymes

# This file is part of Expatriate.
#
# Expatriate is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Expatriate is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Expatriate.  If not, see <http://www.gnu.org/licenses/>.

import logging

import pytest
from expatriate import *

logging.basicConfig(level=logging.DEBUG)

doc = Document()
doc.parse('''<?xml version='1.0' encoding='utf-8'?>
<Root xmlns="http://jaymes.biz">
    <para name="element1">
        text node
    </para>
    <para name="element2"/>
    <para name="element3">
        <para name="subel1">
            <para name="kal-el">
                Superman's dad
            </para>
        </para>
    </para>
</Root>
''')

@pytest.mark.parametrize(
    "test, result",
    (
        (doc.root_element.xpath('.'), [doc.root_element]),
        (doc.xpath('/Root/para'), doc.root_element.children),
        (doc.root_element.xpath('para'), doc.root_element.children),
        (doc.xpath('/Root/para/node()'), [
            doc.root_element[0][0],
            doc.root_element[2][0],
        ]),
        (doc.root_element.xpath('para/node()'), [
            doc.root_element[0][0],
            doc.root_element[2][0],
        ]),
        (doc.xpath('/Root/para/para'), [
            doc.root_element[2][0],
        ]),
        (doc.root_element.xpath('para/para'), [
            doc.root_element[2][0],
        ]),
        (doc.xpath('/Root/para/para/para'), [
            doc.root_element[2][0][0],
        ]),
        (doc.root_element.xpath('para/para/para'), [
            doc.root_element[2][0][0],
        ]),
        (doc.xpath('/Root/para/para/para/text()'), [
            doc.root_element[2][0][0][0],
        ]),
        (doc.root_element.xpath('para/para/para/text()'), [
            doc.root_element[2][0][0][0],
        ]),
    )
)
def test_steps(test, result):
    assert test == result
