# coding=utf-8
"""CSV Formatter"""

import csv
import typing

from . import api


class CSVFormatter(api.TableFormatter):
  """CSV formatter"""

  def __init__(self, dialect: csv.Dialect=csv.excel_tab):
    super().__init__()
    self.dialect = dialect
    self.writer = None

  def initialize_file(self, file_object):
    super().initialize_file(file_object)
    self.writer = csv.writer(self.file_object, dialect=self.dialect)

  def write_row(self, row: typing.Sequence):
    self.writer.writerow(row)

  @property
  def type(self) -> api.TableFormatterType:
    return api.TableFormatterType.STRING

  @property
  def mime_type(self) -> str:
    return "text/csv"

  @property
  def expected_extension(self) -> str:
    return "csv"

  @property
  def supports_streaming(self) -> bool:
    return True


class CSVFormatterFactory(api.FormatterFactory):
  """CSV Formatter factory"""

  def __init__(self, dialect: csv.Dialect=csv.excel_tab):
    super().__init__()
    self.dialect = dialect

  def create(self) -> api.TableFormatter:
    return CSVFormatter(dialect=self.dialect)
