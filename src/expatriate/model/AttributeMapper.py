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

class AttributeMapper:
    def __init__(**kwargs):
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
        if 'local_name' not in kwargs:
            raise DecoratorException('Attributes need at least local_name defined')

        if 'namespace' in kwargs:
            namespace = kwargs['namespace']
        else:
            namespace = None

        self._kwargs = kwargs

    def _assign_default_value(self, model):
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
