.. XML Object Relational Modeling

******************************
XML Object Relational Modeling
******************************

=======
Classes
=======

.. autoclass:: expatriate.model.Model
    :members:

==========
Decorators
==========

The decorators can be all imported with the following::

    from expatriate.model.decorators import *

.. py:decorator:: attribute

    Decorator to map xml attributes to model attributes

    Used as follows::

        @attribute(local_name='test', type=StringType)
        class ModelWithTestAttribute(Model):
            pass

    :param str namespace: The xml namespace to match. It can also be * to match any namespace. If not specified, it defaults to the parent element's namespace.
    :param str local_name: Required. The local name of the xml attribute we're matching. It can also be * to match any local name.
    :param str into: The python attribute to store the value of the attribute into. Defaults to the local_name if not specified.
    :param type: The type of the expected value. Types are stored directly as data, no enclosed in a model class. Types usually restrict the domain values.
    :type type: class or tuple(package_str, class_str)
    :param enum: Enumeration the attribute's value must be from
    :type enum: list or tuple
    :param str pattern: Pattern which the value of the attribute must match.
    :param bool required: True or False (default). Specifies if the attribute is required.
    :param default: The default value of an attribute if it isn't specified. The (implicit) default is None or the first item of an *enum*.
    :param min: The minimum value of the attribute. Can be numeric or None (the default).
    :param max: The maximum value of the attribute. Can be numeric or None (the default).
    :param prohibited: The attribute should not appear in the element.

.. py:decorator:: element

    Decorator to map xml elements to model children.

    One of *type* or *cls* must be specified. If the type/class cannot be passed in
    by object, a tuple with the package and name of the class may be passed to
    defer the import of the class.

    Used as follows::

        @element(namespace='http://jaymes.biz/test', local_name='test',
            list='test', type=StringType)
        class ModelWithTestChildrenInAList(Model):
            pass

    :param namespace: The xml namespace to match. It can also be * to match any namespace. If not specified, it defaults to the parent element.
    :param local_name: Required. The local name of the xml element we're matching. It can also be * to match any local name.
    :param into: The python attribute to store the value of the element into. Defaults to the local_name if not specified.
    :param list: The python attribute to store the value of the element into (as a list).  Defaults to the local_name if not specified.
    :param dict: The python attribute to store the value of the element into (as a dict). Defaults to the local_name if not specified.
    :param dict_key: The attribute of the sub-element to use as the key of the dict. By default it is the *id* attribute.
    :param dict_value: The attribute of the sub-element to use as the value of the dict. By default it is the value of the element.
    :param type: The type of the expected value. Types are stored directly as data, no enclosed in a model class. Types usually restrict the domain values.
    :param cls: The model class with which to load the element.
    :param min: The minimum number of elements to be present. Can be numeric or None (the  default).
    :param max: The maximum number of elements to be present. Can be numeric or None (the default).
    :param enum: Enumeration to which the value of the element must belong.
    :param pattern: Pattern which the value of the element must match.
    :param nillable: If True, the element can be nil (from the xsi spec). False specifies that it cannot (the default).

.. py:decorator:: content

    Decorator to map xml element content to model data.

    Used as follows::

        @content(enum=('value1', 'value2'))
        class Value1Or2(Model):
            pass

    :param enum: Enumeration the attribute's value must be from
    :param pattern: Pattern which the value of the attribute must match.
    :param type: Type against which a value must validate
    :param min: The minimum value of the attribute. Can be numeric or None (the default).
    :param max: The maximum value of the attribute. Can be numeric or None (the default).

===========
Basic Types
===========

Simple types defined by `XML Schema <http://www.w3.org/2001/XMLSchema>`_. All
are imported by::

    from expatriate.model.types import *

.. py:class:: AllNniType
.. py:class:: AnySimpleType
.. py:class:: AnyTypeType
.. py:class:: AnyUriType
.. py:class:: Base64BinaryType
.. py:class:: BooleanType
.. py:class:: ByteType
.. py:class:: DateTimeStampType
.. py:class:: DateTimeType
.. py:class:: DateType
.. py:class:: DayTimeDurationType
.. py:class:: DecimalType
.. py:class:: DoubleType
.. py:class:: DurationType
.. py:class:: EntitiesType
.. py:class:: EntityType
.. py:class:: FloatType
.. py:class:: GDayType
.. py:class:: GMonthDayType
.. py:class:: GMonthType
.. py:class:: GYearMonthType
.. py:class:: GYearType
.. py:class:: HexBinaryType
.. py:class:: IdRefsType
.. py:class:: IdRefType
.. py:class:: IdType
.. py:class:: IntegerType
.. py:class:: IntType
.. py:class:: LanguageType
.. py:class:: LongType
.. py:class:: NamespaceListType
.. py:class:: NameType
.. py:class:: NCNameType
.. py:class:: NegativeIntegerType
.. py:class:: NMTokensType
.. py:class:: NMTokenType
.. py:class:: NonNegativeIntegerType
.. py:class:: NonPositiveIntegerType
.. py:class:: NormalizedStringType
.. py:class:: PositiveIntegerType
.. py:class:: QNameType
.. py:class:: ShortType
.. py:class:: StringType
.. py:class:: TimeType
.. py:class:: TokenType
.. py:class:: UnsignedByteType
.. py:class:: UnsignedIntType
.. py:class:: UnsignedLongType
.. py:class:: UnsignedShortType
.. py:class:: YearMonthDurationType

===============
Support Classes
===============

These classes are used (via decorators) to map xml data to and from
:py:class:`Model` objects.

.. py:class:: AttributeMapper
.. py:class:: ContentMapper
.. py:class:: ElementMapper
.. py:class:: Mapper

===========
Exceptions
===========

Exceptions are available by::

    from expatriate.model.exceptions import *

.. py:exception:: expatriate.model.exceptions.DecoratorException
.. py:exception:: expatriate.model.exceptions.ElementMappingException
.. py:exception:: expatriate.model.exceptions.ReferenceException
.. py:exception:: expatriate.model.exceptions.RequiredAttributeException
.. py:exception:: expatriate.model.exceptions.ProhibitedAttributeException
.. py:exception:: expatriate.model.exceptions.UnknownAttributeException
.. py:exception:: expatriate.model.exceptions.UnknownElementException
.. py:exception:: expatriate.model.exceptions.MinimumElementException
.. py:exception:: expatriate.model.exceptions.MaximumElementException
.. py:exception:: expatriate.model.exceptions.EnumerationException
.. py:exception:: expatriate.model.exceptions.PatternException
