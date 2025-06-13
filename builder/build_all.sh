python3 -m pip install --user virtualenv
python3 -m venv --upgrade-deps venv
source ../venv/bin/activate
./venv/bin/python3 -m pip install --upgrade pip
./venv/bin/python3 -m pip install -r requirements.txt
./venv/bin/python3 -m pip install ../database/
./venv/bin/python3 -m pip install ../keybords/
./venv/bin/python3 -m pip install ../handlers/
./venv/bin/python3 -m pip install ../calendar_tg/