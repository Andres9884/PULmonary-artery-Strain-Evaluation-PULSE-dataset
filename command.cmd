@echo off
set "input_folder=E:\TEST\"
set "output_folder=E:\RESULTS\"
set "mapdl_path=MAPDL.exe"

for %%f in ("%input_folder%\*.in") do (
    "%mapdl_path%" -i "%%f" -o "E:\test.out" -b nolist -j "TRASH" -dir "%output_folder%"
    if errorlevel 1 (
        echo Error procesando %%~nxf
    ) else (
        echo Procesado exitoso: %%~nxf
    )
    del /f /q "%output_folder%\*TRASH*"
)

