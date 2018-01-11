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

@pytest.mark.parametrize(
    "test, result",
    (
        (doc.xpath('(2)'), 2),
        (doc.xpath('(2+3)+2'), 7),
    )
)
def test_subexpr(test, result):
    assert test == result

def test_left_association():
    assert doc.xpath('3 > 2 > 1') == doc.xpath('(3 > 2) > 1')

@pytest.mark.parametrize(
    "test, result",
    (
        (doc.xpath('2 '), 2),
        (doc.xpath(' 2'), 2),
        (doc.xpath(' 2 '), 2),
    )
)
def test_whitespace(test, result):
    assert test == result

def test_unclosed():
    with pytest.raises(XPathSyntaxException):
        doc.xpath('(2')
