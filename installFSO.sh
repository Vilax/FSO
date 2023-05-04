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
pip install matplotlib

# Editing paths
INITFILE="config.ini"
rm ${INITFILE}
XMIPP_PATH="/xmipp-lite/build"
SEARCH_PATH=$HOME/.local
CHIMERA_PATH=$(find ${SEARCH_PATH} -name "chimera" | grep bin)

echo "[EXTERNAL_PROGRAMS]" >> $INITFILE
echo "XMIPP_PATH = ${PWD}${XMIPP_PATH}" >> $INITFILE
echo "CHIMERA_PATH = ${CHIMERA_PATH}" >> $INITFILE

EXECUTABLEFILE="FSO"
echo "cd $(pwd)" >> $EXECUTABLEFILE
echo "$(pwd)/Occupancy.py" >> $EXECUTABLEFILE
chmod +x ${EXECUTABLEFILE}


















