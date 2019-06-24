# coding=utf-8
# pylint: disable=missing-docstring,redefined-outer-name

import pytest

from xls_writer import detail, exceptions
from xls_writer.field import FieldFactory

from . import helpers


@pytest.fixture()
def field_reader():
  return detail.DefaultFieldReader("foo.bar.baz")


def test_path(field_reader):
  assert field_reader.path == ["foo", "bar", "baz"]


@pytest.mark.parametrize("instance", helpers.foobarbaz("canary"))
def test_extraction(field_reader, instance):
  assert field_reader(field=None, instance=instance) == "canary"


def test_missing(field_reader):
  with pytest.raises(exceptions.MissingField):
    field_reader(None, object())


@pytest.mark.parametrize("instance", helpers.foobarbaz("canary"))
def test_const_field_reader(instance):
  canary = object()
  field_reader = detail.ConstReader(canary)
  assert field_reader(field=None, instance=instance) == canary


def test_multi_reader():
  instance = detail.MultiReader({
    "foo": FieldFactory.create_const_field("Foo", "foo"),
    "bar": FieldFactory.create_const_field("Bar", "bar"),
  })
  assert instance(None, None) == {'bar': 'bar', 'foo': 'foo'}
