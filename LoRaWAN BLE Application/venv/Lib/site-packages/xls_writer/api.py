# coding=utf-8
"""Module with API classes."""
import abc
import enum
import typing


class TableField(object):
  """Represents table field."""

  @property
  def header(self) -> str:
    """Field header"""
    raise NotImplementedError

  def __call__(self, row: object) -> object:
    """
    Extracts and formats data from row.
    """


class BaseToString(object):

  """Base class that creates human-readable to strings for all the objects."""

  def __repr__(self):
    return "<{typename} {dict}>".format(
      typename=type(self).__name__,
      dict=" ".join(["{0}='{1}'".format(*x) for x in sorted(self.__dict__.items())])
    )


class FieldReader(BaseToString, metaclass=abc.ABCMeta):
  """Object that extracts data from row."""

  @abc.abstractmethod
  def __call__(self, field: TableField, instance) -> object:
    """
    Extract data from row.

    :param field: Field this reader belongs to.
    :param instance: Row instance.
    :return: Cell value
    """
    raise NotImplementedError


class FieldFormatter(BaseToString, metaclass=abc.ABCMeta):
  """Formats cell value."""

  @abc.abstractmethod
  def __call__(self, field: TableField, instance) -> object:
    """

    :param field: Field this formatter belongs to.
    :param instance: Cell value.
    :return: formatted value
    """
    raise NotImplementedError


class FieldEmptyCheck(BaseToString, metaclass=abc.ABCMeta):
  """
  Checks if field value is empty. If field is empty it will be replaced with default value
  """
  @abc.abstractmethod
  def __call__(self, field: TableField, instance) -> bool:
    """

    :param field: Field this object belongs to.
    :param instance: Extracted cell value (before formatting!)
    :return: true if field IS EMPTY.
    """
    raise NotImplementedError


class TableFormatterType(enum.Enum):
  """Type of formatter: it either formats table to byte stream or string stream."""
  STRING = "STRING"
  BYTES = "BYTES"


class TableFormatter(object, metaclass=abc.ABCMeta):
  """Object that formats table to either byte stream or char stream."""

  def __init__(self):
    super().__init__()
    self.file_object = None

  @property
  @abc.abstractmethod
  def supports_streaming(self) -> bool:
    """
    Return true if formatter supports streaming that means that file can be
    streamed chunk by chunk.

    This is true for CSV formatter.
    """
    raise NotImplementedError

  @property
  @abc.abstractmethod
  def mime_type(self) -> str:
    """
    Returns mime type for created file.
    """
    raise NotImplementedError

  @property
  @abc.abstractmethod
  def expected_extension(self) -> str:
    """
    Returns expected extension for created file
    """
    raise NotImplementedError

  def initialize_file(self, file_object):
    """
    :param file_object: File opened either in binary mode (if type is BYTES or in char mode)
    """
    self.file_object = file_object

  @property
  @abc.abstractmethod
  def type(self) -> TableFormatterType:
    """
    Returns whether this formatter writes rows as bytes or
    """
    raise NotImplementedError

  def write_header(self, header: typing.Sequence[str]):
    """
    Should be called before write row.
    :param header: Header to be written
    """
    self.write_row(header)

  @abc.abstractmethod
  def write_row(self, row: typing.Sequence):
    """
    :param row: Row to be written
    """
    raise NotImplementedError

  def close(self, close_underlying_file: bool):
    """
    Closes underlying file.
    """
    self.file_object.flush()
    if close_underlying_file:
      self.file_object.close()


class FormatterFactory(object, metaclass=abc.ABCMeta):
  """Factory for formatters."""

  @abc.abstractmethod
  def create(self) -> TableFormatter:
    """Creates the formatter."""
    raise NotImplementedError


class TableDescription(object):
  """Immutable object representing a table."""

  def __init__(self, fields=typing.Sequence[TableField]):
    self.fields = tuple(fields)

  @property
  def header(self) -> typing.List[str]:
    """Table header."""
    return [
      field.header
      for field in self.fields
    ]

  def extract_row(self, row: object) -> typing.List[object]:
    """Table row."""
    return [
      field(row)
      for field in self.fields
    ]
