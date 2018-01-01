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

def test_namespace_registration():
    Model.register_namespace('scap.model.derp', 'http://jaymes.biz/derp')

    Model.namespace_to_package('http://jaymes.biz/derp') == 'scap.model.derp'

    Model.unregister_namespace('scap.model.derp')

    with pytest.raises(UnregisteredNamespaceException):
        Model.namespace_to_package('http://jaymes.biz/derp')

def test_get_model_namespace():
    assert RootFixture._get_model_namespace() == 'http://jaymes.biz/test'
    assert EnclosedFixture2._get_model_namespace() == 'http://jaymes.biz/test2'

def test_is_nil():
    test_xml = '<test:RootFixture xmlns:test="http://jaymes.biz/test" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:nil="true" />'
    doc = expatriate.Document()
    doc.parse(test_xml)
    model = Model.load(None, doc.root_element)
    assert model.get_value() is None
    assert model.is_nil()

def test_is_not_nil():
    test_xml = '<test:RootFixture xmlns:test="http://jaymes.biz/test" />'
    doc = expatriate.Document()
    doc.parse(test_xml)
    model = Model.load(None, doc.root_element)
    assert not model.is_nil()

def test_package_to_namespace():
    assert Model.package_to_namespace('fixtures.test') == 'http://jaymes.biz/test'
    assert Model.package_to_namespace('fixtures.test2') == 'http://jaymes.biz/test2'

    with pytest.raises(UnregisteredNamespaceException):
        Model.package_to_namespace('scap.model.derp')

def test_namespace_to_package():
    assert Model.namespace_to_package('http://jaymes.biz/test') == 'fixtures.test'
    assert Model.namespace_to_package('http://jaymes.biz/test2') == 'fixtures.test2'

    with pytest.raises(UnregisteredNamespaceException):
        Model.namespace_to_package('http://jaymes.biz/derp')

def test_element_to_class():
    test_xml = '<test:RootFixture xmlns:test="http://jaymes.biz/test" />'
    doc = expatriate.Document()
    doc.parse(test_xml)
    assert Model.element_to_class('fixtures.test', doc.root_element) == RootFixture

def test_get_value():
    test_xml = '<test:RootFixture xmlns:test="http://jaymes.biz/test">test</test:RootFixture>'
    doc = expatriate.Document()
    doc.parse(test_xml)
    model = Model.load(None, doc.root_element)
    assert model.get_value() == 'test'

def test_load_root_model():
    test_xml = '<test:RootFixture xmlns:test="http://jaymes.biz/test" />'
    doc = expatriate.Document()
    doc.parse(test_xml)
    model = Model.load(None, doc.root_element)
    assert isinstance(model, RootFixture)

    with pytest.raises(UnregisteredNamespaceException):
        test_xml = '<test:RootFixture xmlns:test="http://jaymes.biz/derp" />'
        doc = expatriate.Document()
        doc.parse(test_xml)
        model = Model.load(None, doc.root_element)

    with pytest.raises(ElementMappingException):
        test_xml = '<test:Derp xmlns:test="http://jaymes.biz/test" />'
        doc = expatriate.Document()
        doc.parse(test_xml)
        model = Model.load(None, doc.root_element)

def test_load_attribute_required():
    test_xml = '<test:RequiredAttributeFixture xmlns:test="http://jaymes.biz/test" required_attribute="test" />'
    doc = expatriate.Document()
    doc.parse(test_xml)
    model = Model.load(None, doc.root_element)
    assert isinstance(model, RequiredAttributeFixture)
    assert hasattr(model, 'required_attribute')
    assert model.required_attribute == 'test'

    with pytest.raises(RequiredAttributeException):
        test_xml = '<test:RequiredAttributeFixture xmlns:test="http://jaymes.biz/test" />'
        doc = expatriate.Document()
        doc.parse(test_xml)
        model = Model.load(None, doc.root_element)

def test_load_attribute_in():
    test_xml = '<test:AttributeFixture xmlns:test="http://jaymes.biz/test" in_attribute="test" />'
    doc = expatriate.Document()
    doc.parse(test_xml)
    model = Model.load(None, doc.root_element)
    assert isinstance(model, AttributeFixture)
    assert hasattr(model, 'in_test')
    assert model.in_test == 'test'

def test_load_attribute_dash():
    test_xml = '<test:AttributeFixture xmlns:test="http://jaymes.biz/test" dash-attribute="test" />'
    doc = expatriate.Document()
    doc.parse(test_xml)
    model = Model.load(None, doc.root_element)
    assert isinstance(model, AttributeFixture)
    assert hasattr(model, 'dash_attribute')
    assert model.dash_attribute == 'test'

def test_load_attribute_default():
    test_xml = '<test:AttributeFixture xmlns:test="http://jaymes.biz/test" />'
    doc = expatriate.Document()
    doc.parse(test_xml)
    model = Model.load(None, doc.root_element)
    assert isinstance(model, AttributeFixture)
    assert hasattr(model, 'default_attribute')
    assert model.default_attribute == 'test'

def test_load_attribute_no_default():
    test_xml = '<test:AttributeFixture xmlns:test="http://jaymes.biz/test" />'
    doc = expatriate.Document()
    doc.parse(test_xml)
    model = Model.load(None, doc.root_element)
    assert isinstance(model, AttributeFixture)
    assert hasattr(model, 'in_test')
    assert model.in_test is None

def test_load_element_min():
    test_xml = '''
        <test:MinMaxElementFixture xmlns:test="http://jaymes.biz/test">
        <test:min>test1</test:min>
        <test:min>test2</test:min>
        <test:min>test3</test:min>
        <test:max>test4</test:max>
        <test:max>test5</test:max>
        </test:MinMaxElementFixture>
        '''
    doc = expatriate.Document()
    doc.parse(test_xml)
    model = Model.load(None, doc.root_element)
    assert isinstance(model, MinMaxElementFixture)

    assert hasattr(model, 'min')
    assert isinstance(model.min, list)
    assert len(model.min) == 3
    assert model.min[0].get_value() == 'test1'
    assert model.min[1].get_value() == 'test2'
    assert model.min[2].get_value() == 'test3'

    with pytest.raises(MinimumElementException):
        test_xml = '''
            <test:MinMaxElementFixture xmlns:test="http://jaymes.biz/test">
            <test:min>test1</test:min>
            <test:max>test4</test:max>
            <test:max>test5</test:max>
            </test:MinMaxElementFixture>
            '''
        doc = expatriate.Document()
        doc.parse(test_xml)
        model = Model.load(None, doc.root_element)

def test_load_element_max():
    test_xml = '''
        <test:MinMaxElementFixture xmlns:test="http://jaymes.biz/test">
        <test:min>test1</test:min>
        <test:min>test2</test:min>
        <test:min>test3</test:min>
        <test:max>test4</test:max>
        <test:max>test5</test:max>
        </test:MinMaxElementFixture>
        '''
    doc = expatriate.Document()
    doc.parse(test_xml)
    model = Model.load(None, doc.root_element)
    assert isinstance(model, MinMaxElementFixture)

    assert hasattr(model, 'max')
    assert isinstance(model.max, list)
    assert len(model.max) == 2
    assert model.max[0].get_value() == 'test4'
    assert model.max[1].get_value() == 'test5'

    with pytest.raises(MaximumElementException):
        test_xml = '''
            <test:MinMaxElementFixture xmlns:test="http://jaymes.biz/test">
            <test:min>test1</test:min>
            <test:min>test2</test:min>
            <test:min>test3</test:min>
            <test:max>test4</test:max>
            <test:max>test5</test:max>
            <test:max>test6</test:max>
            </test:MinMaxElementFixture>
            '''
        doc = expatriate.Document()
        doc.parse(test_xml)
        model = Model.load(None, doc.root_element)

def test_load_element_wildcard_not_in():
    test_xml = '''
        <test:WildcardElementNotInFixture xmlns:test2="http://jaymes.biz/test2" xmlns:test="http://jaymes.biz/test">
        <test:wildcard_element>test1</test:wildcard_element>
        <test2:wildcard_element>test2</test2:wildcard_element>
        </test:WildcardElementNotInFixture>
        '''
    doc = expatriate.Document()
    doc.parse(test_xml)
    model = Model.load(None, doc.root_element)
    assert isinstance(model, WildcardElementNotInFixture)
    assert hasattr(model, '_elements')
    assert isinstance(model._elements, list)
    assert len(model._elements) == 2
    assert isinstance(model._elements[0], EnclosedFixture)
    assert isinstance(model._elements[1], EnclosedFixture2)
    assert model._elements[0].get_value() == 'test1'
    assert model._elements[1].get_value() == 'test2'

def test_load_element_wildcard_in():
    test_xml = '''
        <test:WildcardElementInFixture xmlns:test2="http://jaymes.biz/test2" xmlns:test="http://jaymes.biz/test">
        <test:wildcard_element>test1</test:wildcard_element>
        <test2:wildcard_element>test2</test2:wildcard_element>
        </test:WildcardElementInFixture>
        '''
    doc = expatriate.Document()
    doc.parse(test_xml)
    model = Model.load(None, doc.root_element)

    assert isinstance(model, WildcardElementInFixture)

    assert hasattr(model, 'test_elements')
    assert isinstance(model.test_elements, list)
    assert len(model.test_elements) == 1

    assert hasattr(model, 'elements')
    assert isinstance(model.elements, list)
    assert len(model.elements) == 1

    assert isinstance(model.test_elements[0], EnclosedFixture)
    assert model.test_elements[0].get_value() == 'test1'

    assert isinstance(model.elements[0], EnclosedFixture2)
    assert model.elements[0].get_value() == 'test2'

def test_load_element_append_nil():
    test_xml = '''
        <test:AppendElementFixture xmlns:test="http://jaymes.biz/test" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
        <test:append_nil xsi:nil="true" />
        <test:append_nil>test2</test:append_nil>
        </test:AppendElementFixture>
        '''
    doc = expatriate.Document()
    doc.parse(test_xml)
    model = Model.load(None, doc.root_element)

    assert isinstance(model, AppendElementFixture)

    assert hasattr(model, 'append_nil')
    assert isinstance(model.append_nil, list)
    assert len(model.append_nil) == 2

    assert model.append_nil[0] is None

    assert isinstance(model.append_nil[1], EnclosedFixture)
    assert model.append_nil[1].get_value() == 'test2'

def test_load_element_append_type():
    test_xml = '''
        <test:AppendElementFixture xmlns:test="http://jaymes.biz/test">
        <test:append_type>1.1</test:append_type>
        <test:append_type>1.2</test:append_type>
        </test:AppendElementFixture>
        '''
    doc = expatriate.Document()
    doc.parse(test_xml)
    model = Model.load(None, doc.root_element)

    assert isinstance(model, AppendElementFixture)

    assert hasattr(model, 'append_type')
    assert isinstance(model.append_type, list)
    assert len(model.append_type) == 2

    assert isinstance(model.append_type[0], float)
    assert model.append_type[0] == 1.1

    assert isinstance(model.append_type[1], float)
    assert model.append_type[1] == 1.2

def test_load_element_append_class():
    test_xml = '''
        <test:AppendElementFixture xmlns:test="http://jaymes.biz/test">
        <test:append_class>test1</test:append_class>
        <test:append_class>test2</test:append_class>
        </test:AppendElementFixture>
        '''
    doc = expatriate.Document()
    doc.parse(test_xml)
    model = Model.load(None, doc.root_element)

    assert isinstance(model, AppendElementFixture)

    assert hasattr(model, 'append_class')
    assert isinstance(model.append_class, list)
    assert len(model.append_class) == 2

    assert isinstance(model.append_class[0], EnclosedFixture)
    assert model.append_class[0].get_value() == 'test1'

    assert isinstance(model.append_class[1], EnclosedFixture)
    assert model.append_class[1].get_value() == 'test2'

def test_load_element_map_key_explicit():
    test_xml = '''
        <test:MapElementFixture xmlns:test="http://jaymes.biz/test" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
        <test:map_explicit_key key="test1">test1</test:map_explicit_key>
        <test:map_explicit_key key="test2">test2</test:map_explicit_key>
        </test:MapElementFixture>
        '''
    doc = expatriate.Document()
    doc.parse(test_xml)
    model = Model.load(None, doc.root_element)

    assert isinstance(model, MapElementFixture)

    assert hasattr(model, 'map_explicit_key')
    assert len(model.map_explicit_key) == 2

    assert 'test1' in model.map_explicit_key
    assert model.map_explicit_key['test1'] == 'test1'

    assert 'test2' in model.map_explicit_key
    assert model.map_explicit_key['test2'] == 'test2'

def test_load_element_map_key_implicit():
    test_xml = '''
        <test:MapElementFixture xmlns:test="http://jaymes.biz/test" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
        <test:map_implicit_key id="test1">test1</test:map_implicit_key>
        <test:map_implicit_key id="test2">test2</test:map_implicit_key>
        </test:MapElementFixture>
        '''
    doc = expatriate.Document()
    doc.parse(test_xml)
    model = Model.load(None, doc.root_element)

    assert isinstance(model, MapElementFixture)

    assert hasattr(model, 'map_implicit_key')
    assert len(model.map_implicit_key) == 2

    assert 'test1' in model.map_implicit_key
    assert model.map_implicit_key['test1'] == 'test1'

    assert 'test2' in model.map_implicit_key
    assert model.map_implicit_key['test2'] == 'test2'

def test_load_element_map_value_nil():
    test_xml = '''
        <test:MapElementFixture xmlns:test="http://jaymes.biz/test" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
        <test:map_value_nil id="test1" xsi:nil="true"/>
        <test:map_value_nil id="test2">test2</test:map_value_nil>
        </test:MapElementFixture>
        '''
    doc = expatriate.Document()
    doc.parse(test_xml)
    model = Model.load(None, doc.root_element)

    assert isinstance(model, MapElementFixture)

    assert hasattr(model, 'map_value_nil')
    assert len(model.map_value_nil) == 2

    assert 'test1' in model.map_value_nil
    assert model.map_value_nil['test1'] == None

    assert 'test2' in model.map_value_nil
    assert model.map_value_nil['test2'] == 'test2'

def test_load_element_map_value_attr():
    test_xml = '''
        <test:MapElementFixture xmlns:test="http://jaymes.biz/test" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
        <test:map_value_attr id="test1" value="test1"/>
        <test:map_value_attr id="test2" value="test2"/>
        </test:MapElementFixture>
        '''
    doc = expatriate.Document()
    doc.parse(test_xml)
    model = Model.load(None, doc.root_element)

    assert isinstance(model, MapElementFixture)

    assert hasattr(model, 'map_value_attr')
    assert len(model.map_value_attr) == 2

    assert 'test1' in model.map_value_attr
    assert model.map_value_attr['test1'] == 'test1'

    assert 'test2' in model.map_value_attr
    assert model.map_value_attr['test2'] == 'test2'

def test_load_element_map_value_type():
    test_xml = '''
        <test:MapElementFixture xmlns:test="http://jaymes.biz/test" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
        <test:map_value_type id="test1">test1</test:map_value_type>
        <test:map_value_type id="test2">test2</test:map_value_type>
        </test:MapElementFixture>
        '''
    doc = expatriate.Document()
    doc.parse(test_xml)
    model = Model.load(None, doc.root_element)

    assert isinstance(model, MapElementFixture)

    assert hasattr(model, 'map_value_type')
    assert len(model.map_value_type) == 2

    assert 'test1' in model.map_value_type
    assert model.map_value_type['test1'] == 'test1'

    assert 'test2' in model.map_value_type
    assert model.map_value_type['test2'] == 'test2'

def test_load_element_map_value_class():
    test_xml = '''
        <test:MapElementFixture xmlns:test="http://jaymes.biz/test" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
        <test:map_value_class id="test1" tag="blue">text1</test:map_value_class>
        <test:map_value_class id="test2" tag="red">text2</test:map_value_class>
        </test:MapElementFixture>
        '''
    doc = expatriate.Document()
    doc.parse(test_xml)
    model = Model.load(None, doc.root_element)

    assert isinstance(model, MapElementFixture)

    assert hasattr(model, 'map_value_class')
    assert len(model.map_value_class) == 2

    assert 'test1' in model.map_value_class
    assert isinstance(model.map_value_class['test1'], MappableElementFixture)
    assert model.map_value_class['test1'].id == 'test1'
    assert model.map_value_class['test1'].tag == 'blue'
    assert model.map_value_class['test1'].get_value() == 'text1'

    assert 'test2' in model.map_value_class
    assert isinstance(model.map_value_class['test2'], MappableElementFixture)
    assert model.map_value_class['test2'].id == 'test2'
    assert model.map_value_class['test2'].tag == 'red'
    assert model.map_value_class['test2'].get_value() == 'text2'

def test_initialization():
    init = InitFixture()

    assert isinstance(init, InitFixture)
    assert hasattr(init, 'attr')
    assert init.attr is None

    assert not hasattr(init, 'in_attr')
    assert hasattr(init, 'test_attr')
    assert init.test_attr is None

    assert hasattr(init, 'dash_attr')
    assert init.dash_attr is None

    assert hasattr(init, 'default_attr')
    assert init.default_attr == 'Default'

    assert hasattr(init, 'list_')
    assert isinstance(init.list_, list)
    assert len(init.list_) == 0

    assert hasattr(init, 'dict_')
    assert isinstance(init.dict_, dict)
    assert len(init.dict_.keys()) == 0

    assert not hasattr(init, 'in_test')
    assert hasattr(init, 'test_in')
    assert init.test_in is None

    assert hasattr(init, 'dash_test')
    assert init.dash_test is None

    assert hasattr(init, 'test2_elements')
    assert isinstance(init.test2_elements, list)
    assert len(init.test2_elements) == 0

    assert hasattr(init, '_elements')
    assert isinstance(init._elements, list)
    assert len(init._elements) == 0

def test_get_package():
    root = RootFixture()
    assert root.get_package() == 'fixtures.test'

def test_str_id_func():
    root = RootFixture()
    assert str(root) == ('RootFixture # ' + str(id(root)))

def test_str_id():
    root = RootFixture()
    root.id = 'test'
    assert str(root) == ('RootFixture id: test')

def test_str_Id():
    root = RootFixture()
    root.Id = 'test'
    assert str(root) == ('RootFixture Id: test')

def test_str_name():
    root = RootFixture()
    root.name = 'test'
    assert str(root) == ('RootFixture name: test')
#
# def test_references():
#     root = RootFixture()
#     enc = EnclosedFixture()
#     enc._parent = root
#     enc.id = 'reftest1'
#     assert root.find_reference('reftest1') == enc
#
#     with pytest.raises(ReferenceException):
#         root.find_reference('test1')
#
# def test_tag_name():
#     root = RootFixture()
#     assert root.tag_name == 'RootFixture'
#
# def test_xmlns():
#     root = RootFixture()
#     assert root.xmlns == 'http://jaymes.biz/test'
#
# # NOTE: from_xml is tested via Model.load
#
# def test_to_xml_root_enclosed():
#     el = RootFixture()
#     el.EnclosedFixture = EnclosedFixture(tag_name='EnclosedFixture')
#     assert el.to_xml() == \
#         b'<test:RootFixture xmlns:test="http://jaymes.biz/test"><test:EnclosedFixture /></test:RootFixture>'
#
# def test_to_xml_required_attribute():
#     el = RequiredAttributeFixture()
#     with pytest.raises(RequiredAttributeException):
#         el.to_xml()
#     el.required_attribute = 'test'
#     assert el.to_xml() == \
#         b'<test:RequiredAttributeFixture xmlns:test="http://jaymes.biz/test" required_attribute="test" />'
#
# def test_to_xml_attributes():
#     el = AttributeFixture()
#     el.in_test = 'test'
#     el.dash_attribute = 'test'
#     el.default_attribute = 'not default'
#
#     xml = el.to_xml()
#     assert xml.startswith(b'<test:AttributeFixture xmlns:test="http://jaymes.biz/test"')
#     assert b'dash-attribute="test" ' in xml
#     assert b'default_attribute="not default" ' in xml
#     assert b'in_attribute="test" ' in xml
#
#     el.in_test = None
#     xml = el.to_xml()
#     assert b'in_attribute=' not in xml
#
#     el.default_attribute = 'test'
#     xml = el.to_xml()
#     assert b'default_attribute="test" ' not in xml
#
# def test_to_xml_min_max():
#     el = MinMaxElementFixture()
#     for i in range(0, 3):
#         el.min.append(EnclosedFixture(tag_name='min'))
#     for i in range(0, 2):
#         el.max.append(EnclosedFixture(tag_name='max'))
#
#     xml = el.to_xml()
#     assert xml.startswith(b'<test:MinMaxElementFixture xmlns:test="http://jaymes.biz/test"')
#     assert xml.count(b'<test:min') == 3
#     assert xml.count(b'<test:max') == 2
#
#     del el.min[0]
#     with pytest.raises(MinimumElementException):
#         el.to_xml()
#
#     el.min.append(EnclosedFixture())
#     el.max.append(EnclosedFixture())
#     with pytest.raises(MaximumElementException):
#         el.to_xml()
#
# def test_to_xml_wildcard_not_in():
#     el = WildcardElementNotInFixture()
#     el._elements.append(EnclosedFixture(tag_name='wildcard_element'))
#     el._elements.append(EnclosedFixture2(tag_name='wildcard_element'))
#
#     xml = el.to_xml()
#     assert xml.startswith(b'<test:WildcardElementNotInFixture')
#     assert b'xmlns:test="http://jaymes.biz/test"' in xml
#     assert b'xmlns:test2="http://jaymes.biz/test2"' in xml
#     assert b'<test:wildcard_element' in xml
#     assert b'<test2:wildcard_element' in xml
#
# def test_to_xml_wildcard_in():
#     el = WildcardElementInFixture()
#     el.test_elements.append(EnclosedFixture(tag_name='wildcard_element'))
#     el.elements.append(EnclosedFixture2(tag_name='wildcard_element'))
#
#     xml = el.to_xml()
#     assert xml.startswith(b'<test:WildcardElementInFixture')
#     assert b'xmlns:test="http://jaymes.biz/test"' in xml
#     assert b'xmlns:test2="http://jaymes.biz/test2"' in xml
#     assert b'<test:wildcard_element' in xml
#     assert b'<test2:wildcard_element' in xml
#
# def test_to_xml_append_nil():
#     el = AppendElementFixture()
#     el.append_nil.append(None)
#     el.append_nil.append(EnclosedFixture(value='test', tag_name='append_nil'))
#
#     xml = el.to_xml()
#     assert xml.startswith(b'<test:AppendElementFixture')
#     assert b'xmlns:test="http://jaymes.biz/test"' in xml
#     assert b'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"' in xml
#     assert b'<test:append_nil xsi:nil="true" />' in xml
#     assert b'<test:append_nil>test</test:append_nil>' in xml
#
# def test_to_xml_append_type():
#     el = AppendElementFixture()
#     el.append_type.append(1.1)
#     el.append_type.append(1.2)
#
#     xml = el.to_xml()
#     assert xml.startswith(b'<test:AppendElementFixture')
#     assert b'xmlns:test="http://jaymes.biz/test"' in xml
#     assert b'<test:append_type>1.1</test:append_type>' in xml
#     assert b'<test:append_type>1.2</test:append_type>' in xml
#
# def test_to_xml_append_class():
#     el = AppendElementFixture()
#     el.append_class.append(EnclosedFixture(value='test1', tag_name='append_class'))
#     el.append_class.append(EnclosedFixture(value='test2', tag_name='append_class'))
#
#     xml = el.to_xml()
#     assert xml.startswith(b'<test:AppendElementFixture')
#     assert b'xmlns:test="http://jaymes.biz/test"' in xml
#     assert b'<test:append_class>test1</test:append_class>' in xml
#     assert b'<test:append_class>test2</test:append_class>' in xml
#
# def test_to_xml_map_key_explicit():
#     el = MapElementFixture()
#     el.map_explicit_key['test1'] = 'test1'
#     el.map_explicit_key['test2'] = 'test2'
#
#     xml = el.to_xml()
#     assert xml.startswith(b'<test:MapElementFixture')
#     assert b'xmlns:test="http://jaymes.biz/test"' in xml
#     assert b'<test:map_explicit_key key="test1">test1</test:map_explicit_key>' in xml
#     assert b'<test:map_explicit_key key="test2">test2</test:map_explicit_key>' in xml
#
# def test_to_xml_map_key_implicit():
#     el = MapElementFixture()
#     el.map_implicit_key['test1'] = 'test1'
#     el.map_implicit_key['test2'] = 'test2'
#
#     xml = el.to_xml()
#     assert xml.startswith(b'<test:MapElementFixture')
#     assert b'xmlns:test="http://jaymes.biz/test"' in xml
#     assert b'<test:map_implicit_key id="test1">test1</test:map_implicit_key>' in xml
#     assert b'<test:map_implicit_key id="test2">test2</test:map_implicit_key>' in xml
#
# def test_to_xml_map_value_nil():
#     el = MapElementFixture()
#     el.map_value_nil['test1'] = None
#     el.map_value_nil['test2'] = 'test2'
#
#     xml = el.to_xml()
#     assert xml.startswith(b'<test:MapElementFixture')
#     assert b'xmlns:test="http://jaymes.biz/test"' in xml
#     assert b'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"' in xml
#     assert b'<test:map_value_nil id="test1" xsi:nil="true" />' in xml
#     assert b'<test:map_value_nil id="test2">test2</test:map_value_nil>' in xml
#
# def test_to_xml_map_value_attr():
#     el = MapElementFixture()
#     el.map_value_attr['test1'] = 'test1'
#     el.map_value_attr['test2'] = 'test2'
#
#     xml = el.to_xml()
#     assert xml.startswith(b'<test:MapElementFixture')
#     assert b'xmlns:test="http://jaymes.biz/test"' in xml
#     assert b'<test:map_value_attr id="test1" value="test1" />' in xml
#     assert b'<test:map_value_attr id="test2" value="test2" />' in xml
#
# def test_to_xml_map_value_type():
#     el = MapElementFixture()
#     el.map_value_type['test1'] = 'test1'
#     el.map_value_type['test2'] = 'test2'
#
#     xml = el.to_xml()
#     assert xml.startswith(b'<test:MapElementFixture')
#     assert b'xmlns:test="http://jaymes.biz/test"' in xml
#     assert b'<test:map_value_type id="test1">test1</test:map_value_type>' in xml
#     assert b'<test:map_value_type id="test2">test2</test:map_value_type>' in xml
#
# def test_to_xml_map_value_class():
#     el = MapElementFixture()
#     el.map_value_class['test1'] = MappableElementFixture(value='text1', tag_name='map_value_class')
#     el.map_value_class['test1'].tag = 'blue'
#     el.map_value_class['test2'] = MappableElementFixture(value='text2', tag_name='map_value_class')
#     el.map_value_class['test2'].tag = 'red'
#
#     xml = el.to_xml()
#     assert xml.startswith(b'<test:MapElementFixture')
#     assert b'xmlns:test="http://jaymes.biz/test"' in xml
#     assert b'<test:map_value_class id="test1" tag="blue">text1</test:map_value_class>' in xml
#     assert b'<test:map_value_class id="test2" tag="red">text2</test:map_value_class>' in xml
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
#     out_xml = model.to_xml()
#     print(test_xml)
#     print(out_xml)
#     assert out_xml == test_xml
#
# def test_load_attribute_value_in_enum():
#     test_xml = '<test:RootFixture xmlns:test="http://jaymes.biz/test"><test:EnumValue>bravo</test:EnumValue></test:RootFixture>'
#     doc = expatriate.Document()
#     doc.parse(test_xml)
#     model = Model.load(None, doc.root_element)
#     assert isinstance(model, RootFixture)
#     assert hasattr(model, 'EnumValue')
#     assert model.EnumValue.get_value() == 'bravo'
#
# def test_load_attribute_value_not_in_enum():
#     with pytest.raises(ValueError):
#         test_xml = '<test:RootFixture xmlns:test="http://jaymes.biz/test"><test:EnumValue>delta</test:EnumValue></test:RootFixture>'
#         doc = expatriate.Document()
#         doc.parse(test_xml)
#         model = Model.load(None, doc.root_element)
#
# def test_load_attribute_value_matches_pattern():
#     test_xml = '<test:RootFixture xmlns:test="http://jaymes.biz/test"><test:PatternValue>Bravo12</test:PatternValue></test:RootFixture>'
#     doc = expatriate.Document()
#     doc.parse(test_xml)
#     model = Model.load(None, doc.root_element)
#     assert isinstance(model, RootFixture)
#     assert hasattr(model, 'PatternValue')
#     assert model.PatternValue.get_value() == 'Bravo12'
#
# def test_load_attribute_value_not_matches_pattern():
#     with pytest.raises(ValueError):
#         test_xml = '<test:RootFixture xmlns:test="http://jaymes.biz/test"><test:PatternValue>delta</test:PatternValue></test:RootFixture>'
#         doc = expatriate.Document()
#         doc.parse(test_xml)
#         model = Model.load(None, doc.root_element)
