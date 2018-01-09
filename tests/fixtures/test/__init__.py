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

PREFIX = 'test'

ELEMENT_MAP = {
    ('http://jaymes.biz/test', 'RootFixture'): 'RootFixture',
    ('http://jaymes.biz/test', 'AttributeFixture'): 'AttributeFixture',
    ('http://jaymes.biz/test', 'RequiredAttributeFixture'): 'RequiredAttributeFixture',
    ('http://jaymes.biz/test', 'wildcard_element'): 'EnclosedFixture',
    ('http://jaymes.biz/test', 'EnclosedFixture'): 'EnclosedFixture',
    ('http://jaymes.biz/test', 'WildcardElementNotInFixture'): 'WildcardElementNotInFixture',
    ('http://jaymes.biz/test', 'WildcardElementInFixture'): 'WildcardElementInFixture',
    ('http://jaymes.biz/test', 'ListElementFixture'): 'ListElementFixture',
    ('http://jaymes.biz/test', 'DictElementFixture'): 'DictElementFixture',
    ('http://jaymes.biz/test', 'InitFixture'): 'InitFixture',
    ('http://jaymes.biz/test', 'MinMaxElementFixture'): 'MinMaxElementFixture',
}
