# coding=utf-8
"""Module with all exceptions."""


class XLSWriter(Exception):
  """Base exception"""


class MissingField(XLSWriter):
  """Raised when we are missing required field with no default."""
