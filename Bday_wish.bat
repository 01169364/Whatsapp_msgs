@echo off
:: FIX 3: Force UTF-8 and prevent early exit
chcp 65001 > nul
set PYTHONIOENCODING=utf-8
set PYTHONLEGACYWINDOWSSTDIO=utf-8

cd /d "%~dp0"

:: Run Python with unbuffered output for real-time logging
python -u whatsapp.py >> log.txt 2>&1
exit