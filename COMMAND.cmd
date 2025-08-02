@echo off
set "input_folder=C:\Users\investigacion\Desktop\INFILEs\" :: Replace with you .in file location
set "output_folder=C:\Users\investigacion\Desktop\INFILEs\" :: Replace with your simluation result destination
set "mapdl_path=MAPDL.exe" :: You should have mapdl as an enviroment variable

for %%f in ("%input_folder%\*.in") do (
    "%mapdl_path%" -i "%%f" -o "E:\test.out" -b nolist -j "TRASH" -dir "%output_folder%" :: Create a .out file an replace its location
    ren "%output_folder%\TRASH.rst" "%%~nf.rst"
    del /f /q "%output_folder%\*TRASH*"
    echo Succesfull process: %%~nxf
)

