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
import re

from ..decorators import *
from .TokenType import TokenType

logger = logging.getLogger(__name__)

class LanguageType(TokenType):
    def parse_value(self, value):
        m = re.fullmatch(r'[a-zA-Z]{1,8}(-[a-zA-Z0-9]{1,8})*', value)
        if not m:
            raise ValueError('xs:language must match [a-zA-Z]{1,8}(-[a-zA-Z0-9]{1,8})*')

        return super().parse_value(value)
