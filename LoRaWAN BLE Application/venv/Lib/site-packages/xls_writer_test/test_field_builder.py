# coding=utf-8
# pylint: disable=missing-docstring

import pytest

from xls_writer import field, detail


def test_header():
  tested_field = field.FieldFactory("a header")
  assert tested_field.header == "a header"


def test_required_default():
  tested_field = field.FieldFactory("a header")
  assert not tested_field.required


@pytest.mark.parametrize('required_state', [True, False])
def test_required(required_state):
  tested_field = field.FieldFactory("a header", required=required_state)
  assert tested_field.required == required_state


def test_default_default():
  tested_field = field.FieldFactory("a header")
  assert tested_field.default is field._NO_DEFAULT  # pylint: disable=protected-access


@pytest.mark.parametrize('default', list(range(10)))
def test_default_value(default):
  tested_field = field.FieldFactory("a header", default=default).create()
  assert tested_field.default is default


def test_field_reader():
  canary = object()
  tested_field = field.FieldFactory("a header").reader(canary).create()
  assert tested_field.field_reader is canary


def test_path_reader():
  path_canary = "foo.bar.baz"
  tested_field = field.FieldFactory("a header").path(path_canary).create()
  assert isinstance(tested_field.field_reader, detail.DefaultFieldReader)
  assert tested_field.field_reader.path == ['foo', 'bar', 'baz']


def test_const_reader():
  const_canary = object()
  tested_field = field.FieldFactory("a header").const_field(const_canary).create()
  assert isinstance(tested_field.field_reader, detail.ConstReader)
  assert tested_field.field_reader.instance == const_canary


@pytest.mark.parametrize('coalesce_to', [int, float, str])
def test_type_formatter(coalesce_to):
  tested_field = field.FieldFactory("a header", required=True) \
    .path("foo.bar.baz").type_formatter(coalesce_to).create()
  assert isinstance(tested_field.field_formatter, detail.TypeFormatter)
  assert tested_field.field_formatter.object_type == coalesce_to


def test_field_formatter():
  formatter_canary = object()
  tested_field = field.FieldFactory("a header", required=True) \
    .path("foo.bar.baz").formatter(formatter_canary).create()

  assert tested_field.field_formatter is formatter_canary


def test_empty_check_default():
  tested_field = field.FieldFactory("a header").create()
  assert isinstance(tested_field.field_empty_check, detail.DefaultFieldEmptyCheck)


def test_empty_check_noop():
  tested_field = field.FieldFactory("a header").noop_empty_check().create()
  assert isinstance(tested_field.field_empty_check, detail.NoopEmptyCheck)


def test_empty_check():
  empty_check_canary = object()
  tested_field = field.FieldFactory("a header").empty_check(empty_check_canary).create()
  assert tested_field.field_empty_check is empty_check_canary


def test_enumerated_empty_check():
  canary = {1, 2, 3}
  tested_field = field.FieldFactory("a header").enumerated_empty_check(canary).create()
  assert isinstance(tested_field.field_empty_check, detail.EnumeratedFieldEmptyCheck)
  assert tested_field.field_empty_check.empty_values == canary
