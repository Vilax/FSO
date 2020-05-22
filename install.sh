#!/bin/bash

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
sudo apt-get install python3-venv
python3 -m venv FSO
source FSO/bin/activate
pip install pyqt5
pip install matplotlib

echo " "
echo " "
echo "Downloading Fourier Shell Occupancy..."
git clone https://github.com/Vilax/FourierShellOccupancy.git








