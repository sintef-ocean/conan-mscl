@echo off
echo -----------------------------------------------------------------
echo BUILDING CONAN PACKAGE FOR MSCL
echo -----------------------------------------------------------------

REM Removing possible packages
conan remove MSCL -f

set name=sintef/testing
cd %~dp0

rmdir test_package\build
conan create . %name% -s build_type=Debug -o:b multi_core=True
rmdir test_package\build
conan create . %name% -s build_type=Release -o:b multi_core=True
