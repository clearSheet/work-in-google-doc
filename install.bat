color 2
curl "https://www.python.org/ftp/python/3.10.5/python-3.10.5-amd64.exe" --output python.exe
python.exe /passive InstallAllUsers=1 PrependPath=1 Include_test=0 SimpleInstall=1
DEL /F /A python.exe
python -m pip install --upgrade pip
python3 -m venv venv
pip install -r requirements.txt

