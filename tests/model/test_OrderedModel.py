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

import pytest
import logging
import expatriate
import types
import sys

from expatriate.model.decorators import *
from expatriate.model.exceptions import *
from expatriate.model.types import *
from expatriate.model import Model

from fixtures.test.RootFixture import RootFixture
from fixtures.test.EnclosedFixture import EnclosedFixture
from fixtures.test.AttributeFixture import AttributeFixture
from fixtures.test.RequiredAttributeFixture import RequiredAttributeFixture
from fixtures.test.WildcardElementNotInFixture import WildcardElementNotInFixture
from fixtures.test.WildcardElementInFixture import WildcardElementInFixture
from fixtures.test.AppendElementFixture import AppendElementFixture
from fixtures.test.MapElementFixture import MapElementFixture
from fixtures.test.MappableElementFixture import MappableElementFixture
from fixtures.test.InitFixture import InitFixture
from fixtures.test.MinMaxElementFixture import MinMaxElementFixture
from fixtures.test.InheritingFixture import InheritingFixture

from fixtures.test2.EnclosedFixture import EnclosedFixture as EnclosedFixture2

logging.basicConfig(level=logging.DEBUG)

Model.register_namespace('fixtures.test', 'http://jaymes.biz/test')
Model.register_namespace('fixtures.test2', 'http://jaymes.biz/test2')

#
# def test_in_and_out():
#     test_xml = b'<test:InitFixture xmlns:test="http://jaymes.biz/test" xmlns:test2="http://jaymes.biz/test2">' + \
#         b'<test:list id="test1" />' + \
#         b'<test:list id="test2" />' + \
#         b'<test:list id="test3" />' + \
#         b'<test:dict id="test4" />' + \
#         b'<test:dict id="test5" />' + \
#         b'<test:dict id="test6" />' + \
#         b'<test:dict id="test7" />' + \
#         b'<test:dict id="test8" />' + \
#         b'<test:in_test id="test9" />' + \
#         b'<test:dash-test id="test10" />' + \
#         b'<test2:wildcard_element id="test11" />' + \
#         b'<test:wildcard_element id="test12" />' + \
#         b'<test:dict id="test13" />' + \
#         b'<test:list id="test14" />' + \
#         b'</test:InitFixture>'
#     doc = expatriate.Document()
#     doc.parse(test_xml)
#     model = Model.load(None, doc.root_element)
#
#     out_xml = model.produce()
#     print(test_xml)
#     print(out_xml)
#     assert out_xml == test_xml
