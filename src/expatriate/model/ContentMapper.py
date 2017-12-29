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

class ContentMapper:
    def __init__(**kwargs):
        '''
            **kwargs**

            enum
                Enumeration the attribute's value must be from
            pattern
                Pattern which the value of the attribute must match.
            type
                Type against which a value must validate

            min
                The minimum value of the attribute. Can be numeric or None (the
                default).
            max
                The maximum value of the attribute. Can be numeric or None (the
                default).
        '''
        self._kwargs = kwargs
