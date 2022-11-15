@echo off

title Toolbox

cd C:\Repos\Toolbox

echo.
echo                     **************************************
echo                     *                                    *
echo                     *      List of all manual tasks      *
echo                     *                                    *
echo                     **************************************
echo.
echo                     1. Check softwares version
echo                     2. Sync backup folders with targets
echo                     3. Collect MSYS2 packages info
echo                     4. Stitch images
echo                     5. Get codebase details
echo.

set /p option= Enter your option (any other to exit): 
echo.

goto option-%option%

:option-1

python softwares-version.py
goto EOF

:option-2

python backup-sync.py
goto EOF

:option-3

python packages-info.py
goto EOF

:option-4

python img-stitch.py
goto EOF

:option-5

python codebase-details.py
goto EOF

:EOF
echo:
pause
exit
