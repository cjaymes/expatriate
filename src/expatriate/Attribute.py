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

from .Node import Node
from .xpath.Literal import Literal

logger = logging.getLogger(__name__)

class Attribute(Node):
    def __init__(self, name, value, document=None, document_order=-1, parent=None):
        super(Attribute, self).__init__(document=document, document_order=document_order, parent=parent)

        object.__setattr__(self, 'name', name)
        self._parse_name()
        self.value = value

    def get_type(self):
        return 'attribute'

    def get_string_value(self):
        return self.value

    def get_expanded_name(self):
        return (self.namespace, self.local_name)

    def __eq__(self, other):
        if isinstance(other, Literal):
            return self.value == other.value
        return other == self.value

    def __str__(self):
        s = self.__class__.__name__ + ' ' + hex(id(self)) + ' '
        if self.namespace is not None:
            s += self.namespace + ':'
        s += self.local_name + '=' + self.value
        return s
