chcp 65001
rem rmdir /s /q \venv
rmdir ..\venv
py -m pip install --user virtualenv
py -m venv --upgrade-deps ..\venv
.\venv\Scripts\python.exe -m pip install -r requirements.txt
.\venv\Scripts\python.exe -m pip install --upgrade pip
.\venv\Scripts\python.exe -m pip install ..\database\
