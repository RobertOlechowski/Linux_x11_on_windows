rem @echo off
cls
set python_exe="D:\bin\Python36_64\python.exe"
set ssh_key="D:/Archiwum/Klucze/cnc/openSSH.priv"
set DISPLAY=127.0.0.1:0

%python_exe% scripts/run_x11.py -a 192.168.10.225 -k %ssh_key% -u cnc -c "xterm"
