@echo off
cd /d "%~dp0.."
backend\.venv\Scripts\python.exe -m backend.scripts.inspect_schema
backend\.venv\Scripts\python.exe -m backend.scripts.index_schema
pause
