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

class ElementMapper:
    def __init__(**kwargs):
        '''
            **kwargs**

            namespace
                The xml namespace to match. It can also be * to match any namespace.
                If not specified, it defaults to the parent element.
            local_name
                Required. The local name of the xml element we're matching. It can
                also be * to match any local name.

            into
                The python attribute to store the value of the element into.
                Defaults to the local_name if not specified.
            list
                The python attribute to store the value of the element into (as a
                list).  Defaults to the local_name if not specified.
            dict
                The python attribute to store the value of the element into (as a
                dict). Defaults to the local_name if not specified.

            dict_key
                The attribute of the sub-element to use as the key of the dict. By
                default it is the *id* attribute.
            dict_value
                The attribute of the sub-element to use as the value of the dict. By
                default it is the value of the element.

            Unless One of *type* or *cls* must be specified. *defer_class_load* can be
            used to load the class upon access instead of passing the class:

            type
                The type of the expected value. Types are stored directly as data,
                no enclosed in a model class. Types usually restrict the domain
                values.
            cls
                The model class with which to load the element.

            min
                The minimum number of elements to be present. Can be numeric or None
                (the  default).
            max
                The maximum number of elements to be present. Can be numeric or None
                (the default).

            enum
                Enumeration to which the value of the element must belong.
            pattern
                Pattern which the value of the element must match.

            nillable
                If True, the element can be nil (from the xsi spec). False
                specifies that it cannot (the default).
        '''
        if 'local_name' not in kwargs:
            raise DecoratorException('Attributes need at least local_name defined')

        if 'namespace' in kwargs:
            namespace = kwargs['namespace']
        else:
            namespace = None

        self._kwargs = kwargs
