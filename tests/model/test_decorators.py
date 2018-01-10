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
from expatriate.model.Model import Model

logging.basicConfig(level=logging.DEBUG)

def test_attribute():
    @attribute(namespace=None, local_name='local_name', type='type1')
    @attribute(namespace='http://jaymes.biz', local_name='xmlns_name', type='type2')
    class AttrClass(Model):
        pass

    assert hasattr(AttrClass, '_attribute_mappers')

    mapper_names = [(x.get_namespace(), x.get_local_name()) for x in AttrClass._get_attribute_mappers()]
    assert (None, 'local_name') in mapper_names
    assert ('http://jaymes.biz', 'xmlns_name') in mapper_names

def test_element():
    @element(namespace=None, local_name='local_name', type='type1')
    @element(namespace='http://jaymes.biz', local_name='xmlns_name', type='type2')
    class ElClass(Model):
        pass

    assert hasattr(ElClass, '_element_mappers')

    mapper_names = [(x.get_namespace(), x.get_local_name()) for x in ElClass._get_element_mappers()]

    assert (None, 'local_name') in mapper_names

    assert ('http://jaymes.biz', 'xmlns_name') in mapper_names

# TODO content
