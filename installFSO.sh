#!/bin/sh

# This script download all programs requires to run the Fourier Shell Occupancy algorithm

echo "Creating a virtual enviroment..."

ifvenv=$(pip list | grep virtualenv)
if [ "$ifvenv" != "*virtualenv*" ];
then
pip install virtualenv
fi

python3 -m venv env
. env/bin/activate
pip install --upgrade pip
pip install pyqt5
pip install numpy
pip install mrcfile
pip install matplotlib


EXECUTABLEFILE="FSO"
echo "cd $(pwd)" >> $EXECUTABLEFILE
echo "$(pwd)/fso.py" >> $EXECUTABLEFILE
chmod +x ${EXECUTABLEFILE}


















