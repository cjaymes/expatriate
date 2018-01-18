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
import sys
import types

import expatriate
import pytest
from expatriate.exceptions import *
from expatriate.model import *
from fixtures.test2.EnclosedFixture import EnclosedFixture as EnclosedFixture2
from fixtures.test.AttributeFixture import AttributeFixture
from fixtures.test.DictElementFixture import DictElementFixture
from fixtures.test.DictValueElementFixture import DictValueElementFixture
from fixtures.test.EnclosedFixture import EnclosedFixture
from fixtures.test.InheritingFixture import InheritingFixture
from fixtures.test.InitFixture import InitFixture
from fixtures.test.ListElementFixture import ListElementFixture
from fixtures.test.MinMaxElementFixture import MinMaxElementFixture
from fixtures.test.RequiredAttributeFixture import RequiredAttributeFixture
from fixtures.test.RootFixture import RootFixture
from fixtures.test.WildcardElementInFixture import WildcardElementInFixture
from fixtures.test.WildcardElementNotInFixture import \
    WildcardElementNotInFixture

logging.basicConfig(level=logging.DEBUG)

Model.register_namespace('fixtures.test', 'http://jaymes.biz/test', 'test')
Model.register_namespace('fixtures.test2', 'http://jaymes.biz/test2', 'test2')

def test_namespace_registration():
    Model.register_namespace('scap.model.derp', 'http://jaymes.biz/derp', 'derp')

    Model.namespace_to_package('http://jaymes.biz/derp') == 'scap.model.derp'

    Model.unregister_namespace('scap.model.derp')

    with pytest.raises(UnknownNamespaceException):
        Model.namespace_to_package('http://jaymes.biz/derp')

def test_is_nil():
    test_xml = '<test:RootFixture xmlns:test="http://jaymes.biz/test" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:nil="true"/>'
    doc = expatriate.Document()
    doc.parse(test_xml)
    model = Model.load(None, doc.root_element)
    assert model.get_value() is None
    assert model.is_nil()

def test_is_not_nil():
    test_xml = '<test:RootFixture xmlns:test="http://jaymes.biz/test"/>'
    doc = expatriate.Document()
    doc.parse(test_xml)
    model = Model.load(None, doc.root_element)
    assert not model.is_nil()

def test_package_to_namespace():
    assert Model.package_to_namespace('fixtures.test') == 'http://jaymes.biz/test'
    assert Model.package_to_namespace('fixtures.test2') == 'http://jaymes.biz/test2'

    with pytest.raises(UnknownNamespaceException):
        Model.package_to_namespace('scap.model.derp')

def test_namespace_to_package():
    assert Model.namespace_to_package('http://jaymes.biz/test') == 'fixtures.test'
    assert Model.namespace_to_package('http://jaymes.biz/test2') == 'fixtures.test2'

    with pytest.raises(UnknownNamespaceException):
        Model.namespace_to_package('http://jaymes.biz/derp')

#TODO test_namespace_to_prefix

def test_class_for_element():
    test_xml = '<test:RootFixture xmlns:test="http://jaymes.biz/test"/>'
    doc = expatriate.Document()
    doc.parse(test_xml)
    assert Model.class_for_element(doc.root_element) == RootFixture

def test_get_value():
    test_xml = '<test:RootFixture xmlns:test="http://jaymes.biz/test">test</test:RootFixture>'
    doc = expatriate.Document()
    doc.parse(test_xml)
    model = Model.load(None, doc.root_element)
    assert model.get_value() == 'test'

def test_load_root_model():
    test_xml = '<test:RootFixture xmlns:test="http://jaymes.biz/test"/>'
    doc = expatriate.Document()
    doc.parse(test_xml)
    model = Model.load(None, doc.root_element)
    assert isinstance(model, RootFixture)

    with pytest.raises(UnknownNamespaceException):
        test_xml = '<test:RootFixture xmlns:test="http://jaymes.biz/derp"/>'
        doc = expatriate.Document()
        doc.parse(test_xml)
        model = Model.load(None, doc.root_element)

    with pytest.raises(ElementMappingException):
        test_xml = '<test:Derp xmlns:test="http://jaymes.biz/test"/>'
        doc = expatriate.Document()
        doc.parse(test_xml)
        model = Model.load(None, doc.root_element)

def test_load_attribute_required():
    test_xml = '<test:RequiredAttributeFixture xmlns:test="http://jaymes.biz/test" required_attribute="test"/>'
    doc = expatriate.Document()
    doc.parse(test_xml)
    model = Model.load(None, doc.root_element)
    assert isinstance(model, RequiredAttributeFixture)
    assert hasattr(model, 'required_attribute')
    assert model.required_attribute == 'test'

    with pytest.raises(RequiredAttributeException):
        test_xml = '<test:RequiredAttributeFixture xmlns:test="http://jaymes.biz/test"/>'
        doc = expatriate.Document()
        doc.parse(test_xml)
        model = Model.load(None, doc.root_element)

def test_load_attribute_in():
    test_xml = '<test:AttributeFixture xmlns:test="http://jaymes.biz/test" in_attribute="test"/>'
    doc = expatriate.Document()
    doc.parse(test_xml)
    model = Model.load(None, doc.root_element)
    assert isinstance(model, AttributeFixture)
    assert hasattr(model, 'in_test')
    assert model.in_test == 'test'

def test_load_attribute_dash():
    test_xml = '<test:AttributeFixture xmlns:test="http://jaymes.biz/test" dash-attribute="test"/>'
    doc = expatriate.Document()
    doc.parse(test_xml)
    model = Model.load(None, doc.root_element)
    assert isinstance(model, AttributeFixture)
    assert hasattr(model, 'dash_attribute')
    assert model.dash_attribute == 'test'

def test_load_attribute_default():
    test_xml = '<test:AttributeFixture xmlns:test="http://jaymes.biz/test"/>'
    doc = expatriate.Document()
    doc.parse(test_xml)
    model = Model.load(None, doc.root_element)
    assert isinstance(model, AttributeFixture)
    assert hasattr(model, 'default_attribute')
    assert model.default_attribute == 'test'

def test_load_attribute_no_default():
    test_xml = '<test:AttributeFixture xmlns:test="http://jaymes.biz/test"/>'
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

def test_load_element_list_nil():
    test_xml = '''
        <test:ListElementFixture xmlns:test="http://jaymes.biz/test" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
        <test:list_nil xsi:nil="true"/>
        <test:list_nil>test2</test:list_nil>
        </test:ListElementFixture>
        '''
    doc = expatriate.Document()
    doc.parse(test_xml)
    model = Model.load(None, doc.root_element)

    assert isinstance(model, ListElementFixture)

    assert hasattr(model, 'list_nil')
    assert isinstance(model.list_nil, list)
    assert len(model.list_nil) == 2

    assert model.list_nil[0] is None

    assert isinstance(model.list_nil[1], EnclosedFixture)
    assert model.list_nil[1].get_value() == 'test2'

def test_load_element_list_type():
    test_xml = '''
        <test:ListElementFixture xmlns:test="http://jaymes.biz/test">
        <test:list_type>1.1</test:list_type>
        <test:list_type>1.2</test:list_type>
        </test:ListElementFixture>
        '''
    doc = expatriate.Document()
    doc.parse(test_xml)
    model = Model.load(None, doc.root_element)

    assert isinstance(model, ListElementFixture)

    assert hasattr(model, 'list_type')
    assert isinstance(model.list_type, list)
    assert len(model.list_type) == 2

    assert isinstance(model.list_type[0], float)
    assert model.list_type[0] == 1.1

    assert isinstance(model.list_type[1], float)
    assert model.list_type[1] == 1.2

def test_load_element_list_class():
    test_xml = '''
        <test:ListElementFixture xmlns:test="http://jaymes.biz/test">
        <test:list_class>test1</test:list_class>
        <test:list_class>test2</test:list_class>
        </test:ListElementFixture>
        '''
    doc = expatriate.Document()
    doc.parse(test_xml)
    model = Model.load(None, doc.root_element)

    assert isinstance(model, ListElementFixture)

    assert hasattr(model, 'list_class')
    assert isinstance(model.list_class, list)
    assert len(model.list_class) == 2

    assert isinstance(model.list_class[0], EnclosedFixture)
    assert model.list_class[0].get_value() == 'test1'

    assert isinstance(model.list_class[1], EnclosedFixture)
    assert model.list_class[1].get_value() == 'test2'

def test_load_element_dict_key_explicit():
    test_xml = '''
        <test:DictElementFixture xmlns:test="http://jaymes.biz/test" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
        <test:dict_explicit_key key="test1">test1</test:dict_explicit_key>
        <test:dict_explicit_key key="test2">test2</test:dict_explicit_key>
        </test:DictElementFixture>
        '''
    doc = expatriate.Document()
    doc.parse(test_xml)
    model = Model.load(None, doc.root_element)

    assert isinstance(model, DictElementFixture)

    assert hasattr(model, 'dict_explicit_key')
    assert len(model.dict_explicit_key) == 2

    assert 'test1' in model.dict_explicit_key
    assert model.dict_explicit_key['test1'] == 'test1'

    assert 'test2' in model.dict_explicit_key
    assert model.dict_explicit_key['test2'] == 'test2'

def test_load_element_dict_key_implicit():
    test_xml = '''
        <test:DictElementFixture xmlns:test="http://jaymes.biz/test" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
        <test:dict_implicit_key id="test1">test1</test:dict_implicit_key>
        <test:dict_implicit_key id="test2">test2</test:dict_implicit_key>
        </test:DictElementFixture>
        '''
    doc = expatriate.Document()
    doc.parse(test_xml)
    model = Model.load(None, doc.root_element)

    assert isinstance(model, DictElementFixture)

    assert hasattr(model, 'dict_implicit_key')
    assert len(model.dict_implicit_key) == 2

    assert 'test1' in model.dict_implicit_key
    assert model.dict_implicit_key['test1'] == 'test1'

    assert 'test2' in model.dict_implicit_key
    assert model.dict_implicit_key['test2'] == 'test2'

def test_load_element_dict_value_nil():
    test_xml = '''
        <test:DictElementFixture xmlns:test="http://jaymes.biz/test" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
        <test:dict_value_nil id="test1" xsi:nil="true"/>
        <test:dict_value_nil id="test2">test2</test:dict_value_nil>
        </test:DictElementFixture>
        '''
    doc = expatriate.Document()
    doc.parse(test_xml)
    model = Model.load(None, doc.root_element)

    assert isinstance(model, DictElementFixture)

    assert hasattr(model, 'dict_value_nil')
    assert len(model.dict_value_nil) == 2

    assert 'test1' in model.dict_value_nil
    assert model.dict_value_nil['test1'] == None

    assert 'test2' in model.dict_value_nil
    assert model.dict_value_nil['test2'] == 'test2'

def test_load_element_dict_value_attr():
    test_xml = '''
        <test:DictElementFixture xmlns:test="http://jaymes.biz/test" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
        <test:dict_value_attr id="test1" value="test1"/>
        <test:dict_value_attr id="test2" value="test2"/>
        </test:DictElementFixture>
        '''
    doc = expatriate.Document()
    doc.parse(test_xml)
    model = Model.load(None, doc.root_element)

    assert isinstance(model, DictElementFixture)

    assert hasattr(model, 'dict_value_attr')
    assert len(model.dict_value_attr) == 2

    assert 'test1' in model.dict_value_attr
    assert model.dict_value_attr['test1'] == 'test1'

    assert 'test2' in model.dict_value_attr
    assert model.dict_value_attr['test2'] == 'test2'

def test_load_element_dict_value_type():
    test_xml = '''
        <test:DictElementFixture xmlns:test="http://jaymes.biz/test" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
        <test:dict_value_type id="test1">test1</test:dict_value_type>
        <test:dict_value_type id="test2">test2</test:dict_value_type>
        </test:DictElementFixture>
        '''
    doc = expatriate.Document()
    doc.parse(test_xml)
    model = Model.load(None, doc.root_element)

    assert isinstance(model, DictElementFixture)

    assert hasattr(model, 'dict_value_type')
    assert len(model.dict_value_type) == 2

    assert 'test1' in model.dict_value_type
    assert model.dict_value_type['test1'] == 'test1'

    assert 'test2' in model.dict_value_type
    assert model.dict_value_type['test2'] == 'test2'

def test_load_element_dict_value_class():
    test_xml = '''
        <test:DictElementFixture xmlns:test="http://jaymes.biz/test" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
        <test:dict_value_class id="test1" tag="blue">text1</test:dict_value_class>
        <test:dict_value_class id="test2" tag="red">text2</test:dict_value_class>
        </test:DictElementFixture>
        '''
    doc = expatriate.Document()
    doc.parse(test_xml)
    model = Model.load(None, doc.root_element)

    assert isinstance(model, DictElementFixture)

    assert hasattr(model, 'dict_value_class')
    assert len(model.dict_value_class) == 2

    assert 'test1' in model.dict_value_class
    assert isinstance(model.dict_value_class['test1'], DictValueElementFixture)
    assert model.dict_value_class['test1'].id == 'test1'
    assert model.dict_value_class['test1'].tag == 'blue'
    assert model.dict_value_class['test1'].get_value() == 'text1'

    assert 'test2' in model.dict_value_class
    assert isinstance(model.dict_value_class['test2'], DictValueElementFixture)
    assert model.dict_value_class['test2'].id == 'test2'
    assert model.dict_value_class['test2'].tag == 'red'
    assert model.dict_value_class['test2'].get_value() == 'text2'

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

def test_references():
    root = RootFixture()
    #TODO need to add to a attr mapper knows about
    enc = EnclosedFixture()
    enc.id = 'reftest1'
    root.EnclosedFixture = enc
    assert root.find_reference('reftest1') == enc

    with pytest.raises(ReferenceException):
        root.find_reference('test1')

def test_produce_root_enclosed():
    model = RootFixture(local_name='RootFixture', namespace='http://jaymes.biz/test', prefix='test')
    model.EnclosedFixture = EnclosedFixture(local_name='EnclosedFixture')
    assert model.produce().produce() == \
        '<test:RootFixture xmlns:test="http://jaymes.biz/test"><test:EnclosedFixture/></test:RootFixture>'

def test_produce_required_attribute():
    model = RequiredAttributeFixture(local_name='RequiredAttributeFixture', namespace='http://jaymes.biz/test', prefix='test')
    with pytest.raises(RequiredAttributeException):
        model.produce()
    model.required_attribute = 'test'
    assert model.produce().produce() == \
        '<test:RequiredAttributeFixture xmlns:test="http://jaymes.biz/test" required_attribute="test"/>'

def test_produce_attributes():
    model = AttributeFixture(local_name='AttributeFixture', namespace='http://jaymes.biz/test', prefix='test')
    model.in_test = 'test'
    model.dash_attribute = 'test'
    model.default_attribute = 'not default'

    xml = model.produce().produce()
    assert xml.startswith('<test:AttributeFixture xmlns:test="http://jaymes.biz/test"')
    assert 'dash-attribute="test"' in xml
    assert 'default_attribute="not default"' in xml
    assert 'in_attribute="test"' in xml

    model.in_test = None
    xml = model.produce()
    assert 'in_attribute=' not in xml

    model.default_attribute = 'test'
    xml = model.produce()
    assert 'default_attribute="test" ' not in xml

def test_produce_min_max():
    model = MinMaxElementFixture(local_name='MinMaxElementFixture', namespace='http://jaymes.biz/test', prefix='test')
    for i in range(0, 3):
        model.min.append(EnclosedFixture(local_name='min'))
    for i in range(0, 2):
        model.max.append(EnclosedFixture(local_name='max'))

    xml = model.produce().produce()
    assert xml.startswith('<test:MinMaxElementFixture xmlns:test="http://jaymes.biz/test"')
    assert xml.count('<test:min') == 3
    assert xml.count('<test:max') == 2

    del model.min[0]
    with pytest.raises(MinimumElementException):
        model.produce()

    model.min.append(EnclosedFixture())
    model.max.append(EnclosedFixture())
    with pytest.raises(MaximumElementException):
        model.produce()

def test_produce_wildcard_not_in():
    model = WildcardElementNotInFixture(local_name='WildcardElementNotInFixture', namespace='http://jaymes.biz/test', prefix='test')
    model._elements.append(EnclosedFixture(local_name='wildcard_element'))
    model._elements.append(EnclosedFixture2(local_name='wildcard_element', namespace='http://jaymes.biz/test2', prefix='test2'))

    xml = model.produce().produce()
    assert xml.startswith('<test:WildcardElementNotInFixture')
    assert 'xmlns:test="http://jaymes.biz/test"' in xml
    assert 'xmlns:test2="http://jaymes.biz/test2"' in xml
    assert '<test:wildcard_element' in xml
    assert '<test2:wildcard_element' in xml

def test_produce_wildcard_in():
    model = WildcardElementInFixture(local_name='WildcardElementInFixture', namespace='http://jaymes.biz/test', prefix='test')
    model.test_elements.append(EnclosedFixture(local_name='wildcard_element'))
    model.elements.append(EnclosedFixture2(local_name='wildcard_element'))

    xml = model.produce().produce()
    assert xml.startswith('<test:WildcardElementInFixture')
    assert 'xmlns:test="http://jaymes.biz/test"' in xml
    assert 'xmlns:test2="http://jaymes.biz/test2"' in xml
    assert '<test:wildcard_element' in xml
    assert '<test2:wildcard_element' in xml

def test_produce_list_nil():
    model = ListElementFixture(local_name='ListElementFixture', namespace='http://jaymes.biz/test', prefix='test')
    model.list_nil.append(None)
    model.list_nil.append(EnclosedFixture(value='test', local_name='list_nil'))

    xml = model.produce().produce()
    assert xml.startswith('<test:ListElementFixture')
    assert 'xmlns:test="http://jaymes.biz/test"' in xml
    assert '<test:list_nil xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:nil="true"/>' in xml
    assert '<test:list_nil>test</test:list_nil>' in xml

def test_produce_list_type():
    model = ListElementFixture(local_name='ListElementFixture', namespace='http://jaymes.biz/test', prefix='test')
    model.list_type.append(1.1)
    model.list_type.append(1.2)

    xml = model.produce().produce()
    assert xml.startswith('<test:ListElementFixture')
    assert 'xmlns:test="http://jaymes.biz/test"' in xml
    assert '<test:list_type>1.1</test:list_type>' in xml
    assert '<test:list_type>1.2</test:list_type>' in xml

def test_produce_list_class():
    model = ListElementFixture(local_name='ListElementFixture', namespace='http://jaymes.biz/test', prefix='test')
    model.list_class.append(EnclosedFixture(value='test1', local_name='list_class'))
    model.list_class.append(EnclosedFixture(value='test2', local_name='list_class'))

    xml = model.produce().produce()
    assert xml.startswith('<test:ListElementFixture')
    assert 'xmlns:test="http://jaymes.biz/test"' in xml
    assert '<test:list_class>test1</test:list_class>' in xml
    assert '<test:list_class>test2</test:list_class>' in xml

def test_produce_dict_key_explicit():
    model = DictElementFixture(local_name='DictElementFixture', namespace='http://jaymes.biz/test', prefix='test')
    model.dict_explicit_key['test1'] = 'test1'
    model.dict_explicit_key['test2'] = 'test2'

    xml = model.produce().produce()
    assert xml.startswith('<test:DictElementFixture')
    assert 'xmlns:test="http://jaymes.biz/test"' in xml
    assert '<test:dict_explicit_key key="test1">test1</test:dict_explicit_key>' in xml
    assert '<test:dict_explicit_key key="test2">test2</test:dict_explicit_key>' in xml

def test_produce_dict_key_implicit():
    model = DictElementFixture(local_name='DictElementFixture', namespace='http://jaymes.biz/test', prefix='test')
    model.dict_implicit_key['test1'] = 'test1'
    model.dict_implicit_key['test2'] = 'test2'

    xml = model.produce().produce()
    assert xml.startswith('<test:DictElementFixture')
    assert 'xmlns:test="http://jaymes.biz/test"' in xml
    assert '<test:dict_implicit_key id="test1">test1</test:dict_implicit_key>' in xml
    assert '<test:dict_implicit_key id="test2">test2</test:dict_implicit_key>' in xml

def test_produce_dict_value_nil():
    model = DictElementFixture(local_name='DictElementFixture', namespace='http://jaymes.biz/test', prefix='test')
    model.dict_value_nil['test1'] = None
    model.dict_value_nil['test2'] = 'test2'

    xml = model.produce().produce()
    assert xml.startswith('<test:DictElementFixture')
    assert 'xmlns:test="http://jaymes.biz/test"' in xml
    assert '<test:dict_value_nil id="test1" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:nil="true"/>' in xml
    assert '<test:dict_value_nil id="test2">test2</test:dict_value_nil>' in xml

def test_produce_dict_value_attr():
    model = DictElementFixture(local_name='DictElementFixture', namespace='http://jaymes.biz/test', prefix='test')
    model.dict_value_attr['test1'] = 'test1'
    model.dict_value_attr['test2'] = 'test2'

    xml = model.produce().produce()
    assert xml.startswith('<test:DictElementFixture')
    assert 'xmlns:test="http://jaymes.biz/test"' in xml
    assert '<test:dict_value_attr id="test1" value="test1"/>' in xml
    assert '<test:dict_value_attr id="test2" value="test2"/>' in xml

def test_produce_dict_value_type():
    model = DictElementFixture(local_name='DictElementFixture', namespace='http://jaymes.biz/test', prefix='test')
    model.dict_value_type['test1'] = 'test1'
    model.dict_value_type['test2'] = 'test2'

    xml = model.produce().produce()
    assert xml.startswith('<test:DictElementFixture')
    assert 'xmlns:test="http://jaymes.biz/test"' in xml
    assert '<test:dict_value_type id="test1">test1</test:dict_value_type>' in xml
    assert '<test:dict_value_type id="test2">test2</test:dict_value_type>' in xml

def test_produce_dict_value_class():
    model = DictElementFixture(local_name='DictElementFixture', namespace='http://jaymes.biz/test', prefix='test')
    model.dict_value_class['test1'] = DictValueElementFixture(value='text1', local_name='dict_value_class')
    model.dict_value_class['test1'].tag = 'blue'
    model.dict_value_class['test2'] = DictValueElementFixture(value='text2', local_name='dict_value_class')
    model.dict_value_class['test2'].tag = 'red'

    xml = model.produce().produce()
    assert xml.startswith('<test:DictElementFixture')
    assert 'xmlns:test="http://jaymes.biz/test"' in xml
    assert '<test:dict_value_class id="test1" tag="blue">text1</test:dict_value_class>' in xml
    assert '<test:dict_value_class id="test2" tag="red">text2</test:dict_value_class>' in xml

def test_in_and_out():
    test_xml = '<test:InitFixture xmlns:test="http://jaymes.biz/test">' + \
        '<test:list id="test1"/>' + \
        '<test:list id="test2"/>' + \
        '<test:list id="test3"/>' + \
        '<test:dict id="test4"/>' + \
        '<test:dict id="test5"/>' + \
        '<test:dict id="test6"/>' + \
        '<test:dict id="test7"/>' + \
        '<test:dict id="test8"/>' + \
        '<test:in_test id="test9"/>' + \
        '<test:dash-test id="test10"/>' + \
        '<test2:wildcard_element xmlns:test2="http://jaymes.biz/test2" id="test11"/>' + \
        '<test:wildcard_element id="test12"/>' + \
        '<test:dict id="test13"/>' + \
        '<test:list id="test14"/>' + \
        '</test:InitFixture>'
    doc = expatriate.Document()
    doc.parse(test_xml)
    model = Model.load(None, doc.root_element)

    out_xml = model.produce().produce()
    print(test_xml)
    print(out_xml)
    assert out_xml == test_xml

def test_load_attribute_value_in_enum():
    test_xml = '<test:RootFixture xmlns:test="http://jaymes.biz/test"><test:EnumValue>bravo</test:EnumValue></test:RootFixture>'
    doc = expatriate.Document()
    doc.parse(test_xml)
    model = Model.load(None, doc.root_element)
    assert isinstance(model, RootFixture)
    assert hasattr(model, 'EnumValue')
    assert model.EnumValue == 'bravo'

def test_load_attribute_value_not_in_enum():
    with pytest.raises(EnumerationException):
        test_xml = '<test:RootFixture xmlns:test="http://jaymes.biz/test"><test:EnumValue>delta</test:EnumValue></test:RootFixture>'
        doc = expatriate.Document()
        doc.parse(test_xml)
        model = Model.load(None, doc.root_element)

def test_load_attribute_value_matches_pattern():
    test_xml = '<test:RootFixture xmlns:test="http://jaymes.biz/test"><test:PatternValue>Bravo12</test:PatternValue></test:RootFixture>'
    doc = expatriate.Document()
    doc.parse(test_xml)
    model = Model.load(None, doc.root_element)
    assert isinstance(model, RootFixture)
    assert hasattr(model, 'PatternValue')
    assert model.PatternValue == 'Bravo12'

def test_load_attribute_value_not_matches_pattern():
    with pytest.raises(PatternException):
        test_xml = '<test:RootFixture xmlns:test="http://jaymes.biz/test"><test:PatternValue>delta</test:PatternValue></test:RootFixture>'
        doc = expatriate.Document()
        doc.parse(test_xml)
        model = Model.load(None, doc.root_element)

def test_children_dict():
    model = DictElementFixture()
    model.dict_value_type['test'] = 'test'
    assert model._children == [('dict_value_type', 'test')]

def test_children_list():
    model = ListElementFixture()
    model.list_type.append(3.5)
    assert model._children == [('list_type', 0)]

def test_children_list_ordering():
    model = ListElementFixture()
    model.list_type.append(1.1)
    model.list_type.append(2.2)
    model.list_type.append(3.3)
    model.list_type.append(4.4)
    model.list_type.remove(2.2)
    assert model._children == [('list_type', 0), ('list_type', 1), ('list_type', 2)]

def test_children_attr():
    model = RootFixture()
    model.EnclosedFixture = EnclosedFixture()
    assert model._children == [('EnclosedFixture', None)]

def test_get_attr_attr_names():
    model = AttributeFixture()
    assert model._get_attribute_mapper_attr_names() == [
        # from Model
        '_xml_lang', '_xml_space', '_xml_base', '_xml_id', '_xmlns', '_xsi_type', '_xsi_nil', '_xsi_schemaLocation', '_xsi_noNamespaceSchemaLocation',
        # from AttributeFixture
        'in_test', 'dash_attribute', 'default_attribute'
        ]

def test_get_el_attr_names():
    model = RootFixture()
    assert model._get_element_mapper_attr_names() == ['EnclosedFixture', 'EnumValue', 'PatternValue']
