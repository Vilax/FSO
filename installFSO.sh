#!/bin/sh

# This script download all programs requires to run the Fourier Shell Occupancy algorithm

# The first step is to download Xmipp-lite and compile it (Xmipp lite is a xmipp version without CUDA, python, just resolution related algorithms)

echo "Cloning xmipp-lite repository..."
git clone https://github.com/Vilax/xmipp-lite.git

echo " "
echo " "
echo "Compiling xmipp-lite..."
echo " "

cd xmipp-lite
chmod +x xmipp
./xmipp
cd ..

echo " "
echo " "
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









