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

import expatriate
import importlib
import logging
import os.path
import re
import sys

from .List import List as ModelList
from .Dict import Dict as ModelDict
from .Child import Child as ModelChild
from .decorators import *
from .exceptions import *

XML_SPACE_ENUMERATION = [
    'default',
    # The value "default" signals that applications' default white-space
    # processing modes are acceptable for this element
    'preserve',
    # the value "preserve" indicates the intent that applications preserve all
    # the white space
]

logger = logging.getLogger(__name__)
#logger.setLevel(logging.INFO)

@attribute(namespace='http://www.w3.org/XML/1998/namespace', local_name='lang', type='StringType', into='_xml_lang')
@attribute(namespace='http://www.w3.org/XML/1998/namespace', local_name='space', enum=('default', 'preserve'), into='_xml_space')
@attribute(namespace='http://www.w3.org/XML/1998/namespace', local_name='base', type='AnyUriType', into='_xml_base')
@attribute(namespace='http://www.w3.org/XML/1998/namespace', local_name='id', type='ID', into='_xml_id')
@attribute(namespace='http://www.w3.org/2001/XMLSchema-instance', local_name='type', type='QNameType', into='_xsi_type')
@attribute(namespace='http://www.w3.org/2001/XMLSchema-instance', local_name='nil', type='BooleanType', into='_xsi_nil', default=False)
@attribute(namespace='http://www.w3.org/2001/XMLSchema-instance', local_name='schemaLocation', type='AnyUriType', into='_xsi_schemaLocation')
@attribute(namespace='http://www.w3.org/2001/XMLSchema-instance', local_name='noNamespaceSchemaLocation', type='AnyUriType', into='_xsi_noNamespaceSchemaLocation')
class Model(object):
    __namespace_to_package = {
        'http://www.w3.org/XML/1998/namespace': 'expatriate.model.xml',
        'http://www.w3.org/2001/XMLSchema': 'expatriate.model.xs',
        'http://www.w3.org/2001/XMLSchema-hasFacetAndProperty': 'expatriate.model.xs.hfp',
        'http://www.w3.org/2001/XMLSchema-instance': 'expatriate.model.xs.i',
    }
    __package_to_namespace = {
        'expatriate.model.xml': 'http://www.w3.org/XML/1998/namespace',
        'expatriate.model.xs': 'http://www.w3.org/2001/XMLSchema',
        'expatriate.model.xs.hfp': 'http://www.w3.org/2001/XMLSchema-hasFacetAndProperty',
        'expatriate.model.xs.i': 'http://www.w3.org/2001/XMLSchema-instance',
    }

    _model_attribute_defs = {}
    _model_element_defs = {}
    _model_element_orders = {}
    _model_content_defs = {}

    @staticmethod
    def register_namespace(model_package, namespace):
        '''
        register a namespace for use
        '''
        Model.__namespace_to_package[namespace] = model_package
        Model.__package_to_namespace[model_package] = namespace

    @staticmethod
    def unregister_namespace(model_package):
        '''
        unregister a namespace; throws UnregisteredNamespaceException if
        namespace isn't registered
        '''
        try:
            namespace = Model.__package_to_namespace[model_package]
        except KeyError:
            raise UnregisteredNamespaceException('Unregistered namespace: '
                + model_package)

        del Model.__package_to_namespace[model_package]
        del Model.__namespace_to_package[namespace]

    @staticmethod
    def package_to_namespace(model_package):
        '''
        find namespace corresponding to package
        '''
        logger.debug('Looking for xml namespace for model package '
            + model_package)
        if model_package not in Model.__package_to_namespace:
            raise UnregisteredNamespaceException('Namespace ' + model_package
                + ' is not in registered namespaces')

        return Model.__package_to_namespace[model_package]

    @staticmethod
    def namespace_to_package(namespace):
        '''
        find package corresponding to namespace
        '''
        logger.debug('Looking for model package for xml namespace ' + str(namespace))
        if namespace not in Model.__namespace_to_package:
            raise UnregisteredNamespaceException('XML namespace ' + str(namespace)
                + ' is not in registered namespaces')

        return Model.__namespace_to_package[namespace]

    @staticmethod
    def load(parent, el, el_def=None):
        '''
        load a Model given an expatriate Element
        '''

        # try to load the element's module
        if parent is None:
            if el.namespace is None:
                raise UnregisteredNamespaceException(
                    'Unable to determine namespace without fully qualified element ('
                    + str(el) + ') and parent model')

            model_package = Model.namespace_to_package(el.namespace)
            model_package, module_name = Model._map_element_to_module_name(
                model_package, el)
        else:
            if el.namespace is None:
                model_package = parent.class_from_module()
                ns_any = parent.namespace, '*'
                fq_name = parent.namespace, el.local_name
            else:
                model_package = Model.namespace_to_package(el.namespace)
                ns_any = el.namespace, '*'
                fq_name = el.namespace, el.local_name

            element_lookup = Model._get_model_element_lookup(parent.__class__)

            logger.debug('Checking ' + parent.__class__.__name__
                + ' for element ' + str(el))
            module_name = None
            for name in [fq_name, ('*', el.local_name), ns_any, ('*', '*')]:
                if name not in element_lookup:
                    continue

                logger.debug(str(el) + ' matched ' + str(name)
                    + ' mapping in ' + parent.__class__.__name__)
                if name.endswith('*'):
                    model_package, module_name = Model._map_element_to_module_name(
                        model_package, el)
                    break
                elif 'class' in element_lookup[name]:
                    module_name = element_lookup[name]['class']
                    break

            if module_name is None:
                raise TagMappingException(parent.__class__.__name__
                    + ' does not define mapping for '
                    + str(el) + ' element; does not match any of '
                    + str([fq_name, el.local_name, ns_any, ('*', '*')]))

        # qualify module name if needed
        if '.' not in module_name:
            model_module = model_package + '.' + module_name
        else:
            model_module = module_name
            module_name = module_name.rpartition('.')[2]

        # use cached copy of module if possible
        if model_module not in sys.modules:
            logger.debug('Loading module ' + model_module)
            mod = importlib.import_module(model_module)
        else:
            mod = sys.modules[model_module]

        # instantiate an instance of the class & load it
        class_ = getattr(mod, module_name)
        if el_def is not None:
            inst = class_(el_def=el_def)
        else:
            inst = class_()
        inst._from_xml(parent, el)

        return inst

    @staticmethod
    def _map_element_to_module_name(model_package, el):
        '''
        discover the model package and model name corresponding to an element
        '''
        pkg_mod = importlib.import_module(model_package)

        if not hasattr(pkg_mod, 'ELEMENT_MAP'):
            raise TagMappingException(pkg_mod.__name__
                + ' does not define ELEMENT_MAP; cannot load ' + el)
        if (el.namespace, el.local_name) not in pkg_mod.ELEMENT_MAP:
            raise TagMappingException(pkg_mod.__name__
                + ' does not define mapping for ' + el.namespace + ', '
                + el.local_name + ' element')

        return pkg_mod.__name__, pkg_mod.ELEMENT_MAP[el.namespace, el.local_name]

    @staticmethod
    def find_content(uri):
        '''
        locates content & loads it, returning the root Model
        '''

        if os.path.isfile(uri):
            try:
                doc = expatriate.Document()
                doc.parse_file(uri)
                return Model.load(None, doc.root_element)
            except:
                raise ReferenceException('Could not find content for: ' + uri)
        else:
            raise NotImplementedError('URI loading is not yet implemented')

        raise ReferenceException('Could not find content for: ' + uri)

    @classmethod
    def class_from_module(cls):
        return cls.__module__.rpartition('.')[0]

    @classmethod
    def _get_model_namespace(cls):
        '''
        determine a model's namespace from a class
        '''
        namespace = None

        # determine from package
        if namespace is None:
            namespace = Model.package_to_namespace(cls.class_from_module())

        return namespace

    @classmethod
    def _get_model_attribute_defs(cls):
        '''
        get all the attribute definitions for a model class
        '''

        at_defs = {}

        for cls_ in reversed(cls.__mro__):
            if issubclass(cls_, Model):
                try:
                    logger.debug('Adding attribute defs from superclass '
                        + cls_.__name__ + ': '
                        + str(cls_._model_attribute_defs[cls_.__name__]))
                    at_defs.update(cls_._model_attribute_defs[cls_.__name__].copy())
                except KeyError:
                    logger.debug('Class ' + cls_.__name__ + ' does not define attributes')

        logger.debug('Attribute defs for ' + cls.__name__ + str(at_defs))
        return at_defs

    @classmethod
    def _get_model_attribute_def(cls, namespace, local_name):
        '''
        get a specific attribute definition for a model class
        '''

        at_def = {}
        for cls_ in reversed(cls.__mro__):
            if issubclass(cls_, Model):
                try:
                    logger.debug('Getting attribute def ' + str(namespace) + ', '
                        + local_name + ' from superclass '
                        + cls_.__name__ + ': '
                        + str(cls_._model_attribute_defs[cls_.__name__]))
                    at_def = cls_._model_attribute_defs[cls_.__name__][namespace, local_name].copy()
                except KeyError:
                    logger.debug('Class ' + cls_.__name__
                        + ' does not define attribute ' + str(namespace) + ', '
                        + local_name)

        logger.debug('Attribute def ' + str(namespace) + ', '
            + local_name + ' for ' + cls.__name__ + ': ' + str(at_def))
        return at_def

    @classmethod
    def _set_model_attribute_def(cls, namespace, local_name, kwargs):
        '''
        set the model attribute definition for an attribute
        '''

        if cls.__name__ not in cls._model_attribute_defs:
            cls._model_attribute_defs[cls.__name__] = {}

        logger.debug('Setting ' + str(cls) + ' ' + str(namespace) + ', ' + local_name
            + ' attribute def to ' + str(kwargs))
        cls._model_attribute_defs[cls.__name__][namespace, local_name] = kwargs

    @classmethod
    def _get_model_element_defs(cls):
        '''
        get all the element definitions for a model class
        '''

        el_defs = {}

        for cls_ in reversed(cls.__mro__):
            if issubclass(cls_, Model):
                try:
                    logger.debug('Adding element defs from superclass '
                        + cls_.__name__ + ': '
                        + str(cls_._model_element_defs[cls_.__name__]))
                    el_defs.update(cls_._model_element_defs[cls_.__name__].copy())
                except KeyError:
                    logger.debug('Class ' + cls_.__name__
                        + ' does not define elements')

        logger.debug('Element defs for ' + cls.__name__ + str(el_defs))
        return el_defs

    @classmethod
    def _get_model_element_def(cls, namespace, local_name):
        '''
        get a specific element definition for a model class
        '''

        el_def = {}
        for cls_ in reversed(cls.__mro__):
            if issubclass(cls_, Model):
                try:
                    logger.debug('Getting element def ' + str(namespace) + ', '
                        + local_name + ' from superclass '
                        + cls_.__name__ + ': '
                        + str(cls_._model_element_defs[cls_.__name__]))
                    el_def = cls_._model_element_defs[cls_.__name__][namespace, local_name].copy()
                except KeyError:
                    logger.debug('Class ' + cls_.__name__
                        + ' does not define element ' + str(namespace) + ', '
                        + local_name)

        logger.debug('Element def ' + str(namespace) + ', '
            + local_name + ' for ' + cls.__name__ + ': ' + str(el_def))
        return el_def

    @classmethod
    def _set_model_element_def(cls, namespace, local_name, kwargs):
        '''
        set the model element definition for an attribute
        '''

        if cls.__name__ not in cls._model_element_defs:
            cls._model_element_defs[cls.__name__] = {}

        logger.debug('Setting ' + str(cls) + ' ' + str(namespace) + ', '
            + local_name + ' element def to ' + str(kwargs))
        cls._model_element_defs[cls.__name__][namespace, local_name] = kwargs

        # now set the order that this element was defined
        if cls.__name__ not in cls._model_element_orders:
            cls._model_element_orders[cls.__name__] = []

        # have to insert at the front because decorators are applied in reverse
        # order
        cls._model_element_orders[cls.__name__].insert(0, (namespace, local_name))

    @classmethod
    def _get_model_element_lookup(cls):
        '''
        get the element lookup dict for a class
        '''

        el_lookup = {}

        for el_def in cls._get_model_element_defs():
            if not isinstance(el_def, dict):
                raise TagMappingException('Class ' + cls.__name__
                    + ' has an invalid element definition: ' + str(el_def))

            if 'namespace' not in el_def and el_def['local_name'] == '*':
                el_lookup['*', '*'] = el_def
            elif 'namespace' in el_def:
                el_lookup[el_def['namespace'], el_def['local_name']] = el_def
            else:
                # try using element's namespace
                namespace = cls._get_model_namespace()
                el_lookup[namespace, el_def['local_name']] = el_def

        logger.debug('Element lookup for ' + cls.__name__ + str(el_lookup))
        return el_lookup

    @classmethod
    def _add_model_content_def(cls, kwargs):
        '''
        add a model content definition for the class
        '''

        logger.debug('Setting ' + str(cls) + ' content def to ' + str(kwargs))
        cls.__model_content_defs = kwargs
        if cls.__name__ not in cls._model_content_defs:
            cls._model_content_defs[cls.__name__] = []

        logger.debug('Adding ' + str(cls) + ' content def: ' + str(kwargs))
        cls._model_content_defs[cls.__name__].append(kwargs)

    @classmethod
    def _get_model_content_defs(cls):
        '''
        get the model content definitions
        '''

        return cls._model_content_defs[cls.__name__]

    def __init__(self, value=None, namespace=None, local_name=None, el_def=None):
        # child_map must be first to prevent recursion of __getattr__
        self._child_map = {}
        self._children_values = []
        self._children_el_defs = []
        self._children_keys = []
        self._parent = None

        self._references = {}

        self._value_enum = None
        self._value_pattern = None
        if el_def is not None:
            if 'value_enum' in el_def:
                self._value_enum = el_def['value_enum']
            if 'value_pattern' in el_def:
                self._value_pattern = el_def['value_pattern']

        if local_name is not None:
            self.local_name = local_name

        # must have namespace for concrete classes
        if namespace is None:
            namespace = self._get_model_namespace()
            if namespace is None:
                raise ValueError('No namespace defined for ' + self.__class__.__name__ + ' & could not detect')
            else:
                self.namespace = namespace
        else:
            self.namespace = namespace

        self._element_counts = {}

        # initialize attribute values
        for at_def in self._get_model_attribute_defs().values():
            if 'into' in at_def:
                attr_name = at_def['into']
            else:
                attr_name = at_def['local_name'].replace('-', '_')

            if 'default' in at_def:
                default_value = at_def['default']
                setattr(self, attr_name, default_value)
                logger.debug('Default of attribute ' + attr_name + ' = ' + str(default_value))
            else:
                setattr(self, attr_name, None)

        # initialize elements; if subclass defined the corresponding attribute,
        # we don't re-define
        for el_def in self._get_model_element_defs().values():
            if el_def['local_name'].endswith('*'):
                if 'into' not in el_def:
                    name = '_elements'
                else:
                    name = el_def['into']

                if name not in self._child_map:
                    logger.debug('Initializing ' + name + ' to ModelList()')
                    self._child_map[name] = ModelList(self, el_def)

            elif 'list' in el_def:
                # initialze the array if it doesn't exist
                if el_def['list'] not in self._child_map:
                    logger.debug('Initializing ' + el_def['list'] + ' to ModelList()')
                    self._child_map[el_def['list']] = ModelList(self, el_def)

            elif 'dict' in el_def:
                # initialze the dict if it doesn't exist
                if el_def['dict'] not in self._child_map:
                    logger.debug('Initializing ' + el_def['dict'] + ' to ModelDict()')
                    self._child_map[el_def['dict']] = ModelDict(self, el_def)

            else:
                if 'into' in el_def:
                    name = el_def['into']
                else:
                    name = el_def['local_name'].replace('-', '_')

                if name not in self._child_map:
                    logger.debug('Initializing ' + name + ' to ModelChild()')
                    self._child_map[name] = ModelChild(self, el_def)

        # initialize value
        # TODO we use self.text as the value storage; probably a better way
        if value is not None:
            self.set_value(value)
        else:
            self.text = None
        self.tail = None

    def is_nil(self):
        '''
        determine if the model's xsi nil is set
        '''
        return self._xsi_nil

    def set_nil(self):
        '''
        set model's xsi nil
        '''
        self._xsi_nil = True
        self.set_value(None)

    def get_value(self):
        #TODO replace for content
        logger.debug(self.__class__.__name__ + ' value currently '
            + str(self.text))
        return self.text

    def set_value(self, value):
        #TODO replace for content
        if self._value_enum is not None:
            if value not in self._value_enum:
                raise ValueError(self.__class__.__name__ + ' Invalid value '
                    + str(value) + '; not in ' + str(self._value_enum))
        if self._value_pattern is not None:
            if (
                not isinstance(value, str)
                or not re.fullmatch(self._value_pattern, value)
            ):
                raise ValueError(self.__class__.__name__ + ' Invalid value '
                    + str(value) + '; does not match ' + self._value_pattern)
        self.text = value
        logger.debug(self.__class__.__name__ + ' value set to '
            + str(self.text))

    def parse_value(self, value):
        '''
        parse the given *value* and return; overriden for value-limiting
        subclasses
        '''
        return value

    def produce_value(self, value):
        '''
        produce the given *value* and return; overriden for value-limiting
        subclasses
        '''
        if value is None:
            return value
        return str(value)

    def __str__(self):
        '''
        string representation of the model
        '''
        s = self.__class__.__module__ + '.' + self.__class__.__name__
        if hasattr(self, 'id') and self.id is not None:
            s += ' id: ' + self.id
        elif hasattr(self, 'Id') and self.Id is not None:
            s += ' Id: ' + self.Id
        elif hasattr(self, 'name') and self.name is not None:
            s += ' name: ' + self.name
        else:
            s += ' # ' + str(id(self))

        return s

    def __setattr__(self, name, value):
        '''
        setattr override to keep track of indexes etc.
        '''

        try:
            object.__getattribute__(self, '_child_map')
        except:
            # not initialzed yet, just pass through
            object.__setattr__(self, name, value)

        # keep index of 'id' attrs
        if name == 'id':
            if self._parent is not None:
                self._parent._references[value] = self
        if name == 'parent' and hasattr(self, 'id'):
            self._parent._references[self.id] = self

        if name in self._child_map:
            # capture element assignment
            el_def = self._child_map[name].el_def
            if isinstance(self._child_map[name], ModelList):
                if isinstance(value, list):
                    # wrap in ModelList
                    self._child_map[name] = ModelList(self, el_def, value)
                else:
                    raise ValueError('Trying to assign ' + value.__class__.__name__ + ' type to ' + name + ' attribute, but expecting list')
            elif isinstance(self._child_map[name], ModelDict):
                if isinstance(value, dict):
                    # wrap in ModelDict
                    self._child_map[name] = ModelDict(self, el_def, value)
                else:
                    raise ValueError('Trying to assign ' + value.__class__.__name__ + ' type to ' + name + ' attribute, but expecting dict')
            elif isinstance(self._child_map[name], ModelChild):
                # wrapped in ModelChild
                self._remove_child(self._child_map[name].value)
                self._child_map[name].value = value
                self._append_child_for(value, self._child_map[name].el_def)
            else:
                raise ValueError('Child map entry for ' + name + ' is set to an unsupported type')
        else:
            # process as regular attribute
            object.__setattr__(self, name, value)

    def __getattr__(self, name):
        '''
        getattr override to keep track of indexes etc.
        '''

        try:
            object.__getattribute__(self, '_child_map')
        except:
            # not initialzed yet, just return __getattribute__
            return object.__getattribute__(self, name)

        if name in self._child_map:
            if isinstance(self._child_map[name], ModelChild):
                return self._child_map[name].value
            else:
                return self._child_map[name]
        else:
            raise AttributeError('Attribute ' + name + ' was not found in '
                + self.__class__.__name__ + ': ' + str(self._child_map.keys()))

    def _append_child_for(self, value, el_def, key=None):
        self._children_values.append(value)
        self._children_el_defs.append(el_def)
        self._children_keys.append(key)

    def _remove_child(self, value):
        try:
            i = self._children_values.index(value)
            del self._children_values[i]
            del self._children_el_defs[i]
            del self._children_keys[i]
        except ValueError:
            pass

    def find_reference(self, ref):
        '''
        find child that matches reference *ref*
        '''

        if ref in self._references:
            return self._references[ref]
        else:
            for c in self._children_values:
                try:
                    return c.find_reference(ref)
                except:
                    pass

        raise ReferenceException('Could not find reference ' + ref + ' within ' + str(self))

    def _from_xml(self, parent, el):
        '''
        create model instance from xml element *el*
        '''
        self._parent = parent

        logger.debug('Parsing ' + str(el) + ' element into ' + self.__class__.__module__ + '.' + self.__class__.__name__ + ' class')

        self.local_name = el.local_name

        if el.namespace is None:
            # copy the parents
            self.namespace = self._parent.namespace
        else:
            self.namespace = el.namespace

        for (namespace, local_name), at_def in self._get_model_attribute_defs().items():
            # check that required attributes are defined
            if (
                'required' in at_def
                and at_def['required']
                and attrib not in el.keys()
                and 'default' not in at_def
            ):
                raise RequiredAttributeException(str(el) + ' must define ' + attrib + ' attribute')

            # check that prohibited attributes are not defined
            if (
                'prohibited' in at_def
                and at_def['prohibited']
                and attrib in el.keys()
            ):
                raise ProhibitedAttributeException(str(el) + ' must not define ' + attrib + ' attribute')

        for name, value in list(el.items()):
            self._parse_attribute(name, value)

        for sub_el in el:
            self._parse_element(sub_el)

        # check the element restrictions
        for (namespace, local_name), el_def in self._get_model_element_defs().items():
            if namespace is None and local_name == '*':
                el_spec = ('*', '*')
            elif namespace is not None:
                el_spec = (namespace, local_name)
            else:
                el_spec = (self.namespace, local_name)

            min_ = 1
            if 'dict' in el_def or 'list' in el_def or local_name == '*':
                # dicts and lists default to no max
                max_ = None
            else:
                max_ = 1

            # if there's an explicit min/max definition, use that
            if 'min' in el_def:
                min_ = el_def['min']
            if 'max' in el_def:
                max_ = el_def['max']

            # check that we have the min & max of those elements
            if min_ != 0 and (
                el_spec not in self._element_counts
                or self._element_counts[el_spec] < min_
            ):
                raise MinimumElementException(self.__class__.__name__
                    + ' must have at least ' + str(min_) + ' ' + str(el_spec)
                    + ' elements')

            if (
                max_ is not None
                and el_spec in self._element_counts
                and self._element_counts[el_spec] > max_
            ):
                raise MaximumElementException(self.__class__.__name__
                    + ' may have at most ' + str(max_) + ' ' + el_spec
                    + ' elements')

        if el.text is not None:
            self.set_value(self.parse_value(el.text))

    def _parse_attribute(self, attr):
        '''
        parse an attribute against the attribute definitions
        '''
        namespace = attr.namespace
        local_name = attr.local_name
        value = attr.value

        if namespace is None:
            ns_any = (self.namespace, '*')
            fq_key = (self.namespace, local_name)
        else:
            ns_any = (namespace, '*')
            fq_key = (namespace, local_name)

        at_defs = self._get_model_element_defs()

        for key in [fq_key, (None, local_name), ns_any, ('*', '*')]:
            if key not in at_defs:
                continue

            at_def = at_defs[key]

            if 'enum' in at_def and value not in at_def['enum']:
                raise EnumerationException(name + ' attribute must be one of '
                    + str(at_def['enum']) + ': ' + str(value))

            # convert value
            if 'type' in at_def:
                logger.debug('Parsing ' + str(value) + ' as ' + at_def['type']
                    + ' type')
                type_ = at_def['type']()
                value = type_.parse_value(value)

            if 'into' in at_def:
                name = at_def['into']
            else:
                name = local_name.replace('-', '_')

            logger.debug('Setting attribute ' + name + ' = ' + str(value))
            setattr(self, name, value)

            return

        # if we didn't find a match for the attribute, raise
        raise UnknownAttributeException('Unknown ' + str(self) + ' attribute '
            + str(namespace, local_name) + ' = ' + value)

    def _parse_element(self, el):
        '''
        parse an element against the element definitions
        '''
        namespace = el.namespace
        local_name = el.local_name

        if namespace is None:
            ns_any = (self.namespace, '*')
            fq_name = (self.namespace, local_name)
        else:
            ns_any = (namespace, '*')
            fq_name = (namespace, local_name)

        for key in [fq_name, local_name, ns_any, ('*', '*')]:
            # check both namespace + local_name and just local_name
            if key not in self._model_map['element_lookup']:
                continue

            logger.debug('Tag ' + str(el) + ' matched ' + str(key))
            el_def = self._model_map['element_lookup'][key]

            if 'ignore' in el_def and el_def['ignore'] == True:
                logger.debug('Ignoring ' + fq_name + ' element in ' + str(self))
                return

            if key[1] == '*':
                logger.debug(str(self) + ' parsing ' + str(key) + ' elements matching *')
                if 'into' in el_def:
                    name = el_def['into']
                else:
                    name = '_elements'

                lst = getattr(self, name)

                if (
                    '{http://www.w3.org/2001/XMLSchema-instance}nil' in el.keys()
                    and el.get('{http://www.w3.org/2001/XMLSchema-instance}nil') == 'true'
                ):
                    # check if we can accept nil
                    if 'nillable' in el_def and el_def['nillable']:
                        value = None
                    else:
                        raise ValueError(str(el) + ' is nil, but not expecting nil value')
                elif 'type' in el_def:
                    type_ = el_def['type']()
                    value = type_.parse_value(el.text)
                else:
                    value = Model.load(self, el, el_def=el_def)
                    value.namespace = namespace
                    value.local_name = local_name

                lst.append(value)
                logger.debug('Appended ' + str(value) + ' to ' + name)

            elif 'list' in el_def:
                logger.debug(str(self) + ' parsing ' + str(key) + ' elements into ' + el_def['list'])
                lst = getattr(self, el_def['list'])

                if (
                    '{http://www.w3.org/2001/XMLSchema-instance}nil' in el.keys()
                    and el.get('{http://www.w3.org/2001/XMLSchema-instance}nil') == 'true'
                ):
                    # check if we can accept nil
                    if 'nillable' in el_def and el_def['nillable']:
                        value = None
                    else:
                        raise ValueError(str(el) + ' is nil, but not expecting nil value')
                elif 'type' in el_def:
                    value = el_def['type']().parse_value(el.text)
                else:
                    value = Model.load(self, el, el_def=el_def)
                    value.namespace = namespace
                    value.local_name = local_name

                lst.append(value)
                logger.debug('Appended ' + str(value) + ' to ' + el_def['list'])

            elif 'dict' in el_def:
                logger.debug(str(self) + ' parsing ' + str(key) + ' elements into ' + el_def['dict'])
                dic = getattr(self, el_def['dict'])

                # TODO: implement key_element as well
                if 'key' in el_def:
                    if el_def['key'] not in el.keys():
                        key = None
                    else:
                        key = el.get(el_def['key'])
                else:
                    if 'id' not in el.keys():
                        key = None
                    else:
                        key = el.get('id')

                # TODO: implement value_element? as well
                if (
                    '{http://www.w3.org/2001/XMLSchema-instance}nil' in el.keys()
                    and el.get('{http://www.w3.org/2001/XMLSchema-instance}nil') == 'true'
                ):
                    # check if we can accept nil
                    if 'nillable' in el_def and el_def['nillable']:
                        value = None
                    else:
                        raise ValueError(str(el) + ' is nil, but not allowing nil value')
                elif 'value_attr' in el_def:
                    # try parsing from an attribute
                    if el_def['value_attr'] not in el.keys():
                        raise ValueError('Could not parse value from ' + str(el) + ' attribute ' + el_def['value_attr'])

                    if 'type' not in el_def:
                        raise ValueError('Could not parse value from ' + str(el) + ' attribute ' + el_def['value_attr'] + ' without explicit type')

                    type_ = el_def['type']()
                    value = type_.parse_value(el.get(el_def['value_attr']))
                else:
                    # try parsing from the element itself, just mapping with the key
                    if 'type' in el_def:
                        type_ = el_def['type']()
                        value = type_.parse_value(el.text)
                    else:
                        # needs 'class' in el_def
                        value = Model.load(self, el, el_def=el_def)
                        value.namespace = namespace
                        value.local_name = local_name

                dic[key] = value
                logger.debug('Mapped ' + str(key) + ' to ' + str(value) + ' in ' + el_def['dict'])

            elif 'class' in el_def:
                logger.debug(str(self) + ' parsing ' + str(key) + ' elements as ' + el_def['class'])
                if (
                    '{http://www.w3.org/2001/XMLSchema-instance}nil' in el.keys()
                    and el.get('{http://www.w3.org/2001/XMLSchema-instance}nil') == 'true'
                ):
                    # check if we can accept nil
                    if 'nillable' in el_def and el_def['nillable']:
                        value = None
                    else:
                        raise ValueError(str(el) + ' is nil, but not expecting nil value')
                else:
                    value = Model.load(self, el, el_def=el_def)
                    value.namespace = namespace
                    value.local_name = local_name

                if 'into' in el_def:
                    name = el_def['into']
                else:
                    name = local_name.replace('-', '_')

                setattr(self, name, value)
                logger.debug('Set attribute ' + str(name) + ' to ' + str(value) + ' in ' + str(self))

            elif 'type' in el_def:
                logger.debug(str(self) + ' parsing ' + str(key) + ' elements as ' + el_def['type'])
                if (
                    '{http://www.w3.org/2001/XMLSchema-instance}nil' in el.keys()
                    and el.get('{http://www.w3.org/2001/XMLSchema-instance}nil') == 'true'
                ):
                    # check if we can accept nil
                    if 'nillable' in el_def and el_def['nillable']:
                        value = None
                    else:
                        raise ValueError(str(el) + ' is nil, but not expecting nil value')
                else:
                    type_ = el_def['type']()
                    value = type_.parse_value(el.text)

                if 'into' in el_def:
                    name = el_def['into']
                else:
                    name = local_name.replace('-', '_')

                setattr(self, name, value)
                logger.debug('Set attribute ' + str(name) + ' to ' + str(value) + ' in ' + str(self))

            elif 'enum' in el_def:
                logger.debug(str(self) + ' parsing ' + str(key) + ' elements from enum ' + str(el_def['enum']))
                if el.text not in el_def['enum']:
                    raise EnumerationException(str(key) + ' value must be one of ' + str(el_def['enum']))

                if 'into' in el_def:
                    name = el_def['into']
                else:
                    name = local_name.replace('-', '_')

                value = el.text

                setattr(self, name, value)
                logger.debug('Set enum attribute ' + str(name) + ' to ' + str(value) + ' in ' + str(self))

            else:
                raise UnknownElementException(str(self) + ' could not parse ' + str(key) + ' element')

            if key not in self._element_counts:
                self._element_counts[key] = 1
            else:
                self._element_counts[key] += 1

            return

        raise UnknownElementException('Unknown ' + str(self) + ' sub-element ' + str(el) + ' does not match ' + str([fq_name, local_name, ns_any, '*']))

    def to_xml(self):
        '''
        generate xml representation of the model
        '''

        logger.debug(str(self) + ' to xml')
        el = expatriate.Element(self.local_name, namespace=self.namespace)

        for (namespace, local_name), at_def in self._get_model_attribute_defs().items():
            value = self._produce_attribute(el, namespace, local_name, at_def)

        for (namespace, local_name), el_def in self._get_model_element_defs().items():
            if el_def['local_name'].endswith('*'):
                if 'into' in el_def:
                    lst = getattr(self, el_def['into'])
                else:
                    lst = getattr(self, '_elements')

                # check minimum element count
                if 'min' in el_def and el_def['min'] > len(lst):
                    raise MinimumElementException(str(self)
                        + ' must have at least ' + str(el_def['min'])
                        + ' ' + el_def['local_name'] + ' elements; '
                        + str(len(lst)) + ' found')

                # check maximum element count
                if (
                    'max' in el_def
                    and el_def['max'] is not None
                    and el_def['max'] < len(lst)
                ):
                    raise MaximumElementException(str(self)
                        + ' may have at most ' + str(el_def['max'])
                        + ' ' + el_def['local_name'] + ' elements; '
                        + str(len(lst)) + ' found')

            elif 'list' in el_def:
                lst = getattr(self, el_def['list'])

                # check minimum element count
                if 'min' in el_def and el_def['min'] > len(lst):
                    raise MinimumElementException(str(self)
                        + ' must have at least ' + str(el_def['min'])
                        + ' ' + el_def['local_name'] + ' elements; '
                        + str(len(lst)) + ' found')

                # check maximum element count
                if (
                    'max' in el_def
                    and el_def['max'] is not None
                    and el_def['max'] < len(lst)
                ):
                    raise MaximumElementException(str(self)
                        + ' may have at most ' + str(el_def['max'])
                        + ' ' + el_def['local_name'] + ' elements; '
                        + str(len(lst)) + ' found')

            elif 'dict' in el_def:
                dct = getattr(self, el_def['dict'])

                # check minimum element count
                if 'min' in el_def and el_def['min'] > len(dct):
                    raise MinimumElementException(str(self)
                        + ' must have at least ' + str(el_def['min']) + ' '
                        + el_def['local_name'] + ' elements; '
                        + str(len(dct)) + ' found')

                # check maximum element count
                if (
                    'max' in el_def
                    and el_def['max'] is not None
                    and el_def['max'] < len(dct)
                ):
                    raise MaximumElementException(str(self)
                        + ' may have at most ' + str(el_def['max'])
                        + ' ' + el_def['local_name'] + ' elements; '
                        + str(len(dct)) + ' found')

        for i in range(0, len(self._children_values)):
            self._produce_child(i, el)

        el.text = self.produce_value(self.get_value())

        if self.tail is not None:
            el.tail = str(self.tail)

        return el

    def _produce_attribute(self, el, namespace, local_name, at_def):
        '''
        produce an attribute for xml
        '''
        if local_name.endswith('*'):
            return

        if 'into' in at_def:
            value_name = at_def['into']
        else:
            value_name = local_name.replace('-', '_')

        if not hasattr(self, value_name):
            if 'required' in at_def and at_def['required']:
                raise RequiredAttributeException(str(self)
                    + ' must assign required attribute ' + local_name)
            elif 'prohibited' in at_def and at_def['prohibited']:
                logger.debug('Skipping prohibited attribute ' + local_name)
                return
            else:
                logger.debug('Skipping undefined attribute ' + local_name)
                return
        else:
            if 'prohibited' in at_def and at_def['prohibited']:
                raise ProhibitedAttributeException(str(self)
                    + ' must not assign prohibited attribute '
                    + local_name)
            value = getattr(self, value_name)

        # TODO nillable for attrs?
        if value is None:
            if 'required' in at_def and at_def['required']:
                raise RequiredAttributeException(str(self)
                    + ' must assign required attribute ' + local_name)
            else:
                logger.debug(str(self) + ' Skipping unassigned attribute '
                    + local_name)
                return

        if 'default' in at_def and value == at_def['default']:
            logger.debug('Skipping attribute ' + local_name
                + '; remains at default ' + str(at_def['default']))
            return

        # # if model's namespace doesn't match attribute's, then we need to include it
        # if namespace is not None and self.namespace != namespace:
        #     attr_name = name

        if 'type' in at_def:
            logger.debug(str(self) + ' Producing ' + str(value) + ' as '
                + at_def['type'] + ' type')
            type_ = at_def['type']()
            v = type_.produce_value(value)

            el.set(attr_name, v)

        elif 'enum' in at_def:
            if value not in at_def['enum']:
                raise EnumerationException(str(self) + '.' + name
                    + ' attribute must be one of ' + str(at_def['enum'])
                    + ': ' + str(value))
            el.set(attr_name, value)

        else:
            # otherwise, we default to producing as string
            logger.debug(str(self) + ' Producing ' + str(value)
                + ' as String type')
            type_ = StringType()
            v = type_.produce_value(value)
            el.set(attr_name, v)

    def _produce_child(self, child_index, el):
        '''
        produce child element for xml
        '''

        child = self._children_values[child_index]
        el_def = self._children_el_defs[child_index]

        logger.debug(str(self) + ' producing ' + str(child) + ' according to ' + str(el_def))
        if el_def['local_name'] == '*':
            if 'type' in el_def and child.local_name is None:
                raise ValueError('Unable to produce wildcard elements with only "type" in the model map, because local_name is not defined')

            # TODO nillable
            el.append(child.to_xml())

        elif 'list' in el_def:
            if 'namespace' in el_def:
                namespace = el_def['namespace']
            else:
                namespace = self.namespace
            local_name = el_def['local_name']

            if 'type' in el_def:
                if child is None:
                    sub_el = expatriate.Element(local_name, namespace=namespace)
                    sub_el.set('{http://www.w3.org/2001/XMLSchema-instance}nil', 'true')
                    el.append(sub_el)
                else:
                    # wrap value in xs element
                    class_ = el_def['type']
                    child = class_(namespace=namespace, local_name=local_name, value=child)
                    el.append(child.to_xml())
            elif 'class' in el_def:
                if child is None:
                    sub_el = expatriate.Element(local_name, namespace=namespace)
                    sub_el.set('{http://www.w3.org/2001/XMLSchema-instance}nil', 'true')
                    el.append(sub_el)
                else:
                    el.append(child.to_xml())

            else:
                raise ValueError('"class" or "type" must be defined for "list" and "dict" model mapping')

        elif 'dict' in el_def:
            if 'namespace' in el_def:
                namespace = el_def['namespace']
            else:
                namespace = self.namespace
            local_name = el_def['local_name']

            # TODO: implement key_element as well
            key_name = 'id'
            if 'key' in el_def:
                key_name = el_def['key']

            if 'type' in el_def:
                sub_el = expatriate.Element(local_name, namespace=namespace)
                sub_el.set(key_name, self._children_keys[child_index])
                if 'value_attr' in el_def:
                    if child is None:
                        raise ValueError(str(self) + ' Cannot have none for a value_attr: ' + el_def['dict'] + '[' + self._children_keys[child_index] + ']')
                    type_ = el_def['type']()
                    value = type_.produce_value(child)
                    sub_el.set(el_def['value_attr'], value)
                else:
                    if child is None:
                        sub_el.set('{http://www.w3.org/2001/XMLSchema-instance}nil', 'true')
                    else:
                        type_ = el_def['type']()
                        sub_el.text = type_.produce_value(child)
                el.append(sub_el)

            elif 'class' in el_def:
                if child is None:
                    sub_el = expatriate.Element(local_name, namespace=namespace)
                    sub_el.set(key_name, self._children_keys[child_index])
                    sub_el.set('{http://www.w3.org/2001/XMLSchema-instance}nil', 'true')
                    el.append(sub_el)
                else:
                    setattr(child, key_name, self._children_keys[child_index])
                    el.append(child.to_xml())

            else:
                raise ValueError('"class" or "type" must be defined for "list" and "dict" model mapping')

        elif 'class' in el_def:
            if child is None:
                return

            el.append(child.to_xml())

        elif 'type' in el_def:
            if child is None:
                return

            if 'namespace' in el_def:
                namespace = el_def['namespace']
            else:
                namespace = self.namespace
            local_name = el_def['local_name']
            class_ = el_def['type']
            child = class_(namespace=namespace, local_name=local_name, value=child)

            el.append(child.to_xml())

        elif 'enum' in el_def:
            if child is None:
                return

            if child not in el_def['enum']:
                raise EnumerationException(str(namespace, local_name) + ' value must be one of ' + str(el_def['enum']))

            if 'namespace' in el_def:
                namespace = el_def['namespace']
            else:
                namespace = self.namespace
            local_name = el_def['local_name']
            child = String(namespace=namespace, local_name=local_name, value=child)

            el.append(child.to_xml())

        else:
            raise UnknownElementException(str(self) + ' could not produce ' + str(namespace, local_name) + ' element')
