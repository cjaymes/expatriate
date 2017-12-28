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

from expatriate.model.decorators import *

logging.basicConfig(level=logging.DEBUG)

def test_attribute():
    @attribute(namespace=None, local_name='local_name', type='type1')
    @attribute(namespace='http://jaymes.biz', local_name='xmlns_name', type='type2')
    class AttrClass(object):
        pass

    assert hasattr(AttrClass, '_model_attribute_definitions')

    assert (None, 'local_name') in AttrClass._model_attribute_definitions
    assert AttrClass._model_attribute_definitions[(None, 'local_name')]['type'] == 'type1'

    assert ('http://jaymes.biz', 'xmlns_name') in AttrClass._model_attribute_definitions
    assert AttrClass._model_attribute_definitions[('http://jaymes.biz', 'xmlns_name')]['type'] == 'type2'

def test_element():
    @element(namespace=None, local_name='local_name', type='type1')
    @element(namespace='http://jaymes.biz', local_name='xmlns_name', type='type2')
    class ElClass(object):
        pass

    assert hasattr(ElClass, '_model_element_definitions')

    assert (None, 'local_name') in ElClass._model_element_definitions
    assert ElClass._model_element_definitions[(None, 'local_name')]['type'] == 'type1'

    assert ('http://jaymes.biz', 'xmlns_name') in ElClass._model_element_definitions
    assert ElClass._model_element_definitions[('http://jaymes.biz', 'xmlns_name')]['type'] == 'type2'

    assert ElClass._model_element_order[0] == (None, 'local_name')
    assert ElClass._model_element_order[1] == ('http://jaymes.biz', 'xmlns_name')

# TODO content
