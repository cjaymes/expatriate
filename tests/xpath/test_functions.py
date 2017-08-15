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
import math
import pytest

from expatriate import *

logging.basicConfig(level=logging.DEBUG)

doc = Document()
doc.parse('''<?xml version='1.0' encoding='utf-8'?>
<Root xmlns="http://jaymes.biz">
    <test:para name="element1" xmlns:test="http://jaymes.biz/test">
        text node
    </test:para>
    <para name="element2"/>
    <para name="element3">
        <para name="subel1" xml:lang="en">
            <para name="kal-el">
                Superman's dad
            </para>
            <para name="kal-el" xml:lang="de">
                Supermanns Vater
            </para>
        </para>
    </para>
</Root>
''')

# # Node Set Functions

@pytest.mark.parametrize(
    "test, result",
    (
        (doc.xpath('last()'), 1),
    )
)
def test_last(test, result):
    assert test == result

# TODO actual node set

def test_position():
    assert doc.xpath('position()') == 1

# TODO actual node set

def test_count():
    assert doc.xpath('count(child::*)') == 1

def test_id():
    assert doc.xpath('id(child::*)') == 'text nodeSuperman\'s dadSupermanns Vater'

@pytest.mark.parametrize(
    "test, result",
    (
        (doc.root_element.xpath('local-name()'), 'Root'),
        (doc.root_element[0].xpath('local-name()'), 'para'),
        (doc.root_element.xpath('local-name(child::*)'), 'para'),
    )
)
def test_local_name(test, result):
    assert test == result

@pytest.mark.parametrize(
    "test, result",
    (
        (doc.root_element.xpath('namespace-uri()'), 'http://jaymes.biz'),
        (doc.root_element[0].xpath('namespace-uri()'), 'http://jaymes.biz/test'),
        (doc.root_element.xpath('namespace-uri(child::*)'), 'http://jaymes.biz/test'),
    )
)
def test_namespace_uri(test, result):
    assert test == result

@pytest.mark.parametrize(
    "test, result",
    (
        (doc.root_element.xpath('name()'), 'Root'),
        (doc.root_element[0].xpath('name()'), 'test:para'),
        (doc.root_element.xpath('name(child::*)'), 'test:para'),
    )
)
def test_name(test, result):
    assert test == result

# # String Functions

@pytest.mark.parametrize(
    "test, result",
    (
        (doc.xpath('string(3)'), '3'),
        (doc.xpath('string(3.3)'), '3.3'),
        (doc.xpath('string(true)'), 'true'),
        (doc.xpath('string("test")'), 'test'),
        (doc.xpath('string(2+2)'), '4'),
        (doc.xpath('string()'), 'text nodeSuperman\'s dadSupermanns Vater'),
        (doc.root_element[0].xpath('string()'), 'text node'),
        (doc.xpath('string(NaN)'), 'NaN'),
        (doc.xpath('string(Infinity)'), 'Infinity'),
        (doc.xpath('string(-Infinity)'), '-Infinity'),
    )
)
def test_string(test, result):
    assert test == result

@pytest.mark.parametrize(
    "expr, result",
    (
        ('concat("a", "b")', 'ab'),
        ('concat("a", "b", "c")', 'abc'),
    )
)
def test_concat(expr, result):
    assert doc.xpath(expr) == result

@pytest.mark.parametrize(
    "expr, result",
    (
        ('concat("a")', 'a'),
    )
)
def test_concat_err(expr, result):
    with pytest.raises(XPathSyntaxException):
        doc.xpath(expr)

@pytest.mark.parametrize(
    "expr, result",
    (
        ('starts-with("a", "b")', False),
        ('starts-with("apple", "a")', True),
        ('starts-with("a", "")', True),
    )
)
def test_starts_with(expr, result):
    assert doc.xpath(expr) == result

@pytest.mark.parametrize(
    "expr, result",
    (
        ('contains("apple", "a")', True),
        ('contains("apple", "b")', False),
        ('contains("a", "")', True),
    )
)
def test_contains(expr, result):
    assert doc.xpath(expr) == result

def test_substring_before():
    assert doc.xpath('substring-before("1999/04/01","/")') == '1999'

def test_substring_before():
    assert doc.xpath('substring-after("1999/04/01","/")') == '04/01'

@pytest.mark.parametrize(
    "expr, result",
    (
        ('substring("12345",2,3)', '234'),
        ('substring("12345",2)', '2345'),
        ('substring("12345", 1.5, 2.6)', '234'),
        ('substring("12345", 0, 3)', '12'),
        ('substring("12345", 0 div 0, 3)', ''),
        ('substring("12345", 1, 0 div 0)', ''),
        ('substring("12345", -42, 1 div 0)', "12345"),
        ('substring("12345", -1 div 0, 1 div 0)', ""),
    )
)
def test_substring(expr, result):
    assert doc.xpath(expr) == result

@pytest.mark.parametrize(
    "expr, result",
    (
        ('string-length("12345")', 5),
        ('string-length("")', 0),
    )
)
def test_string_length(expr, result):
    assert doc.xpath(expr) == result

def test_string_length_fail():
    with pytest.raises(XPathSyntaxException):
        doc.xpath('string-length(3)')

@pytest.mark.parametrize(
    "expr, result",
    (
        ('normalize-space("  12345")', '12345'),
        ('normalize-space("12345  ")', '12345'),
        ('normalize-space("123  45")', '123 45'),
        ('normalize-space("123\x0A\x0A45")', '123 45'),
        ('normalize-space("123\x09\x0945")', '123 45'),
        ('normalize-space("123\x0D\x0D45")', '123 45'),
    )
)
def test_normalize_space(expr, result):
    assert doc.xpath(expr) == result

@pytest.mark.parametrize(
    "expr, result",
    (
        ('translate("bar","abc","ABC")', 'BAr'),
        ('translate("--aaa--","abc-","ABC")', 'AAA'),
        ('translate("--aaa--","abc","ABC-")', '--AAA--'),
    )
)
def test_translate(expr, result):
    assert doc.xpath(expr) == result

# # Boolean Functions

@pytest.mark.parametrize(
    "test, result",
    (
        (doc.xpath('boolean(0)'), False),
        (doc.xpath('boolean(1)'), True),
        (doc.xpath('boolean(3)'), True),
        (doc.xpath('boolean(child::*)'), True),
        (doc.root_element[1].xpath('boolean(child::*)'), False),
        (doc.xpath('boolean("")'), False),
        (doc.xpath('boolean("test")'), True),
        (doc.xpath('boolean(true)'), True),
        (doc.xpath('boolean(false)'), False),
        (doc.xpath('boolean(NaN)'), False),
        (doc.xpath('boolean(-Infinity)'), True),
        (doc.xpath('boolean(Infinity)'), True),
    )
)
def test_boolean(test, result):
    assert test == result

@pytest.mark.parametrize(
    "expr, result",
    (
        ('not(true)', False),
        ('not(false)', True),
    )
)
def test_not(expr, result):
    assert doc.xpath(expr) == result

def test_true():
    assert doc.xpath('true()') == True

def test_false():
    assert doc.xpath('false()') == False

@pytest.mark.parametrize(
    "test, result",
    (
        (doc.root_element.xpath('lang("en")'), False),
        (doc.root_element[2][0].xpath('lang("en")'), True),
        (doc.root_element[2][0][0].xpath('lang("en")'), True),
        (doc.root_element[2][0][1].xpath('lang("en")'), False),
        (doc.root_element[2][0][1].xpath('lang("de")'), True),
    )
)
def test_lang(test, result):
    assert test == result

# # Number Functions

@pytest.mark.parametrize(
    "expr, result",
    (
        ('number(1)', 1),
        ('number(2.6)', 2.6),
        ('number(true)', 1),
        ('number(false)', 0),
        ('number("3")', 3),
        ('number("3.1")', 3.1),
        ('number(concat("4", "2"))', 42),
        ('number(-Infinity)', -math.inf),
        ('number(Infinity)', math.inf),
    )
)
def test_number(expr, result):
    assert doc.xpath(expr) == result

def test_number_nan():
    assert math.isnan(doc.xpath('number(NaN)'))

@pytest.mark.parametrize(
    "expr, result",
    (
        ('floor(1.1)', 1),
        ('floor(2.6)', 2),
    )
)
def test_floor(expr, result):
    assert doc.xpath(expr) == result

def test_sum():
    with pytest.raises(XPathSyntaxException):
        doc.xpath('sum(child::*)')

# TODO real sum test

@pytest.mark.parametrize(
    "expr, result",
    (
        ('ceiling(1.1)', 2),
        ('ceiling(2.6)', 3),
    )
)
def test_ceiling(expr, result):
    assert doc.xpath(expr) == result

@pytest.mark.parametrize(
    "expr, result",
    (
        ('round(1.5)', 2),
        ('round(2.6)', 3),
    )
)
def test_round(expr, result):
    assert doc.xpath(expr) == result

def test_unknown():
    with pytest.raises(XPathSyntaxException):
        doc.root_element.xpath('unknown()')
