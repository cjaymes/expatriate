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

def test_len():
    doc = Document()
    doc.parse('''<Root><Element/><Element/><Element/></Root>''')
    assert len(doc.root_element) == 3

def test_getitem():
    doc = Document()
    doc.parse('''<Root><Element name="a"/><Element name="b"/><Element name="c"/></Root>''')
    assert doc.root_element[1].attributes['name'] == 'b'

def test_setitem():
    doc = Document()
    doc.parse('''<Root><Element name="a"/><Element name="b"/><Element name="c"/></Root>''')
    doc.root_element[1] = doc.root_element.spawn_element('Element', {'name': 'bravo'})
    assert doc.root_element[1].attributes['name'] == 'bravo'

def test_delitem():
    doc = Document()
    doc.parse('''<Root><Element name="a"/><Element name="b"/><Element name="c"/></Root>''')
    del doc.root_element[1]
    assert doc.root_element[1].attributes['name'] == 'c'

def test_iter():
    doc = Document()
    doc.parse('''<Root><Element name="a"/><Element name="b"/><Element name="c"/></Root>''')
    names = ['a', 'b', 'c']
    i = 0
    for e in iter(doc.root_element):
        assert e.attributes['name'] == names[i]
        i += 1

def test_append_str():
    doc = Document()
    doc.parse('''<Root><Element name="a"/><Element name="b"/><Element name="c"/></Root>''')
    doc.root_element.append('delta')
    assert doc.root_element[3] == 'delta'

def test_append_int():
    doc = Document()
    doc.parse('''<Root><Element name="a"/><Element name="b"/><Element name="c"/></Root>''')
    doc.root_element.append(42)
    assert doc.root_element[3] == '42'

def test_append_float():
    doc = Document()
    doc.parse('''<Root><Element name="a"/><Element name="b"/><Element name="c"/></Root>''')
    doc.root_element.append(42.42)
    assert doc.root_element[3] == '42.42'

def test_append_el():
    doc = Document()
    doc.parse('''<Root><Element name="a"/><Element name="b"/><Element name="c"/></Root>''')
    doc.root_element.append(doc.root_element.spawn_element('Element', {'name': 'delta'}))
    assert doc.root_element[3].attributes['name'] == 'delta'

def test_spawn_char():
    doc = Document()
    doc.parse('''<Root><Element name="a"/><Element name="b"/><Element name="c"/></Root>''')
    n = doc.root_element.spawn_character_data('lorem ipsum')
    assert isinstance(n, CharacterData)
    assert n.data == 'lorem ipsum'

def test_spawn_comment():
    doc = Document()
    doc.parse('''<Root><Element name="a"/><Element name="b"/><Element name="c"/></Root>''')
    n = doc.root_element.spawn_comment('off-hand comment')
    assert isinstance(n, Comment)
    assert n.data == 'off-hand comment'

def test_spawn_el():
    doc = Document()
    doc.parse('''<Root><Element name="a"/><Element name="b"/><Element name="c"/></Root>''')
    n = doc.root_element.spawn_element('Element', {'name': 'delta'})
    assert isinstance(n, Element)
    assert n.name == 'Element'
    assert 'name' in n.attributes
    assert n.attributes['name'] == 'delta'

def test_spawn_pi():
    doc = Document()
    doc.parse('''<Root><Element name="a"/><Element name="b"/><Element name="c"/></Root>''')
    n = doc.root_element.spawn_processing_instruction('amidships', 'big guns')
    assert isinstance(n, ProcessingInstruction)
    assert n.target == 'amidships'
    assert n.data == 'big guns'

# TODO count, index, extend, insert, pop, remove, reverse, sort
