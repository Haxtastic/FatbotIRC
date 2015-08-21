@echo off
:run
python main.py slimcore.cfg slimmod.cfg gui
echo -------------------------------------
echo Any key to run again, CTRL+C to exit.
pause
goto run