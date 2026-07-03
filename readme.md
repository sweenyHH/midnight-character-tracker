########### Requirements: ###########

pytest
PySide6
watchdog

########### On Widnows WSL - Ubunto I needed to do the following: ###########

python3 -m venv venv

source venv/bin/activate


...before I was able to:

pip install -r requirements.txt


To allow execution of run_tests.sh:

chmod +x run_tests.sh

