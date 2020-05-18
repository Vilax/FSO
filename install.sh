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
echo "Downloading Fourier Shell Occupancy..."
git clone https://github.com/Vilax/FourierOccupancyShell.git




