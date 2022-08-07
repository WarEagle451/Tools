@echo off
pushd %~dp0\..\
echo Set directory: %cd%
echo Enter file and flags
set /p input= ""
python sort.py %input%
pause