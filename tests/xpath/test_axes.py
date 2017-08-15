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
<root xmlns="http://jaymes.biz">
    <para name="element1">
        text node
    </para>
    <para name="element2"/>
    <para name="element3">
        <para name="element3_1">
            <para name="kal-el">
                Superman's dad
            </para>
        </para>
        <para name="element3_2"/>
    </para>
</root>
''')

def test_child():
    assert doc.xpath('child::*') == doc.children

def test_descendant():
    ns = [
        doc.root_element[0],
        doc.root_element[1],
        doc.root_element[2],
        doc.root_element[2][0],
        doc.root_element[2][0][0],
        doc.root_element[2][1],
    ]

    test = doc.root_element.xpath('descendant::*')
    assert test == ns

def test_descendant_or_self():
    ns = [
        doc.root_element,
        doc.root_element[0],
        doc.root_element[1],
        doc.root_element[2],
        doc.root_element[2][0],
        doc.root_element[2][0][0],
        doc.root_element[2][1],
    ]

    test = doc.root_element.xpath('descendant-or-self::*')
    assert test == ns

def test_parent():
    assert doc.root_element[0].xpath('parent::*') == [doc.root_element]

def test_ancestor():
    ns = [
        doc.root_element[2][0],
        doc.root_element[2],
        doc.root_element,
    ]
    assert doc.root_element[2][0][0].xpath('ancestor::*') == ns

def test_ancestor_or_self():
    ns = [
        doc.root_element[2][0][0],
        doc.root_element[2][0],
        doc.root_element[2],
        doc.root_element,
    ]
    assert doc.root_element[2][0][0].xpath('ancestor-or-self::*') == ns

def test_following_sibling():
    assert doc.root_element[0].xpath('following-sibling::*') == [
        doc.root_element[1],
        doc.root_element[2],
    ]

def test_preceding_sibling():
    assert doc.root_element[2].xpath('preceding-sibling::*') == [
        doc.root_element[1],
        doc.root_element[0],
    ]

def test_following():
    assert doc.root_element[2][0][0].xpath('following::*') == [
        doc.root_element[2][1],
    ]

def test_preceding():
    assert doc.root_element[2][0][0].xpath('preceding::*') == [
        doc.root_element[2][0],
        doc.root_element[2],
        doc.root_element[1],
        doc.root_element[0],
        doc.root_element,
    ]

def test_attribute():
    assert doc.root_element[0].xpath('attribute::*') == [doc.root_element[0].attribute_nodes['name']]

def test_namespace():
    ns = doc.root_element[0].xpath('namespace::*')
    assert doc.root_element[0].namespace_nodes[None] in ns
    assert doc.root_element[0].namespace_nodes['xml'] in ns

def test_self():
    assert doc.root_element.xpath('self::*') == [doc.root_element]

def test_unknown():
    with pytest.raises(XPathSyntaxException):
        doc.root_element.xpath('unknown::*')

# NOTE: The ancestor, descendant, following, preceding and self axes partition a
# document (ignoring attribute and namespace nodes): they do not overlap and
# together they contain all the nodes in the document.
