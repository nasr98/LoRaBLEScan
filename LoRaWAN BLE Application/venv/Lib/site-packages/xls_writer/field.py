# coding=utf-8
"""Implements the table field."""
import typing

from . import api, exceptions, detail


_NO_DEFAULT = object()


_TableField = typing.NamedTuple(
  "_TableField",
  (
    ("header", str),
    ("required", bool),
    ("default", typing.Optional[object]),
    ("field_formatter", api.FieldFormatter),
    ("field_empty_check", api.FieldEmptyCheck),
    ("field_reader", api.FieldReader),
  )
)


class DefaultField(_TableField):
  """Default implementation for api.Field."""

  def __call__(self, row):
    """Extract value from row, format it, handling defaults."""

    try:
      cell_value = self.field_reader(field=self, instance=row)
    except exceptions.MissingField:
      cell_value = None

    if self.field_empty_check(field=self, instance=cell_value):
      if self.required and self.default is _NO_DEFAULT:
        raise exceptions.MissingField(self, row)
      if self.default is not _NO_DEFAULT:
        cell_value = self.default
    if self.field_formatter:
      cell_value = self.field_formatter(field=self, instance=cell_value)
    return cell_value


class FieldFactory(object):
  """Implements a field factory."""

  @classmethod
  def create_const_field(cls, header: str, value: object) -> detail.TableField:
    """
    Create field that returns value irregardless of data what is in the row.
    """
    return cls(header=header, required=False).const_field(value).noop_empty_check().create()

  def __init__(
      self,
      header: str,
      required: bool = False,
      default: object = _NO_DEFAULT
  ):
    self.header = header
    self.required = required
    self.default = default
    self.field_reader = None
    self.field_formatter = detail.NoopFormatter()
    self.field_empty_check = detail.DefaultFieldEmptyCheck()

  def path(self, path: str) -> 'FieldFactory':
    """Read cell value using a path."""
    self.field_reader = detail.DefaultFieldReader(path=path)
    return self

  def const_field(self, const: object) -> 'FieldFactory':
    """
    Always return constant value for this field.

    This is useful if column is just missing from source data, yet must be present in output data.
    """
    self.field_reader = detail.ConstReader(instance=const)
    return self

  def reader(self, field_reader: 'api.FieldReader'):
    """
    Directly set field reader.
    """
    self.field_reader = field_reader
    return self

  def formatter(self, formatter: 'api.FieldFormatter') -> 'FieldFactory':
    """Set formatter explicitly."""
    self.field_formatter = formatter
    return self

  def type_formatter(self, object_type: type) -> 'FieldFactory':
    """
    Use formatter that coalesces to given built-in type.

    For example to format values as integers use: "self.type_formatter(int)".
    """
    self.field_formatter = detail.TypeFormatter(object_type=object_type)
    return self

  def format_formatter(self, fformat: str, object_type: type = None):
    """Adds formatter that uses str.format."""
    self.field_formatter = detail.FormatFormatter(fformat, object_type)
    return self

  def empty_check(self, empty_check: 'api.FieldEmptyCheck'):
    """Set empty-check explicitly."""
    self.field_empty_check = empty_check
    return self

  def enumerated_empty_check(self, empty_values: typing.Sequence):
    """
    Use empty check that treats special values as empty.

    For example use enumerated_empty_check([None, -1]) to treat None and -1 as missing values.
    """
    self.field_empty_check = detail.EnumeratedFieldEmptyCheck(empty_values=empty_values)
    return self

  def noop_empty_check(self):
    """Disable empty checking. """
    self.field_empty_check = detail.NoopEmptyCheck()
    return self

  def create(self) -> DefaultField:
    """Create the field."""
    return DefaultField(
      header=self.header,
      field_reader=self.field_reader,
      field_empty_check=self.field_empty_check,
      required=self.required,
      default=self.default,
      field_formatter=self.field_formatter,
    )
