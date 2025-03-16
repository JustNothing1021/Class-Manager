@echo off
chcp 936 >nul
setlocal enabledelayedexpansion
title ClassManager_Action����
cd /d "%~dp0"

set "DEFAULT_COMPILER=1"
set "COMPILER_CMD=pyinstaller"
set "COMPILER_NAME=PyInstaller"

if not exist "compile.conf" (
    call :first_run_config
)

for /f "tokens=1,2 delims==" %%a in (compile.conf) do set "%%a=%%b"

if "%create_venv%"=="1" set "install_requirements=1"

if "%compiler%"=="1" (
    set "COMPILER_CMD=pyinstaller"
    set "COMPILER_NAME=PyInstaller"
) else if "%compiler%"=="2" (
    set "COMPILER_CMD=nuitka"
    set "COMPILER_NAME=Nuitka"
)

:main_menu
cls
echo ===================================
echo      ClassManager ���� v2.2
echo        ��ǰ��������!COMPILER_NAME!
echo ===================================
echo [��ǰ����]
call :show_config create_venv       "�������⻷��"
call :show_config install_requirements "��װ����"
call :show_config show_process      "��ʾ������"
call :show_config build_zip         "���ɷ��а�"
echo ===================================
set /p "modify=����M�޸����ã���������ʼ���룺"
if /i "%modify%"=="M" call :modify_config

call :check_dependencies || exit /b 1

if not exist "ClassManager\Compile" (
    md "ClassManager\Compile" 2>nul || (
        echo �޷���������Ŀ¼
        pause
        exit /b 1
    )
)
if "%create_venv%"=="1" (
    echo ���ڳ�ʼ�����⻷��...
    rd /s /q .venv 2>nul
    python -m venv .venv || (
        echo ���⻷������ʧ��
        pause
        exit /b 1
    )
    call .venv\Scripts\activate
    set "install_requirements=1"  :: ǿ�ư�װ����
)

if "%install_requirements%"=="1" (
    echo ���ڰ�װ��������...
    if "%show_process%"=="1" (
        python -m pip install -r requirements.txt --progress-bar pretty
    ) else (
        python -m pip install -r requirements.txt -q
    )
    python -m pip install pillow >nul
    echo ���ڰ�װ!COMPILER_NAME!...
    if "%COMPILER_CMD%"=="nuitka" (
        python -m pip install nuitka >nul
    ) else (
        python -m pip install pyinstaller >nul
    )
)

call :generate_output_path

if "%COMPILER_CMD%"=="pyinstaller" (
    call :pyinstaller_compile
) else (
    call :nuitka_compile
)

if "%build_zip%"=="1" (
    call :package_release
) else (
    echo ��������ѱ�������!OUTPUT_PATH!
)

echo.
echo ===== ��������� =====
pause
exit /b

:first_run_config
cls
echo ===== �״��������� =====
echo ��������³�ʼ�����ã�
echo.
choice /c 12 /n /m "ѡ������� (1.PyInstaller 2.Nuitka): "
set "compiler=!errorlevel!"
echo.
set /p "create_venv=�������⻷�� (1=��/0=��): "
set /p "show_process=��ʾ������ (1=��/0=��): "
set /p "build_zip=���ɷ��а� (1=��/0=��): "

:: �Զ�����������װ
if "%create_venv%"=="1" set "install_requirements=1"

(echo compiler=%compiler%
 echo create_venv=%create_venv%
 echo install_requirements=%install_requirements%
 echo show_process=%show_process%
 echo build_zip=%build_zip%) > compile.conf
exit /b

:modify_config
cls
echo ===== �޸����� =====
echo ��ǰ��������!COMPILER_NAME!
echo.
choice /c 12 /n /m "ѡ������� (1.PyInstaller 2.Nuitka): "
set "compiler=!errorlevel!"
echo.
set /p "create_venv=�������⻷�� (1=��/0=��): "
set /p "show_process=��ʾ������ (1=��/0=��): "
set /p "build_zip=���ɷ��а� (1=��/0=��): "

if "%create_venv%"=="1" set "install_requirements=1"

(echo compiler=%compiler%
 echo create_venv=%create_venv%
 echo install_requirements=%install_requirements%
 echo show_process=%show_process%
 echo build_zip=%build_zip%) > compile.conf
echo �����Ѹ��£�
timeout /t 2 >nul
goto :main_menu

:show_config
setlocal
set "flag=[ ]"
if "!%~1!"=="1" set "flag=[?]"
echo %flag% %~2
endlocal
exit /b

:check_dependencies
python --version >nul 2>&1 || (
    echo ����Python����δ��ȷ����
    echo ��ȷ�ϣ�
    echo 1. �Ѱ�װPython 3.8+
    echo 2. �������ϵͳPATH
    pause
    exit /b 1
)
exit /b 0

:generate_output_path
for /f "tokens=2 delims==" %%a in ('wmic os get localdatetime /value') do set "datetime=%%a"
set "date_suffix=%datetime:~2,6%"
set "OUTPUT_PATH=dist\main"
if "%build_zip%"=="0" set "OUTPUT_PATH=dist\main_%date_suffix%"

if exist "!OUTPUT_PATH!" (
    choice /m "Ŀ¼!OUTPUT_PATH!�Ѵ��ڣ��Ƿ񸲸ǣ�(Y����/Nȡ��)"
    if errorlevel 2 exit /b 1
    rd /s /q "!OUTPUT_PATH!" 2>nul
)
if exist "img\favicon.ico" (
    echo ������֤ͼ���ļ�...
    python -c "from PIL import Image; img = Image.open('img/favicon.ico'); img.verify()" || (
        echo ����ͼ���ļ��𻵻��ʽ����ȷ
        pause
        exit /b 1
    )
) else (
    echo ����ͼ���ļ���������imgĿ¼
    pause
    exit /b 1
)
exit /b

:pyinstaller_compile
echo ����ʹ��PyInstaller����...
set "cmd=pyinstaller main.py -w --icon "img/favicon.ico" -n "main" --contents-directory . --add-data "audio;audio" --add-data "img;img" --add-data "ui;ui" --add-data "utils;utils" --add-data "LICENSE;." --add-data "src;src" --add-data "version;." --hidden-import PyQt6.QtWebEngine --exclude-module PyQt5 --exclude-module PyQt6 --distpath "dist" --workpath "build" --noconfirm"

set "cmd=!cmd! --exclude-module _bootlocale"
if "%show_process%"=="0" set "cmd=!cmd! >nul 2>&1"
cmd /c "!cmd!" || (
    echo PyInstaller����ʧ��
    pause
    exit /b 1
)
exit /b

:nuitka_compile
echo ����ʹ��Nuitka����(��)...
set "cmd=python -m nuitka --mingw64 --windows-icon=img/favicon.ico --output-dir=dist --remove-output --enable-plugin=pyqt6 --include-data-dir=audio=audio --include-data-dir=img=img --include-data-dir=ui=ui --include-data-dir=utils=utils --include-data-dir=src=src --include-data-dir=version=version --include-data-file=LICENSE=LICENSE --windows-disable-console --follow-imports main.py"

if "%show_process%"=="0" set "cmd=!cmd! >nul 2>&1"
cmd /c "!cmd!" || (
    echo Nuitka����ʧ��
    pause
    exit /b 1
)

if exist "dist\main.dist" (
    ren "dist\main.dist" "main"
    move "dist\main" "!OUTPUT_PATH!" >nul
)
exit /b

:package_release
echo �������ɷ��а�...
if not exist "ClassManager\Compile" md "ClassManager\Compile"
set "temp_dir=ClassManager\Compile\temp"
rd /s /q "%temp_dir%" 2>nul
md "%temp_dir%"
xcopy /E /Y "!OUTPUT_PATH!\*" "%temp_dir%\" >nul
powershell -Command "$date=(Get-Date -Format 'yyyyMMdd'); $zipPath='ClassManager\Compile\main_'+$date+'.zip'; Compress-Archive -Path '%temp_dir%' -DestinationPath $zipPath -Force"
rd /s /q "%temp_dir%"
if exist "ClassManager\Compile\main_*.zip" (
    echo ���а������ɣ�ClassManager\Compile\main_%date%.zip
    rd /s /q dist build 2>nul
) else (
    echo ѹ��������ʧ��
)
exit /b