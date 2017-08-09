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
    "expr, result",
    (
        ('"test"', 'test'),
        ('"test test\t test\n test"', 'test test\t test\n test'),
    )
)
def test_string(expr, result):
    assert doc.xpath(expr) == result

@pytest.mark.parametrize(
    "expr, result",
    (
        ('3', 3),
        ('42', 42),
        ('4.2', 4.2),
    )
)
def test_number(expr, result):
    assert doc.xpath(expr) == result

def test_true():
    assert doc.xpath('true') == True

def test_false():
    assert doc.xpath('false') == False
