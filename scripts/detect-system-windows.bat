@echo off
setlocal enabledelayedexpansion

REM Enhanced Windows System Detection Script
REM Collects comprehensive system information for AI analysis

echo {

REM Basic system information
for /f "tokens=2 delims==" %%i in ('wmic os get localdatetime /value ^| find "="') do set datetime=%%i
set timestamp=!datetime:~0,4!-!datetime:~4,2!-!datetime:~6,2!T!datetime:~8,2!:!datetime:~10,2!:!datetime:~12,2!
echo   "timestamp": "!timestamp!",
echo   "platform": "win32",

REM Windows system information using systeminfo
echo   "os_release": {
for /f "tokens=2 delims=:" %%i in ('systeminfo ^| find "OS Name"') do (
    set osname=%%i
    set osname=!osname:~1!
    echo     "PRETTY_NAME": "!osname!",
    echo     "NAME": "!osname!",
)
for /f "tokens=2 delims=:" %%i in ('systeminfo ^| find "OS Version"') do (
    set osversion=%%i
    set osversion=!osversion:~1!
    echo     "VERSION": "!osversion!",
)
echo     "ID": "windows"
echo   },

REM System information
echo   "system": {
echo     "hostname": "%COMPUTERNAME%",
for /f "tokens=2 delims=:" %%i in ('systeminfo ^| find "System Type"') do (
    set arch=%%i
    set arch=!arch:~1!
    echo     "architecture": "!arch!",
)
echo     "shell": "%COMSPEC%",
echo     "user": "%USERNAME%",
echo     "home": "%USERPROFILE%"
echo   },

REM Hardware information
echo   "hardware": {
for /f "tokens=2 delims=:" %%i in ('systeminfo ^| find "Processor(s)"') do (
    set cpu=%%i
    set cpu=!cpu:~1!
    echo     "cpu_model": "!cpu!",
)
for /f "tokens=2 delims=:" %%i in ('systeminfo ^| find "Total Physical Memory"') do (
    set memory=%%i
    set memory=!memory:~1!
    echo     "memory_total": "!memory!",
)
echo     "disk_usage": "unknown"
echo   },

REM Package managers detection
echo   "package_managers": {
set first=true
set managers=winget choco scoop npm pip
for %%m in (!managers!) do (
    if !first!==false echo ,
    set first=false
    where %%m >nul 2>&1
    if !errorlevel!==0 (
        echo     "%%m": {"available": true, "version": "unknown"}
    ) else (
        echo     "%%m": {"available": false}
    )
)
echo   },

REM Development tools
echo   "development_tools": {
set first=true
set tools=git node npm python pip docker curl wget code
for %%t in (!tools!) do (
    if !first!==false echo ,
    set first=false
    where %%t >nul 2>&1
    if !errorlevel!==0 (
        echo     "%%t": {"available": true, "version": "installed"}
    ) else (
        echo     "%%t": {"available": false}
    )
)
echo   },

REM Network information
echo   "network": {
echo     "hostname_fqdn": "%COMPUTERNAME%",
for /f "tokens=2 delims=:" %%i in ('ipconfig ^| find "IPv4 Address"') do (
    set ip=%%i
    set ip=!ip:~1!
    echo     "ip_address": "!ip!",
    goto :found_ip
)
:found_ip
ping 8.8.8.8 -n 1 >nul 2>&1
if !errorlevel!==0 (
    echo     "internet_connection": true
) else (
    echo     "internet_connection": false
)
echo   },

REM Windows-specific information
echo   "distribution": {
echo     "family": "windows",
for /f "tokens=2 delims=:" %%i in ('systeminfo ^| find "OS Version"') do (
    set version=%%i
    set version=!version:~1!
    echo     "version": "!version!",
)
where winget >nul 2>&1
if !errorlevel!==0 (
    echo     "primary_package_manager": "winget"
) else (
    where choco >nul 2>&1
    if !errorlevel!==0 (
        echo     "primary_package_manager": "choco"
    ) else (
        echo     "primary_package_manager": "none"
    )
)
echo   }

echo }