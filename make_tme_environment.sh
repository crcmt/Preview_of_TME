#!/usr/bin/env bash
set -e

VENV_NAME="TME_MFP_env"
VENV_PATH="/opt/$VENV_NAME"

if [ -d "$VENV_PATH" ]
then
    echo "Directory $VENV_PATH already exist."
    echo "If you want to reinstall environment, execute the commands below and then restart script:"
    echo "rm -rf $VENV_PATH" | tr '[:upper:]' '[:lower:]'
    exit 1
fi

echo "Create new virtual environment with name: '$VENV_NAME'"
/usr/bin/python3 -m venv $VENV_PATH

echo "Enter virtual environment"
source $VENV_PATH/bin/activate

echo "Install packages"
pip install --upgrade pip wheel --no-cache-dir
pip install -r requirements.txt --no-cache-dir

#echo "Create jupyter kernel with name $VENV_NAME" | tr '[:upper:]' '[:lower:]'
#python -m ipykernel install --user --name="$VENV_NAME" 
