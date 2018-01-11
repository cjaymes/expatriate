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

from ..decorators import *
from .AnnotatedType import AnnotatedType
from .FieldElement import FieldElement
from .NCNameType import NCNameType
from .SelectorElement import SelectorElement

logger = logging.getLogger(__name__)

@attribute(local_name='name', type=NCNameType, required=True)
@element(local_name='selector', list='tags', cls=SelectorElement)
@element(local_name='field', list='tags', cls=FieldElement, min=1, max=None)
class KeybaseType(AnnotatedType):
    pass
