@echo off
REM sva — sme-vital-agents launcher
REM Usage: sva optiqos
REM        sva --list
REM        sva optiqos --model opus
python "%~dp0launch.py" %*
