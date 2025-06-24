@echo off
chcp 65001 > nul
setlocal enabledelayedexpansion

:: 获取当前脚本目录
set "current_dir=%~dp0"

:: ============== 第一部分：数据库初始化 ==============
echo.
echo 正在进行MySQL数据库初始化...

:: 询问MySQL账户
set /p MYSQL_USER="请输入MySQL账户: "

:: 安全询问密码
set "psCommand=powershell -Command "$p=read-host '请输入MySQL密码' -AsSecureString; ^
    $BSTR=[System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($p); ^
    [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($BSTR)""
for /f "usebackq delims=" %%p in (`%psCommand%`) do set "MYSQL_PASSWORD=%%p"

:: 创建数据库
mysql -u%MYSQL_USER% -p%MYSQL_PASSWORD% -e "CREATE DATABASE IF NOT EXISTS realtime_voting;" --connect-timeout=3
if errorlevel 1 (
    echo 错误：数据库创建失败！请检查MySQL账户和密码
    pause
    exit /b 1
)

:: 执行init.sql
echo 正在初始化数据库结构...
mysql -u%MYSQL_USER% -p%MYSQL_PASSWORD% realtime_voting --connect-timeout=5 < "%current_dir%init.sql"
if errorlevel 1 (
    echo 错误：数据库初始化失败！请检查init.sql文件
    pause
    exit /b 1
)

:: 创建.env文件
echo 正在生成后端配置文件...
if not exist "%current_dir%backend\" mkdir "%current_dir%backend"
(
    echo MYSQL_HOST=localhost
    echo MYSQL_PORT=3306
    echo MYSQL_USER=%MYSQL_USER%
    echo MYSQL_PASSWORD=%MYSQL_PASSWORD%
    echo MYSQL_DB=realtime_voting
) > "%current_dir%backend\.env"

echo  数据库配置完成！

:: ============== 第二部分：Python环境设置 ==============
echo.
echo 正在设置Python后端环境...
pushd "%current_dir%backend"

:: 检查Python安装
where python > nul 2> nul
if %errorlevel% neq 0 (
    echo 错误：未检测到Python安装
    echo 请从 https://www.python.org/downloads/ 安装Python并添加到系统路径
    pause
    exit /b 1
)

:: 创建虚拟环境
echo 检查Python虚拟环境...
if not exist "venv\" (
    echo 正在创建虚拟环境...
    python -m venv venv
    if errorlevel 1 (
        echo 错误：虚拟环境创建失败
        popd
        pause
        exit /b 1
    )
) else (
    echo 虚拟环境已存在，跳过创建
)

:: 激活虚拟环境
call venv\Scripts\activate

:: 安装依赖
echo 正在安装Python依赖...
echo 使用阿里云镜像加速安装...
pip install --retries 3 --timeout 60 -i https://mirrors.aliyun.com/pypi/simple/ -r requirements.txt > pip_install.log 2>&1
if errorlevel 1 (
    echo 错误：依赖安装失败！请查看pip_install.log
    deactivate
    popd
    pause
    exit /b 1
)

:: ============== 完成 ==============
echo.
echo 所有配置已完成！
pause > nul

:: 清理环境变量
set MYSQL_USER=
set MYSQL_PASSWORD=
popd
endlocal