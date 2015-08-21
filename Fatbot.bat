@echo off
:run
python main.py fatcore.cfg fatmod.cfg gui
echo -------------------------------------
echo Any key to run again, CTRL+C to exit.
pause
goto run