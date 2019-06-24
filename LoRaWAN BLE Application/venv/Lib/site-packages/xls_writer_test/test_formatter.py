# coding=utf-8
# pylint: disable=missing-docstring


import pytest

from xls_writer import detail
from xls_writer.detail import FormatFormatter

noop_formater_test_data = list(range(10)) + [None, "foo", "bar"]


@pytest.mark.parametrize("value", noop_formater_test_data)
def test_default_formatter(value):
  noop = detail.NoopFormatter()
  assert noop(field=None, instance=value) is value


type_formatter_test_data = (
  (int, "1", 1),
  (int, 1, 1),
  (int, 1.0, 1),
  (float, 1, 1.0),
  (str, 1, "1")
)


@pytest.mark.parametrize("object_type, value, expected", type_formatter_test_data)
def test_default_empty_check(object_type, value, expected):
  check = detail.TypeFormatter(object_type=object_type)
  assert expected == check(field=None, instance=value)


@pytest.mark.parametrize("field_format, obj_type, instance, expected", (
  ("{:d}", None, 1, "1"),
  ('{:d}', int, 1, "1"),
  ('{:06.2f}', None, 3.141, "003.14"),
  ('{:06.2f}', float, 3.141, "003.14"),
  ('{}', int, 3.141, "3"),
  ('{foo}: {bar}', None, {'foo': 1, 'bar': 2}, '1: 2')
))
def test_format_formatter(field_format, obj_type, instance, expected):
  formatter = FormatFormatter(field_format, obj_type)
  assert expected == formatter(field=None, instance=instance)


def test_to_string():
  noop = detail.NoopFormatter()
  assert str(noop) == '<NoopFormatter >'


def test_to_string_2():
  formatter = detail.TypeFormatter(object_type=int)
  assert str(formatter) == """<TypeFormatter object_type='<class 'int'>'>"""
