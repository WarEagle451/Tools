@echo off
echo Enter file and flags
set /p input= ""
pushd %~dp0\..\
python sort.py %input%
pause