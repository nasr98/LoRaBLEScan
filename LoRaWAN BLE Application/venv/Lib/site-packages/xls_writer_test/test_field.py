# coding=utf-8
# pylint: disable=missing-docstring,redefined-outer-name

import pytest

from xls_writer import field, exceptions

from . import helpers


int_canaries = [0, 1, 2]
float_canaries = [0.0, 1.0, 2.0]
str_canaries = ["2", "1", "0"]


default_canaries = int_canaries + float_canaries + str_canaries


@pytest.fixture(params=default_canaries)
def canary(request):
  return request.param


@pytest.fixture()
def foobarbaz_with_canary(canary):
  return helpers.foobarbaz(canary)


def test_simple_field(canary, foobarbaz_with_canary):
  tested_field = field.FieldFactory("a header").path("foo.bar.baz").create()
  for instance in foobarbaz_with_canary:
    assert tested_field(row=instance) == canary


def test_simple_field_none():
  tested_field = field.FieldFactory("a header").path("foo.bar.baz").create()
  for instance in helpers.foobarbaz(None):
    assert tested_field(row=instance) is None


def test_simple_default():
  tested_field = field.FieldFactory("a header", default="canary").path("foo.bar.baz").create()
  for instance in helpers.foobarbaz(None):
    assert tested_field(row=instance) == "canary"


def test_missing_default():
  tested_field = field.FieldFactory("a header", default="canary", required=False) \
    .path("foo.bar.baz").create()

  assert tested_field(row=object) == "canary"


def test_simple_raises():
  tested_field = field.FieldFactory("a header", required=True).path("foo.bar.baz").create()
  for instance in helpers.foobarbaz(None):
    with pytest.raises(exceptions.MissingField):
      tested_field(row=instance)


@pytest.mark.parametrize('coalesce_to', [int, float, str])
def test_field_type_formatter(coalesce_to, canary, foobarbaz_with_canary):
  tested_field = field.FieldFactory("a header", required=True) \
    .path("foo.bar.baz").type_formatter(coalesce_to).create()
  for instance in foobarbaz_with_canary:
    assert tested_field(row=instance) == coalesce_to(canary)


def test_format_formatter(canary, foobarbaz_with_canary):
  tested_field = field.FieldFactory("a header").path(
    "foo.bar.baz").format_formatter("foo {}").create()
  for instance in foobarbaz_with_canary:
    assert tested_field(row=instance) == "foo {}".format(canary)

