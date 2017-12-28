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

import datetime
import importlib
import logging
import pkgutil
import pytest
import xml.etree.ElementTree as ET

from expatriate.model.Model import Model

# import all the classes in the package
import expatriate.model.xs as pkg
for m_finder, m_name, m_ispkg in pkgutil.iter_modules(path=pkg.__path__):
    try:
        mod = importlib.import_module(pkg.__name__ + '.' + m_name, pkg.__name__)
        globals()[m_name] = getattr(mod, m_name)
    except AttributeError:
        pass

logging.basicConfig(level=logging.DEBUG)

# NOTE: this namespace is registered by default
#Model.register_namespace('scap.model.xs', 'http://www.w3.org/2001/XMLSchema')

def test_SevenPropertyModel_init():
    spm = SevenPropertyModel()
    for i in (spm.year, spm.month, spm.day, spm.hour, spm.minute, spm.second, spm.timezoneOffset):
        assert i is None

    spm = SevenPropertyModel(year=2017, month=5, day=22)
    assert spm.year == 2017
    assert spm.month == 5
    assert spm.day == 22
    for i in (spm.hour, spm.minute, spm.second, spm.timezoneOffset):
        assert i is None

    spm = SevenPropertyModel(hour=12, minute=42, second=42)
    assert spm.hour == 12
    assert spm.minute == 42
    assert spm.second == 42
    for i in (spm.year, spm.month, spm.day, spm.timezoneOffset):
        assert i is None

    spm = SevenPropertyModel(year=2017, month=5, day=22, hour=12, minute=42, second=42)
    assert spm.year == 2017
    assert spm.month == 5
    assert spm.day == 22
    assert spm.hour == 12
    assert spm.minute == 42
    assert spm.second == 42
    assert spm.timezoneOffset is None

    spm = SevenPropertyModel(year=2017, month=5, day=22, hour=12, minute=42, second=42, timezoneOffset=60)
    assert spm.year == 2017
    assert spm.month == 5
    assert spm.day == 22
    assert spm.hour == 12
    assert spm.minute == 42
    assert spm.second == 42
    assert spm.timezoneOffset == 60

def test_SevenPropertyModel_init_date():
    spm = SevenPropertyModel(date=datetime.date(year=2017, month=5, day=22))
    assert spm.year == 2017
    assert spm.month == 5
    assert spm.day == 22
    for i in (spm.hour, spm.minute, spm.second, spm.timezoneOffset):
        assert i is None

def test_SevenPropertyModel_init_datetime():
    spm = SevenPropertyModel(datetime=datetime.datetime(year=2017, month=5, day=22, hour=12, minute=42, second=42))
    assert spm.year == 2017
    assert spm.month == 5
    assert spm.day == 22
    assert spm.hour == 12
    assert spm.minute == 42
    assert spm.second == 42
    assert spm.timezoneOffset is None

def test_SevenPropertyModel_init_time():
    spm = SevenPropertyModel(time=datetime.time(hour=12, minute=42, second=42))
    assert spm.hour == 12
    assert spm.minute == 42
    assert spm.second == 42
    for i in (spm.year, spm.month, spm.day, spm.timezoneOffset):
        assert i is None

def test_SevenPropertyModel_eq():
    assert SevenPropertyModel(hour=12, minute=42, second=42) == SevenPropertyModel(hour=12, minute=42, second=42)
    assert SevenPropertyModel(year=2017, month=5, day=22, hour=12, minute=42, second=42) == \
        SevenPropertyModel(year=2017, month=5, day=22, hour=12, minute=42, second=42)

def test_SevenPropertyModel_ne():
    assert SevenPropertyModel(hour=12, minute=42, second=42) != SevenPropertyModel(hour=13, minute=42, second=42)

def test_SevenPropertyModel_to_date():
    assert SevenPropertyModel(year=2017, month=5, day=22).to_date() == datetime.date(year=2017, month=5, day=22)
    # TODO test timezone offsets

def test_SevenPropertyModel_to_datetime():
    assert SevenPropertyModel(year=2017, month=5, day=22, hour=12, minute=42, second=42).to_datetime() == datetime.datetime(year=2017, month=5, day=22, hour=12, minute=42, second=42)
    # TODO test timezone offsets

def test_SevenPropertyModel_to_time():
    assert SevenPropertyModel(hour=12, minute=42, second=42).to_time() == datetime.time(hour=12, minute=42, second=42)
    # TODO test timezone offsets

# def test_any_simple_type():
#     pass
#
# def test_any_type():
#     pass
#
# def test_any_uri():
#     pass
#
def test_Base64BinaryType_parse():
    assert Base64BinaryType().parse_value(b'FPucA9l+') == b'\x14\xfb\x9c\x03\xd9\x7e'
    assert Base64BinaryType().parse_value(b'FPucA9k=') == b'\x14\xfb\x9c\x03\xd9'
    assert Base64BinaryType().parse_value(b'FPucAw==') == b'\x14\xfb\x9c\x03'

def test_Base64BinaryType_produce():
    assert Base64BinaryType().produce_value(b'\x14\xfb\x9c\x03\xd9\x7e') == b'FPucA9l+'
    assert Base64BinaryType().produce_value(b'\x14\xfb\x9c\x03\xd9') == b'FPucA9k='
    assert Base64BinaryType().produce_value(b'\x14\xfb\x9c\x03') == b'FPucAw=='

def test_BooleanType_parse():
    assert BooleanType().parse_value('1') == True
    assert BooleanType().parse_value('0') == False
    assert BooleanType().parse_value('true') == True
    assert BooleanType().parse_value('false') == False

def test_BooleanType_produce():
    assert BooleanType().produce_value(True) == 'True'
    assert BooleanType().produce_value(False) == 'False'

def test_ByteType_parse():
    assert ByteType().parse_value('127') == 127

def test_ByteType_produce():
    assert ByteType().produce_value(127) == '127'

def test_DateType_parse():
    assert DateType().parse_value('2017-05-16Z') == SevenPropertyModel(year=2017, month=5, day=16, timezoneOffset=0)

def test_DateType_produce():
    assert DateType().produce_value(SevenPropertyModel(year=2017, month=5, day=16, timezoneOffset=0)) == '2017-05-16Z'

def test_DateTimeType_parse():
    assert DateTimeType().parse_value('2017-05-16T12:42:42Z') == SevenPropertyModel(year=2017, month=5, day=16, hour=12, minute=42, second=42, timezoneOffset=0)

def test_DateTimeType_produce():
    assert DateTimeType().produce_value(SevenPropertyModel(year=2017, month=5, day=16, hour=12, minute=42, second=42, timezoneOffset=0)) == '2017-05-16T12:42:42Z'

def test_DateTimeStampType_parse():
    assert DateTimeStampType().parse_value('2017-05-16T12:42:42Z') == SevenPropertyModel(year=2017, month=5, day=16, hour=12, minute=42, second=42, timezoneOffset=0)

def test_DateTimeStampType_produce():
    assert DateTimeStampType().produce_value(SevenPropertyModel(year=2017, month=5, day=16, hour=12, minute=42, second=42, timezoneOffset=0)) == '2017-05-16T12:42:42Z'

def test_DayTimeDurationType_parse():
    assert DayTimeDurationType().parse_value('P1DT1H1M1.1S') == (0, 90061.1)

    assert DayTimeDurationType().parse_value('P1D') == (0, 86400.0)
    assert DayTimeDurationType().parse_value('PT1H') == (0, 3600.0)
    assert DayTimeDurationType().parse_value('PT1M') == (0, 60.0)
    assert DayTimeDurationType().parse_value('PT1S') == (0, 1.0)

    assert DayTimeDurationType().parse_value('-P1D') == (0, -86400.0)
    assert DayTimeDurationType().parse_value('-PT1H') == (0, -3600.0)
    assert DayTimeDurationType().parse_value('-PT1M') == (0, -60.0)
    assert DayTimeDurationType().parse_value('-PT1S') == (0, -1.0)

    with pytest.raises(ValueError):
        DayTimeDurationType().parse_value('P1Y1M1DT1H1M1.1S')

def test_DayTimeDurationType_produce():
    assert DayTimeDurationType().produce_value((0, 90061.1)) == 'P1DT1H1M1.100000S'

    assert DayTimeDurationType().produce_value((0, 86400.0)) == 'P1D'
    assert DayTimeDurationType().produce_value((0, 3600.0)) == 'PT1H'
    assert DayTimeDurationType().produce_value((0, 60.0)) == 'PT1M'
    assert DayTimeDurationType().produce_value((0, 1.0)) == 'PT1S'

    assert DayTimeDurationType().produce_value((0, -86400.0)) == '-P1D'
    assert DayTimeDurationType().produce_value((0, -3600.0)) == '-PT1H'
    assert DayTimeDurationType().produce_value((0, -60.0)) == '-PT1M'
    assert DayTimeDurationType().produce_value((0, -1.0)) == '-PT1S'

    with pytest.raises(ValueError):
        DayTimeDurationType().produce_value((1, 1.0))

def test_DecimalType_parse():
    assert DecimalType().parse_value('1.1') == 1.1

def test_DecimalType_produce():
    assert DecimalType().produce_value(1.1) == '1.1'

def test_DoubleType_parse():
    assert DoubleType().parse_value('1.1') == 1.1

def test_DoubleType_produce():
    assert DoubleType().produce_value(1.1) == '1.1'

def test_DurationType_parse():
    assert DurationType().parse_value('P1Y1M1DT1H1M1.1S') == (13, 90061.1)

    assert DurationType().parse_value('P1Y') == (12, 0.0)
    assert DurationType().parse_value('P1M') == (1, 0.0)
    assert DurationType().parse_value('P1D') == (0, 86400.0)
    assert DurationType().parse_value('PT1H') == (0, 3600.0)
    assert DurationType().parse_value('PT1M') == (0, 60.0)
    assert DurationType().parse_value('PT1S') == (0, 1.0)

    assert DurationType().parse_value('-P1Y') == (-12, 0.0)
    assert DurationType().parse_value('-P1M') == (-1, 0.0)
    assert DurationType().parse_value('-P1D') == (0, -86400.0)
    assert DurationType().parse_value('-PT1H') == (0, -3600.0)
    assert DurationType().parse_value('-PT1M') == (0, -60.0)
    assert DurationType().parse_value('-PT1S') == (0, -1.0)

def test_DurationType_produce():
    assert DurationType().produce_value((13, 90061.1)) == 'P1Y1M1DT1H1M1.100000S'

    assert DurationType().produce_value((12, 0.0)) == 'P1Y'
    assert DurationType().produce_value((1, 0.0)) == 'P1M'
    assert DurationType().produce_value((0, 86400.0)) == 'P1D'
    assert DurationType().produce_value((0, 3600.0)) == 'PT1H'
    assert DurationType().produce_value((0, 60.0)) == 'PT1M'
    assert DurationType().produce_value((0, 1.0)) == 'PT1S'

    assert DurationType().produce_value((-12, 0.0)) == '-P1Y'
    assert DurationType().produce_value((-1, 0.0)) == '-P1M'
    assert DurationType().produce_value((0, -86400.0)) == '-P1D'
    assert DurationType().produce_value((0, -3600.0)) == '-PT1H'
    assert DurationType().produce_value((0, -60.0)) == '-PT1M'
    assert DurationType().produce_value((0, -1.0)) == '-PT1S'

def test_EntitiesType_parse():
    assert EntitiesType().parse_value('blah0 blah1 blah2') == ('blah0', 'blah1', 'blah2')

    with pytest.raises(ValueError):
        EntitiesType().parse_value('')

def test_EntitiesType_produce():
    assert EntitiesType().produce_value(('blah0', 'blah1', 'blah2')) == 'blah0 blah1 blah2'

def test_EntityType_parse():
    assert EntityType().parse_value('test_id_4') == 'test_id_4'

def test_EntityType_produce():
    assert EntityType().produce_value('test_id_4') == 'test_id_4'

def test_FloatType_parse():
    assert FloatType().parse_value('1.1') == 1.1

def test_FloatType_produce():
    assert FloatType().produce_value(1.1) == '1.1'

def test_GDayType_parse():
    assert GDayType().parse_value('---22') == SevenPropertyModel(day=22)

def test_GDayType_produce():
    assert GDayType().produce_value(SevenPropertyModel(day=22)) == '---22'

def test_GMonthType_parse():
    assert GMonthType().parse_value('--05') == SevenPropertyModel(month=5)

def test_GMonthType_produce():
    assert GMonthType().produce_value(SevenPropertyModel(month=5)) == '--05'

def test_GMonthDayType_day_parse():
    assert GMonthDayType().parse_value('--05-22') == SevenPropertyModel(month=5, day=22)

def test_GMonthDayType_produce():
    assert GMonthDayType().produce_value(SevenPropertyModel(month=5, day=22)) == '--05-22'

def test_GYearType_parse():
    assert GYearType().parse_value('2017') == SevenPropertyModel(year=2017)

def test_GYearType_produce():
    assert GYearType().produce_value(SevenPropertyModel(year=2017)) == '2017'

def test_GYearMonthType_parse():
    assert GYearMonthType().parse_value('2017-05') == SevenPropertyModel(year=2017, month=5)

def test_GYearMonthType_produce():
    assert GYearMonthType().produce_value(SevenPropertyModel(year=2017, month=5)) == '2017-05'

def test_HexBinaryType_parse():
    assert HexBinaryType().parse_value(b'14fb9c03d97e') == b'\x14\xfb\x9c\x03\xd9\x7e'
    assert HexBinaryType().parse_value(b'14fb9c03d9') == b'\x14\xfb\x9c\x03\xd9'
    assert HexBinaryType().parse_value(b'14fb9c03') == b'\x14\xfb\x9c\x03'

def test_HexBinaryType_produce():
    assert HexBinaryType().produce_value(b'\x14\xfb\x9c\x03\xd9\x7e') == b'14fb9c03d97e'
    assert HexBinaryType().produce_value(b'\x14\xfb\x9c\x03\xd9') == b'14fb9c03d9'
    assert HexBinaryType().produce_value(b'\x14\xfb\x9c\x03') == b'14fb9c03'

def test_IdType_parse():
    assert IdType().parse_value('test_id_4') == 'test_id_4'

def test_IdType_produce():
    assert IdType().produce_value('test_id_4') == 'test_id_4'

def test_IdRefType_parse():
    assert IdRefType().parse_value('test_id_4') == 'test_id_4'

def test_IdRefType_produce():
    assert IdRefType().produce_value('test_id_4') == 'test_id_4'

def test_IdRefsType_parse():
    assert IdRefsType().parse_value('blah0 blah1 blah2') == ('blah0', 'blah1', 'blah2')

    with pytest.raises(ValueError):
        IdRefsType().parse_value('')

    assert IdRefsType().produce_value(('blah0', 'blah1', 'blah2')) == 'blah0 blah1 blah2'

def test_IdRefsType_produce():
    assert IdRefsType().produce_value(('blah0', 'blah1', 'blah2')) == 'blah0 blah1 blah2'

def test_IntType_parse():
    assert IntType().parse_value('255') == 255

def test_IntType_produce():
    assert IntType().produce_value(255) == '255'

def test_IntegerType_parse():
    assert IntegerType().parse_value('255') == 255

def test_IntegerType_produce():
    assert IntegerType().produce_value(255) == '255'

def test_LanguageType_parse():
    assert LanguageType().parse_value('en') == 'en'
    assert LanguageType().parse_value('en-US') == 'en-US'
    assert LanguageType().parse_value('en-gb') == 'en-gb'

    with pytest.raises(ValueError):
        LanguageType().parse_value('')

def test_LanguageType_parse():
    assert LanguageType().produce_value('en') == 'en'
    assert LanguageType().produce_value('en-US') == 'en-US'

def test_LongType_parse():
    assert LongType().parse_value('255') == 255

def test_LongType_produce():
    assert LongType().produce_value(255) == '255'

def test_NameType_parse():
    assert NameType().parse_value('test_id_4') == 'test_id_4'

    with pytest.raises(ValueError):
        NameType().parse_value('4test_id_4')

def test_NameType_produce():
    assert NameType().produce_value('test_id_4') == 'test_id_4'

def test_NCNameType_parse():
    assert NCNameType().parse_value('test_id_4') == 'test_id_4'

    with pytest.raises(ValueError):
        NCNameType().parse_value('test:id_4')

def test_NCNameType_produce():
    assert NCNameType().produce_value('test_id_4') == 'test_id_4'

def test_NegativeIntegerType_parse():
    assert NegativeIntegerType().parse_value('-255') == -255

def test_NegativeIntegerType_produce():
    assert NegativeIntegerType().produce_value(-255) == '-255'

def test_NMTokenType_parse():
    assert NMTokenType().parse_value('xml_schema') == 'xml_schema'
    assert NMTokenType().parse_value('2xml_schema') == '2xml_schema'
    assert NMTokenType().parse_value('-xml_schema') == '-xml_schema'
    assert NMTokenType().parse_value('.xml_schema') == '.xml_schema'

    with pytest.raises(ValueError):
        NMTokenType().parse_value('\x0dtoken')

def test_NMTokenType_produce():
    assert NMTokenType().produce_value('xml_schema') == 'xml_schema'

def test_NMTokensType_parse():
    assert NMTokensType().parse_value('xml_schema') == ('xml_schema',)
    assert NMTokensType().parse_value('xml_schema xml_schema2') == ('xml_schema', 'xml_schema2')

    with pytest.raises(ValueError):
        NMTokensType().parse_value('\x0dtoken')

def test_NMTokensType_produce():
    assert NMTokensType().produce_value(('xml_schema',)) == 'xml_schema'
    assert NMTokensType().produce_value(('xml_schema', 'xml_schema2')) == 'xml_schema xml_schema2'

def test_NonNegativeIntegerType_parse():
    assert NonNegativeIntegerType().parse_value('255') == 255

def test_NonNegativeIntegerType_produce():
    assert NonNegativeIntegerType().produce_value(255) == '255'

def test_NonPositiveIntegerType_parse():
    assert NonPositiveIntegerType().parse_value('-255') == -255

def test_NonPositiveIntegerType_produce():
    assert NonPositiveIntegerType().produce_value(-255) == '-255'

def test_NormalizedStringType_parse():
    assert NormalizedStringType().parse_value('test_id_4') == 'test_id_4'

def test_NormalizedStringType_produce():
    assert NormalizedStringType().produce_value('test_id_4') == 'test_id_4'

def test_NotationType_parse():
    assert NotationType().parse_value('test_id_4') == 'test_id_4'

def test_NotationType_produce():
    assert NotationType().produce_value('test_id_4') == 'test_id_4'

def test_PositiveIntegerType_parse():
    assert PositiveIntegerType().parse_value('255') == 255

def test_PositiveIntegerType_produce():
    assert PositiveIntegerType().produce_value(255) == '255'

def test_QNameType_parse():
    assert QNameType().parse_value('test_id_4') == 'test_id_4'

def test_QNameType_produce():
    assert QNameType().produce_value('test_id_4') == 'test_id_4'

def test_ShortType_parse():
    assert ShortType().parse_value('255') == 255

def test_ShortType_produce():
    assert ShortType().produce_value(255) == '255'

def test_StringType_parse():
    assert StringType().parse_value('test') == 'test'

    with pytest.raises(TypeError):
        StringType().parse_value(2)
    with pytest.raises(TypeError):
        StringType().parse_value(2.0)
    with pytest.raises(TypeError):
        StringType().parse_value(StringType())

def test_StringType_produce():
    assert StringType().produce_value('255') == '255'

def test_TimeType_parse():
    assert TimeType().parse_value('12:42:42Z') == SevenPropertyModel(hour=12, minute=42, second=42, timezoneOffset=0)

def test_TimeType_produce():
    assert TimeType().produce_value(SevenPropertyModel(hour=12, minute=42, second=42, timezoneOffset=0)) == '12:42:42Z'

def test_TokenType_parse():
    assert TokenType().parse_value('test') == 'test'

def test_TokenType_produce():
    assert TokenType().produce_value('test') == 'test'

def test_UnsignedByteType_parse():
    assert UnsignedByteType().parse_value('255') == 255

def test_UnsignedByteType_produce():
    assert UnsignedByteType().produce_value(255) == '255'

def test_UnsignedIntType_parse():
    assert UnsignedIntType().parse_value('255') == 255

def test_UnsignedIntType_produce():
    assert UnsignedIntType().produce_value(255) == '255'

def test_UnsignedLongType_parse():
    assert UnsignedLongType().parse_value('255') == 255

def test_UnsignedLongType_produce():
    assert UnsignedLongType().produce_value(255) == '255'

def test_UnsignedShortType_parse():
    assert UnsignedShortType().parse_value('255') == 255

def test_UnsignedShortType_produce():
    assert UnsignedShortType().produce_value(255) == '255'

def test_YearMonthDurationType_parse():
    assert YearMonthDurationType().parse_value('P1Y1M') == (13, 0)

    assert YearMonthDurationType().parse_value('P1Y') == (12, 0.0)
    assert YearMonthDurationType().parse_value('P1M') == (1, 0.0)

    assert YearMonthDurationType().parse_value('-P1Y') == (-12, 0.0)
    assert YearMonthDurationType().parse_value('-P1M') == (-1, 0.0)

    with pytest.raises(ValueError):
        DayTimeDurationType().parse_value('P1Y1M1DT1H1M1.1S')

def test_YearMonthDurationType_produce():
    assert YearMonthDurationType().produce_value((13, 0)) == 'P1Y1M'

    assert YearMonthDurationType().produce_value((12, 0.0)) == 'P1Y'
    assert YearMonthDurationType().produce_value((1, 0.0)) == 'P1M'

    assert YearMonthDurationType().produce_value((-12, 0.0)) == '-P1Y'
    assert YearMonthDurationType().produce_value((-1, 0.0)) == '-P1M'

    with pytest.raises(ValueError):
        DayTimeDurationType().produce_value((1, 1.0))
