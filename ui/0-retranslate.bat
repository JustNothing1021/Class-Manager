::coding: GB2312
@echo off
chcp 65001
cls
setlocal enabledelayedexpansion
if not exist py md py
for %%i in (*.ui) do (
	for /f "tokens=1 delims=." %%j in ("%%i") do set "fileName=%%j"
	echo ת��%%i
	pyside6-uic %%i > py/!fileName!.py
	
)
del py\*.ui