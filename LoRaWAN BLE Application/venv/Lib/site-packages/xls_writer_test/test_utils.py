# coding=utf-8
# pylint: disable=missing-docstring,redefined-outer-name,blacklisted-name,invalid-name

import csv
import io

import pytest

from xls_writer import api, utils, csv_formatter
from xls_writer.field import FieldFactory


@pytest.fixture()
def source_data():

  class Bar(object):
    def __init__(self, canary):
      self.baz = canary

  return [
    {"foo": "1", "bar": Bar("row 1")},
    {"foo": "2", "bar": Bar("row 2")},
    {"foo": 3}
  ]


@pytest.fixture()
def table_description():
  fields = [
    FieldFactory("Foo Header", required=True).path("foo").type_formatter(int).create(),
    FieldFactory("Bar Header", required=False, default="<<Missing>>")
    .path("bar.baz").type_formatter(str).create(),
    FieldFactory.create_const_field("Description", "Refer to terms and conditions"),
    FieldFactory.create_const_field("Custom Field 123", "")
  ]
  return api.TableDescription(fields=fields)


expected_result = (
  "Foo Header\tBar Header\tDescription\tCustom Field 123\r\n"
  "1\trow 1\tRefer to terms and conditions\t\r\n"
  "2\trow 2\tRefer to terms and conditions\t\r\n"
  "3\t<<Missing>>\tRefer to terms and conditions\t\r\n"
)


def test_csv(source_data, table_description):
  file = io.StringIO()
  formatter = csv_formatter.CSVFormatterFactory(dialect=csv.excel_tab)
  utils.store_table(source_data, table_description, formatter, file, close_file_on_finish=False)
  file.seek(0)
  actual = str(file.read(-1))
  assert actual == expected_result


@pytest.mark.parametrize('close', [True, False])
def test_formatter_closes_file_when_asked(close):
  file = io.StringIO()
  formatter = csv_formatter.CSVFormatterFactory(dialect=csv.excel_tab).create()
  formatter.initialize_file(file_object=file)
  formatter.close(close_underlying_file=close)
  assert file.closed == close


def test_csv_metadata():
  formatter = csv_formatter.CSVFormatterFactory(dialect=csv.excel_tab).create()
  assert formatter.mime_type == 'text/csv'
  assert formatter.expected_extension == "csv"
  assert formatter.supports_streaming
