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

from expatriate.model.Model import Model
from expatriate.model.decorators import *
from expatriate.model.types import *
from .DictValueElementFixture import DictValueElementFixture

@element(local_name='dict_explicit_key', dict='dict_explicit_key', dict_key='key', type=StringType, min=0)
@element(local_name='dict_implicit_key', dict='dict_implicit_key', type=StringType, min=0)
@element(local_name='dict_value_nil', dict='dict_value_nil', nillable=True, type=StringType, min=0)
@element(local_name='dict_value_attr', dict='dict_value_attr', dict_value='value', type=StringType, min=0)
@element(local_name='dict_value_type', dict='dict_value_type', type=StringType, min=0)
@element(local_name='dict_value_class', dict='dict_value_class', cls=DictValueElementFixture, min=0)
class DictElementFixture(Model):
    pass
