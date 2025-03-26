@echo off
REM Check if the virtual environment folder "venv" exists; if not, create it.
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate the virtual environment.
echo Activating virtual environment...
call venv\Scripts\activate

REM Upgrade pip.
echo Upgrading pip...
pip install --upgrade pip

REM Install requirements if the file exists.
if exist requirements.txt (
    echo Installing packages from requirements.txt...
    pip install -r requirements.txt
) else (
    echo No requirements.txt found. Skipping package installation.
)

REM Keep the command prompt open with the virtual environment active.
cmd /K
