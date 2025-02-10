@echo off
chcp 65001 >nul
cd /d %~dp0
pyinstaller main.py -w -i ./img/favicon.ico -n ????? --contents-directory . --add-data "data;data" --add-data "audio;audio" --add-data "img;img" --add-data "ui;ui" --add-data "src;src" --add-data "ui;ui" --add-data "src;src" --add-data "LICENSE;." --add-data "chunks;chunks" -add-data "backups;backups" --add-data "utils;utils" --hidden-import PyQt6.QtWebEngine
pause