@echo off
setlocal enabledelayedexpansion
title Sky·光遇 电脑版目录选择
color 3f


:menu
cls
echo ╔═══════════════════════════════════════════════════════════════════╗
echo ║                                                                   ║
echo ║                      Sky·光遇 电脑版目录选择                      ║
echo ║                                                                   ║
echo ╠═══════════════════════════════════════════════════════════════════╣
echo ║                                                                   ║
echo ║                  [1] 打开 光遇截图(images) 目录                   ║
echo ║                                                                   ║
echo ║                  [2] 打开 光遇录屏(Record) 目录                   ║
echo ║                                                                   ║
echo ║                  [3] 同时打开录屏和截图两个目录                   ║
echo ║                                                                   ║
echo ║                  [4] 退出                                         ║
echo ║                                                                   ║
echo ╠═══════════════════════════════════════════════════════════════════╣
echo ║                                                                   ║
echo ║                                              Powered By 星川尘心  ║
echo ╚═══════════════════════════════════════════════════════════════════╝
echo.
set /p choice=请输入选项数字（1-4）：
if "%choice%"=="1" (
    start "" "%appdata%\ThatGameCompany\com.netease.sky\images"
    goto :eof
)
if "%choice%"=="2" (
    start "" "%appdata%\ThatGameCompany\com.netease.sky\Record"
    goto :eof
)
if "%choice%"=="3" (
    start "" "%appdata%\ThatGameCompany\com.netease.sky\images"
    start "" "%appdata%\ThatGameCompany\com.netease.sky\Record"
    goto :eof
)
if "%choice%"=="4" (
    exit
)

echo 无效输入，请按任意键重新选择...
pause >nul
goto menu