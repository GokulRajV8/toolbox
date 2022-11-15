@echo off
setlocal

rem Purpose : To use MSYS2 Git in VS code
rem Source  : https://github.com/microsoft/vscode/issues/4651

if "%1" equ "rev-parse" goto rev_parse
git %*
goto :eof
:rev_parse
for /f %%1 in ('git %*') do cygpath -w %%1
