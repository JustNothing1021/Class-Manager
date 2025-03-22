:: Use GB2312 AND CRLF
:: Commit by CRLF, not LF
@echo off
chcp 936 >nul
setlocal enabledelayedexpansion
title ClassManager_编译
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
echo      ClassManager 编译 v2.2
echo        当前编译器：!COMPILER_NAME!
echo ===================================
echo [当前配置]
call :show_config create_venv       "创建虚拟环境"
call :show_config install_requirements "安装依赖"
call :show_config show_process      "显示进度条"
call :show_config build_zip         "生成发行包"
echo ===================================
set /p "modify=输入M修改配置，其他键开始编译："
if /i "%modify%"=="M" call :modify_config

call :check_dependencies || exit /b 1

if not exist "ClassManager\Compile" (
    md "ClassManager\Compile" 2>nul || (
        echo 无法创建编译目录
        pause
        exit /b 1
    )
)
if "%create_venv%"=="1" (
    echo 正在初始化虚拟环境...
    rd /s /q .venv 2>nul
    python -m venv .venv || (
        echo 虚拟环境创建失败
        pause
        exit /b 1
    )
    call .venv\Scripts\activate
    set "install_requirements=1"  :: 强制安装依赖
)

if "%install_requirements%"=="1" (
    echo 正在安装基础依赖...
    if "%show_process%"=="1" (
        python -m pip install -r requirements.txt --progress-bar pretty
    ) else (
        python -m pip install -r requirements.txt -q
    )
    python -m pip install pillow >nul
    echo 正在安装!COMPILER_NAME!...
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
    echo 编译输出已保存至：!OUTPUT_PATH!
)

echo.
echo ===== 操作已完成 =====
pause
exit /b

:first_run_config
cls
echo ===== 首次运行配置 =====
echo 请完成以下初始化配置：
echo.
choice /c 12 /n /m "选择编译器 (1.PyInstaller 2.Nuitka): "
set "compiler=!errorlevel!"
echo.
set /p "create_venv=创建虚拟环境 (1=是/0=否): "
set /p "show_process=显示进度条 (1=是/0=否): "
set /p "build_zip=生成发行包 (1=是/0=否): "

:: 自动设置依赖安装
if "%create_venv%"=="1" set "install_requirements=1"

(echo compiler=%compiler%
 echo create_venv=%create_venv%
 echo install_requirements=%install_requirements%
 echo show_process=%show_process%
 echo build_zip=%build_zip%) > compile.conf
exit /b

:modify_config
cls
echo ===== 修改配置 =====
echo 当前编译器：!COMPILER_NAME!
echo.
choice /c 12 /n /m "选择编译器 (1.PyInstaller 2.Nuitka): "
set "compiler=!errorlevel!"
echo.
set /p "create_venv=创建虚拟环境 (1=是/0=否): "
set /p "show_process=显示进度条 (1=是/0=否): "
set /p "build_zip=生成发行包 (1=是/0=否): "

if "%create_venv%"=="1" set "install_requirements=1"

(echo compiler=%compiler%
 echo create_venv=%create_venv%
 echo install_requirements=%install_requirements%
 echo show_process=%show_process%
 echo build_zip=%build_zip%) > compile.conf
echo 配置已更新！
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
    echo 错误：Python环境未正确配置
    echo 请确认：
    echo 1. 已安装Python 3.8+
    echo 2. 已添加至系统PATH
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
    choice /m "目录!OUTPUT_PATH!已存在，是否覆盖？(Y覆盖/N取消)"
    if errorlevel 2 exit /b 1
    rd /s /q "!OUTPUT_PATH!" 2>nul
)
if exist "img\favicon.ico" (
    echo 正在验证图标文件...
    python -c "from PIL import Image; img = Image.open('img/favicon.ico'); img.verify()" || (
        echo 错误：图标文件损坏或格式不正确
        pause
        exit /b 1
    )
) else (
    echo 错误：图标文件不存在于img目录
    pause
    exit /b 1
)
exit /b

:pyinstaller_compile
echo 正在使用PyInstaller编译...
set "cmd=pyinstaller main.py -w --icon "img/favicon.ico" -n "main" --contents-directory . --add-data "audio;audio" --add-data "img;img" --add-data "ui;ui" --add-data "utils;utils" --add-data "LICENSE;." --add-data "src;src" --add-data "version;." --hidden-import PyQt6.QtWebEngine --exclude-module PyQt5 --exclude-module PyQt6 --distpath "dist" --workpath "build" --noconfirm"

set "cmd=!cmd! --exclude-module _bootlocale"
if "%show_process%"=="0" set "cmd=!cmd! >nul 2>&1"
cmd /c "!cmd!" || (
    echo PyInstaller编译失败
    pause
    exit /b 1
)
exit /b

:nuitka_compile
echo 正在使用Nuitka编译(慢)...
set "cmd=python -m nuitka --mingw64 --windows-icon=img/favicon.ico --output-dir=dist --remove-output --enable-plugin=pyqt6 --include-data-dir=audio=audio --include-data-dir=img=img --include-data-dir=ui=ui --include-data-dir=utils=utils --include-data-dir=src=src --include-data-dir=version=version --include-data-file=LICENSE=LICENSE --windows-disable-console --follow-imports main.py"

if "%show_process%"=="0" set "cmd=!cmd! >nul 2>&1"
cmd /c "!cmd!" || (
    echo Nuitka编译失败
    pause
    exit /b 1
)

if exist "dist\main.dist" (
    ren "dist\main.dist" "main"
    move "dist\main" "!OUTPUT_PATH!" >nul
)
exit /b

:package_release
echo 正在生成发行包...
if not exist "ClassManager\Compile" md "ClassManager\Compile"
set "temp_dir=ClassManager\Compile\temp"
rd /s /q "%temp_dir%" 2>nul
md "%temp_dir%"
xcopy /E /Y "!OUTPUT_PATH!\*" "%temp_dir%\" >nul
powershell -Command "$date=(Get-Date -Format 'yyyyMMdd'); $zipPath='ClassManager\Compile\main_'+$date+'.zip'; Compress-Archive -Path '%temp_dir%' -DestinationPath $zipPath -Force"
rd /s /q "%temp_dir%"
if exist "ClassManager\Compile\main_*.zip" (
    echo 发行包已生成：ClassManager\Compile\main_%date%.zip
    rd /s /q dist build 2>nul
) else (
    echo 压缩包生成失败
)
exit /b