@DEL /S *.pyc 2> nul
@DEL /S *.egg-info 2> nul
@RMDIR /S /Q build dist .cache 2> nul
