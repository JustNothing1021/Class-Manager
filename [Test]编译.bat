::coding: GB2312
@echo off
chcp 65001 >nul
cd /d %~dp0
pyinstaller main.py -w -i ./img/favicon.ico -n °à¼Ä¹ÜÀí --contents-directory . --add-data "audio;audio" --add-data "img;img" --add-data "ui;ui" --add-data "src;src" --add-data "ui;ui" --add-data "src;src" --add-data "LICENSE;." --add-data "utils;utils" --hidden-import PyQt6.QtWebEngine --exclude PyQt5
pause