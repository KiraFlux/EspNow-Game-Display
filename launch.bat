@echo off
setlocal enabledelayedexpansion

:: Установка PYTHONPATH
set "PYTHONPATH=src;"

:: Добавляем все библиотеки из папки lib
for /D %%d in ("lib\*") do (
    set "PYTHONPATH=!PYTHONPATH!;%%~d"
)

:: Запуск основного скрипта
py src/launch.py

endlocal
pause