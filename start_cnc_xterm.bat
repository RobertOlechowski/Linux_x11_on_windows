@echo off
cls
call scripts/common_bat

%python_exe% scripts/run_x11.py -a 192.168.10.225 -k %ssh_key% -u cnc -c "xterm"
if %ERRORLEVEL% == 0 goto :exit

echo.
pause

:exit