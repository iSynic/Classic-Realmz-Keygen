$ErrorActionPreference = "Stop"

$scriptPath = Join-Path $PSScriptRoot "realmz_154_registration_helper.py"

$python = Get-Command pythonw.exe -ErrorAction SilentlyContinue
if ($null -eq $python) {
  $python = Get-Command python.exe -ErrorAction SilentlyContinue
}
if ($null -eq $python) {
  $python = Get-Command python -ErrorAction SilentlyContinue
}
if ($null -eq $python) {
  throw "Python was not found on PATH."
}

& $python.Source $scriptPath
