pyinstaller -n PySysLogQt --onefile --windowed \
  --add-data ./vendor:vendor/ \
  __main__.py
