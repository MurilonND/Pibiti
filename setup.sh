#!/bin/bash
echo "Installing virtualenv..."
pip3 install virtualenv
echo "Creating a virtualenv..."
python3 -m venv env
echo "Openning the virtualenv..."
source env/bin/activate
echo "Installing dependencies..."
python3 -c "import monai"
pip3 install -qU "monai[ignite, nibabel, torchvision, tqdm, fire]==1.1.0"
pip3 install -r requirements.txt