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

@pytest.mark.parametrize(
    "expr, tokens",
    (
        ('"test"', ['"test"']),
        ('"test test\t test\n test"', ['"test test\t test\n test"']),
        ('3', ['3']),
        ('42', ['42']),
        ('true', ['true']),
        ('true or false', ['true', 'or', 'false']),
        ('5 mod 2', ['5', 'mod', '2']),
        ('-5 mod -2', ['-', '5', 'mod', '-', '2']),
        ('child::para', ['child', '::', 'para']),
        ('child::*', ['child', '::', '*']),
        ('child::text()', ['child', '::', 'text', '(', ')']),
        ('child::para[@id]', ['child', '::', 'para', '[', 'attribute', '::', 'id', ']']),
        ('descendant-or-self::para[@id]', ['descendant-or-self', '::', 'para', '[', 'attribute', '::', 'id', ']']),
        ('child::*/child::para', ['child', '::', '*', '/', 'child', '::', 'para']),
        ('/descendant::para', ['/', 'descendant', '::', 'para']),
        ('child::para[position()=1]', ['child', '::', 'para', '[', 'position', '(', ')', '=', '1', ']']),
        ('child::para[position()>1]', ['child', '::', 'para', '[', 'position', '(', ')', '>', '1', ']']),
        ('child::para[attribute::type="warning"]', ['child', '::', 'para', '[', 'attribute', '::', 'type', '=', '"warning"', ']']),
        ('para', ['para']),
        ('*', ['*']),
        ('@name', ['attribute', '::', 'name']),
        ('*/para', ['*', '/', 'para']),
        ('/doc/chapter[5]/section[2]', ['/', 'doc', '/', 'chapter', '[', '5', ']', '/', 'section', '[', '2', ']']),
        ('employee[@secretary and @assistant]', ['employee', '[', 'attribute', '::', 'secretary', 'and', 'attribute', '::', 'assistant', ']']),
        ('$test', ['$test']),
        ('.', ['self', '::', 'node', '(', ')']),
        ('//', ['/', 'descendant-or-self', '::', 'node', '(', ')', '/']),
        ('..', ['parent', '::', 'node', '(', ')']),
    )
)
def test_tokenization(expr, tokens):
    assert doc._tokenize(expr) == tokens
