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

import importlib
import logging

logger = logging.getLogger(__name__)

class AttributeMapper:
    '''
        Decorator to map xml elements to model children

        **kwargs**

        namespace
            The xml namespace to match. It can also be * to match any namespace.
            If not specified, it defaults to the parent element.
        local_name
            Required. The local name of the xml attribute we're matching. It can
            also be * to match any local name.
        into
            The python attribute to store the value of the attribute into.
            Defaults to the local_name if not specified.

        type
            The type of the expected value. Types are stored directly as data,
            no enclosed in a model class. Types usually restrict the domain
            values.
        enum
            Enumeration the attribute's value must be from
        pattern
            Pattern which the value of the attribute must match.

        required
            True or False (default). Specifies if the attribute is required.
        default
            The default value of an attribute if it isn't specified. The
            (implicit) default is None or the first item of an *enum*.

        min
            The minimum value of the attribute. Can be numeric or None (the
            default).
        max
            The maximum value of the attribute. Can be numeric or None (the
            default).

        prohibited
            The attribute should not appear in the element.
    '''
    def __init__(self, **kwargs):
        if 'local_name' not in kwargs:
            raise DecoratorException('Attributes need at least local_name defined')

        self._kwargs = kwargs

    def initialize(self, model):
        if 'into' in self._kwargs:
            attr_name = self._kwargs['into']
        else:
            attr_name = self._kwargs['local_name'].replace('-', '_')

        if 'default' in self._kwargs:
            default_value = self._kwargs['default']
        else:
            default_value = None

        setattr(model, attr_name, default_value)

        logger.debug(str(model) + ' attribute ' + attr_name + ' default ' + str(default_value))

    def get_namespace(self):
        if 'namespace' in self._kwargs:
            return self._kwargs['namespace']
        else:
            return None

    def get_local_name(self):
        return self._kwargs['local_name']

    def matches(self, attr):
        from .Model import Model

        return (self.get_namespace(), self.get_local_name()) in (
            (attr.namespace, attr.local_name),
            (None, attr.local_name),
            (attr.namespace, Model.ANY_LOCAL_NAME),
            (Model.ANY_NAMESPACE, Model.ANY_LOCAL_NAME)
        )

    def _get_attr_name(self):
        if 'into' in self._kwargs:
            return self._kwargs['into']
        else:
            return self._kwargs['local_name'].replace('-', '_')

    def parse_in(self, model, attr):
        name = self._get_attr_name()
        value = attr.value

        if 'enum' in self._kwargs and value not in self._kwargs['enum']:
            raise EnumerationException(name + ' attribute must be one of '
                + str(self._kwargs['enum']) + ': ' + str(value))

        # convert value
        if 'type' in self._kwargs:
            logger.debug('Parsing ' + str(value) + ' as '
                + str(self._kwargs['type']))
            type_ = self._kwargs['type']
            # load from a tuple (module_name, class_name) to defer class load
            if isinstance(type_, tuple):
                mod = importlib.import_module(type_[0])
                type_ = getattr(mod, type_[1])
            value = type_().parse_value(value)

        logger.debug('Setting attribute ' + name + ' = ' + str(value))

        setattr(model, name, value)

    def validate(self, model):
        name = self._kwargs['local_name']

        # check that required attributes are defined
        if (
            'required' in self._kwargs
            and self._kwargs['required']
            and not hasattr(model, name)
        ):
            raise RequiredAttributeException(str(model) + ' must define ' + name + ' attribute')

        # check that prohibited attributes are not defined
        if (
            'prohibited' in self._kwargs
            and self._kwargs['prohibited']
            and hasattr(model, name)
        ):
            raise ProhibitedAttributeException(str(model) + ' must not define ' + name + ' attribute')
