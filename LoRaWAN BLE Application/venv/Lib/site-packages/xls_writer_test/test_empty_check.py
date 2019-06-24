# coding=utf-8
# pylint: disable=missing-docstring

import pytest

from xls_writer import detail


default_test_data = (
  (None, True),
  (0, False),
  ("", False),
  ("non empty", False),
  (1, False)
)


@pytest.mark.parametrize("value, expected", default_test_data)
def test_default_empty_check(value, expected):
  check = detail.DefaultFieldEmptyCheck()
  assert expected == check(field=None, instance=value)


enumerated_empty_check_test_data = (
  # When no values are considered empty all values are not empty
  ([], None, False),
  ([], 0, False),
  ([], "", False),

  # Only values marked as empty are considered empty
  ([0, -1, None], None, True),
  ([0, -1, None], -1, True),
  ([0, -1, None], 0, True),
  ([0, -1, None], "", False),
  ([0, -1, None], "non empty", False),
  ([0, -1, None], 1, False),

  # Test for different containers for empty values
  ((0, -1, None), None, True),
  ({0, -1, None}, None, True),
  (iter({0, -1, None}), None, True),
)


@pytest.mark.parametrize("empty, value, expected", enumerated_empty_check_test_data)
def test_enumerated_check(empty, value, expected):
  check = detail.EnumeratedFieldEmptyCheck(empty_values=empty)
  assert expected == check(field=None, instance=value)
