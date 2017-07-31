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
<test:Root xmlns="http://jaymes.biz" xmlns:test="http://jaymes.biz/test">
    <para name="element1">
        text node
    </para>
    <test:para name="element2"/>
    <para name="element3">
        <para name="subel1">
            <para name="kal-el">
                Superman's dad
            </para>
        </para>
    </para>
    <!-- comment -->
</test:Root>
''')

@pytest.mark.parametrize(
    "test, result",
    (
        (doc.xpath('child::*'), doc.children),
        (doc.xpath('*'), doc.children),
    )
)
def test_any(test, result):
    assert test == result

@pytest.mark.parametrize(
    "test, result",
    (
        (doc.xpath('child::Root'), [doc.root_element]),
        (doc.root_element.xpath('para'), doc.root_element[:-1]),
    )
)
def test_ncname(test, result):
    assert test == result

@pytest.mark.parametrize(
    "test, result",
    (
        (doc.xpath('child::test:Root'), [doc.root_element]),
        (doc.root_element.xpath('test:para'), [doc.root_element[1]]),
    )
)
def test_qname(test, result):
    assert test == result

@pytest.mark.parametrize(
    "test, result",
    (
        (doc.root_element.xpath('child::comment()'), [doc.root_element[3]]),
        (doc.root_element[0].xpath('text()'), [doc.root_element[0][0]]),
        (doc.root_element.xpath('node()'), doc.root_element.children),
    )
)
def test_type(test, result):
    assert test == result
