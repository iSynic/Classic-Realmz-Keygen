# Realmz Registration Helper (Classic)

Small preservation helper for the classic Mac Realmz main application
registration prompt. Tested with 1.22, 1.54, and 3.2.

Realmz has been released non-commercially by Tim Phillips. This helper is
intended for preserving and running the old classic Mac release; it does not
generate scenario registration codes.

## Web App

The static web app lives in `docs/` and can be hosted directly by GitHub Pages:

```text
https://isynic.github.io/Classic-Realmz-Keygen/
```

## Python App

Run the Tkinter version locally:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\start_realmz_154_registration_helper.ps1
```

Or run the helper directly:

```powershell
python scripts\realmz_154_registration_helper.py
```

## Check

```powershell
python scripts\check_realmz_154_registration_helper.py
```
