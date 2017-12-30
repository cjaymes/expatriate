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

logger = logging.getLogger(__name__)

class ElementMapper:
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
    def __init__(self, **kwargs):
        if 'local_name' not in kwargs:
            raise DecoratorException('Attributes need at least local_name defined')

        self._kwargs = kwargs

    def _initialize(self, model):
        if self._kwargs['local_name'] == Model.ANY_LOCAL_NAME:
            if 'into' not in self._kwargs:
                name = '_elements'
            else:
                name = self._kwargs['into']

            if name not in model._child_map:
                logger.debug('Initializing ' + name + ' to ModelList()')
                model._child_map[name] = ModelList(model, self._kwargs)

        elif 'list' in self._kwargs:
            # initialze the array if it doesn't exist
            if self._kwargs['list'] not in model._child_map:
                logger.debug('Initializing ' + self._kwargs['list'] + ' to ModelList()')
                model._child_map[self._kwargs['list']] = ModelList(model, self._kwargs)

        elif 'dict' in self._kwargs:
            # initialze the dict if it doesn't exist
            if self._kwargs['dict'] not in model._child_map:
                logger.debug('Initializing ' + self._kwargs['dict'] + ' to ModelDict()')
                model._child_map[self._kwargs['dict']] = ModelDict(model, self._kwargs)

        else:
            if 'into' in self._kwargs:
                name = self._kwargs['into']
            else:
                name = self._kwargs['local_name'].replace('-', '_')

            if name not in model._child_map:
                logger.debug('Initializing ' + name + ' to ModelChild()')
                model._child_map[name] = ModelChild(model, self._kwargs)

    def get_namespace(self):
        if 'namespace' in self._kwargs:
            return self._kwargs['namespace']
        else:
            return None

    def get_local_name(self):
        return self._kwargs['local_name']
