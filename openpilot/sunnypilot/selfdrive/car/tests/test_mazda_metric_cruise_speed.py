#!/usr/bin/env python3

from types import SimpleNamespace

from openpilot.sunnypilot.selfdrive.car.interfaces import _configure_mazda_metric_cruise_speed


class FakeParams:
  def __init__(self, is_metric):
    self.is_metric = is_metric

  def get_bool(self, key):
    assert key == "IsMetric"
    return self.is_metric


def _interface(brand):
  return SimpleNamespace(CP=SimpleNamespace(brand=brand), CS=SimpleNamespace())


def test_metric_setting_is_forwarded_to_mazda_carstate():
  CI = _interface("mazda")
  _configure_mazda_metric_cruise_speed(CI, FakeParams(True))
  assert CI.CS.use_metric_cruise_speed is True


def test_imperial_setting_keeps_mazda_correction_disabled():
  CI = _interface("mazda")
  _configure_mazda_metric_cruise_speed(CI, FakeParams(False))
  assert CI.CS.use_metric_cruise_speed is False


def test_other_brands_are_untouched():
  CI = _interface("toyota")
  _configure_mazda_metric_cruise_speed(CI, FakeParams(True))
  assert not hasattr(CI.CS, "use_metric_cruise_speed")
