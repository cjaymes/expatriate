# Copyright 2016 Casey Jaymes

# This file is part of PySCAP.
#
# PySCAP is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PySCAP is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with PySCAP.  If not, see <http://www.gnu.org/licenses/>.

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

def test_number():
    assert doc.root_element.xpath('child::*[2]') == [doc.root_element[1]]

def test_boolean():
    assert doc.root_element.xpath('child::*[position()=2]') == [doc.root_element[1]]

def test_sub_expr():
    assert doc.root_element.xpath('child::*[position()-1=1]') == [doc.root_element[1]]
