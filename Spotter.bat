@echo off
echo checking internet connection
Ping www.google.nl -n 1 -w 1000
cls
if errorlevel 1 (goto :Start_Spotter) else (goto :Update_Spotter)

:Update_Spotter
echo Updating Spotter
rem git pull origin master

cd %~dp0/lib/ui/
call build_windows.bat
cd ../..
goto :Start_Spotter

:Start_Spotter
echo starting Spotter
python spotterQt.py