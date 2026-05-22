#!/usr/bin/env python3
"""Check the Realmz 1.5.4 registration helper arithmetic and validation."""

from __future__ import annotations

import sys

import realmz_154_registration_helper as helper


def assert_equal(actual: object, expected: object, label: str) -> None:
  if actual != expected:
    raise AssertionError(f"{label}: expected {expected!r}, got {actual!r}")


def assert_invalid(text: str, label: str) -> None:
  try:
    helper.registration_code_for_text(text)
  except helper.SerialInputError:
    return
  raise AssertionError(f"{label}: expected invalid input for {text!r}")


def main() -> int:
  sample_code = helper.registration_code_for_text("30267355")
  assert_equal(sample_code, "18917189", "known Realmz 1.5.4 sample")

  serial_without_bit_8 = 1234567
  serial_with_bit_8 = serial_without_bit_8 | helper.SERIAL_BIT_8_MASK
  assert_equal(
      helper.registration_code_for_serial(serial_without_bit_8),
      helper.registration_code_for_serial(serial_with_bit_8),
      "classic bit-8 registration state is normalized",
  )

  assert_equal(
      helper.registration_code_for_text("30 267-355"),
      "18917189",
      "whitespace and dashes are accepted as separators",
  )

  invalid_inputs = {
      "empty": "",
      "negative": "-30267355",
      "decimal": "30267355.0",
      "alphabetic": "30267abc",
      "zero": "0",
  }
  for label, text in invalid_inputs.items():
    assert_invalid(text, label)

  print("Realmz 1.5.4 registration helper checks passed.")
  return 0


if __name__ == "__main__":
  try:
    raise SystemExit(main())
  except AssertionError as exc:
    print(f"Realmz 1.5.4 registration helper checks failed: {exc}", file=sys.stderr)
    raise SystemExit(1)
