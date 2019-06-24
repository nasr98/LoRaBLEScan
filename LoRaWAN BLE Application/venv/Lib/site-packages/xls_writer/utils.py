# coding=utf-8
"""Misc utils"""

import typing

from . import api


def store_table(
    row_source: typing.Sequence[object],
    table: api.TableDescription,
    formatter_factory: api.FormatterFactory,
    output_file,
    close_file_on_finish: bool = True
):
  """Store table using formatter."""
  formatter = formatter_factory.create()
  try:
    formatter.initialize_file(output_file)
    formatter.write_header(table.header)
    for row in row_source:
      formatter.write_row(table.extract_row(row))
  finally:
    formatter.close(close_file_on_finish)


