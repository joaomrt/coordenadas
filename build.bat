pyinstaller coordenadas.py -i icone.ico --noconsole
copy icone.ico dist\coordenadas\
xcopy settings.ini dist\coordenadas\
mkdir dist\coordenadas\ficheiros
xcopy /y ficheiros dist\coordenadas\ficheiros\
rmdir /s /q dist\coordenadas\tcl\tzdata
del /q dist\coordenadas\pyproj\data\alaska
del /q dist\coordenadas\pyproj\data\hawaii
del /q dist\coordenadas\pyproj\data\ntv1_can.dat
del /q dist\coordenadas\pyproj\data\conus
del coordenadas.spec
rmdir /s /q build
rmdir /s /q __pycache__
