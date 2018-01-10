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

def test_no_parent():
    el = Element('test', attributes={})
    assert isinstance(el, Element)
    assert el.local_name == 'test'
    assert el.name == 'test'
    assert el.namespace is None
    assert el.prefix is None
    assert el.attributes == {}
    assert el.parent is None

def test_produce_no_ns_no_prefix():
    el = Element('test')
    assert el.produce() == '<test/>'

def test_produce_ns_no_prefix():
    el = Element('test', namespace='http://jaymes.biz/test')
    assert el.produce() == '<test xmlns="http://jaymes.biz/test"/>'

def test_produce_ns_prefix():
    el = Element('test', namespace='http://jaymes.biz/test', prefix='test')
    assert el.produce() == '<test:test xmlns:test="http://jaymes.biz/test"/>'

def test_get_type():
    n = Element('test')
    assert n.get_type() == 'element'
