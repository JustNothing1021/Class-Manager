:: coding: utf-8
:: 问题不大，因为已经chcp 65001了（
:: gb2312看着好像会出问题
@echo off
chcp 65001 >nul
cd /d %~dp0
pyinstaller main.py -w -i ./img/favicon.ico -n 班寄管理 --contents-directory . --add-data "audio;audio" --add-data "img;img" --add-data "ui;ui" --add-data "src;src" --add-data "ui;ui" --add-data "src;src" --add-data "LICENSE;." --add-data "utils;utils" --hidden-import PyQt6.QtWebEngine --exclude PyQt5 --exclude PyQt6
pause