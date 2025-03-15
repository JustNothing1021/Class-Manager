::coding: gb2312_CRLF
::Tip: please use "CRLF" instead of "LF"
@echo off
chcp 936 >nul
cd /d "%~dp0"
pyinstaller main.py ^
  -w ^
  -i "./img/favicon.ico" ^
  -n "main" ^
  --contents-directory . ^
  --add-data "audio;audio" ^
  --add-data "img;img" ^
  --add-data "ui;ui" ^
  --add-data "utils;utils" ^
  --add-data "LICENSE;." ^
  --add-data "src;src" ^
  --hidden-import PyQt6.QtWebEngine ^
  --exclude-module PyQt5 ^
  --exclude-module PyQt6 ^
  --noconfirm 
pause