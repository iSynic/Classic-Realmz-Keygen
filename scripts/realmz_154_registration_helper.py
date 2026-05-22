#!/usr/bin/env python3
"""Tiny Realmz 1.5.4 registration-code helper.

This preserves the main application registration-code check recovered from the
classic Realmz 1.5.4 68K binary. It does not generate scenario codes.
"""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk


SERIAL_BIT_8_MASK = 0x00800000


class SerialInputError(ValueError):
  """Raised when a serial-number string cannot be used."""


def normalize_serial_text(text: str) -> str:
  """Return digits from user input while allowing whitespace and separators."""
  stripped = text.strip()
  if not stripped:
    raise SerialInputError("Enter a serial number.")
  if stripped[0] in "+-":
    raise SerialInputError("Enter a positive serial number without a sign.")

  normalized = "".join(ch for ch in stripped if not ch.isspace() and ch != "-")
  if not normalized:
    raise SerialInputError("Enter a serial number.")
  if not normalized.isdigit():
    raise SerialInputError("Serial numbers can contain only digits, spaces, and dashes.")
  return normalized


def parse_serial(text: str) -> int:
  """Parse a positive Realmz serial number from GUI text."""
  serial = int(normalize_serial_text(text), 10)
  if serial <= 0:
    raise SerialInputError("Enter a positive serial number.")
  return serial


def registration_code_for_serial(serial: int) -> int:
  """Return the center Realmz 1.5.4 registration code for a serial number."""
  if serial <= 0:
    raise ValueError("serial must be positive")

  serial_for_check = serial | SERIAL_BIT_8_MASK
  return ((serial_for_check // 24) + 24) * 15 - 256


def registration_code_for_text(text: str) -> str:
  """Return the registration code string for GUI input text."""
  return str(registration_code_for_serial(parse_serial(text)))


class RegistrationHelperApp(ttk.Frame):
  def __init__(self, root: tk.Tk) -> None:
    super().__init__(root, padding=16)
    self.root = root
    self.serial_var = tk.StringVar()
    self.code_var = tk.StringVar()
    self.error_var = tk.StringVar()

    self._build_widgets()

  def _build_widgets(self) -> None:
    self.root.title("Realmz Registration Helper (Classic)")
    self.root.resizable(False, False)
    self.grid(row=0, column=0, sticky="nsew")

    title = ttk.Label(self, text="Realmz Registration Helper (Classic)", font=("", 11, "bold"))
    title.grid(row=0, column=0, columnspan=4, sticky="w", pady=(0, 12))

    ttk.Label(self, text="Serial number").grid(row=1, column=0, sticky="w", pady=(0, 4))
    serial_entry = ttk.Entry(self, textvariable=self.serial_var, width=28)
    serial_entry.grid(row=2, column=0, columnspan=4, sticky="ew")
    serial_entry.focus_set()
    serial_entry.bind("<Return>", lambda _event: self.generate())

    ttk.Label(self, text="Registration code").grid(row=3, column=0, sticky="w", pady=(12, 4))
    code_entry = ttk.Entry(self, textvariable=self.code_var, width=28, state="readonly")
    code_entry.grid(row=4, column=0, columnspan=4, sticky="ew")

    error_label = ttk.Label(self, textvariable=self.error_var, foreground="#b00020")
    error_label.grid(row=5, column=0, columnspan=4, sticky="w", pady=(8, 0))

    ttk.Button(self, text="Generate", command=self.generate).grid(row=6, column=0, sticky="ew", pady=(14, 0), padx=(0, 6))
    ttk.Button(self, text="Copy", command=self.copy_code).grid(row=6, column=1, sticky="ew", pady=(14, 0), padx=(0, 6))
    ttk.Button(self, text="Clear", command=self.clear).grid(row=6, column=2, sticky="ew", pady=(14, 0), padx=(0, 6))
    ttk.Button(self, text="Close", command=self.root.destroy).grid(row=6, column=3, sticky="ew", pady=(14, 0))

    for column in range(4):
      self.columnconfigure(column, weight=1)

  def generate(self) -> None:
    try:
      self.code_var.set(registration_code_for_text(self.serial_var.get()))
      self.error_var.set("")
    except SerialInputError as exc:
      self.code_var.set("")
      self.error_var.set(str(exc))

  def copy_code(self) -> None:
    code = self.code_var.get()
    if not code:
      self.error_var.set("Generate a registration code first.")
      return
    self.root.clipboard_clear()
    self.root.clipboard_append(code)
    self.error_var.set("")

  def clear(self) -> None:
    self.serial_var.set("")
    self.code_var.set("")
    self.error_var.set("")


def main() -> int:
  root = tk.Tk()
  RegistrationHelperApp(root)
  root.mainloop()
  return 0


if __name__ == "__main__":
  raise SystemExit(main())
