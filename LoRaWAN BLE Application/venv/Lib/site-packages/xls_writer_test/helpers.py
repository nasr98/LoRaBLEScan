# coding=utf-8

# pylint: disable=missing-docstring,blacklisted-name


def foobarbaz_dict(canary="canary"):
  return {"foo": {"bar": {"baz": canary}}}


def foobarbaz_object(canary="canary"):
  class Baz(object):
    def __init__(self):
      self.baz = canary

  class BarBaz(object):
    def __init__(self):
      self.bar = Baz()

  class FooBarBaz(object):
    def __init__(self):
      self.foo = BarBaz()

  return FooBarBaz()


def foobarbaz_mixed(canary="canary"):
  class Baz(object):
    def __init__(self):
      self.baz = canary

  return {"foo": {"bar": Baz()}}


def foobarbaz(canary="canary"):
  return [foobarbaz_dict(canary), foobarbaz_mixed(canary), foobarbaz_object(canary)]
