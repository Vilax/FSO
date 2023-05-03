# FourierShellOccupancy

The Fourier Shell Occupancy (FSO) algorithm measures the Global resolution anisotropy for cryo-EM maps, determining the quality of the map as well as infere if the particle distribution used to reconstruct the map is compatible with the resolution distributionvia directional FSC.

For a detailed information about the algorithm see our manuscript https://www.researchsquare.com/article/rs-1585291/v1

# Required Dependencies

Be sure you have the next dependencies in your system:
```
sudo apt-get -y install libsqlite3-dev libfftw3-dev default-jdk libtiff5-dev libhdf5-dev libopencv-dev python3-dev python3-numpy python3-scipy python3-mpi4py
```

# How to use it

There are two independent ways of using this algorithm:

* Inside Scipion (recommended) - Requires Scipion
* As Stand-alone application - Nothing is required


## Stand-alone installation

Fourier Shell Occupancy uses a enviroment to do not interfer with the system that each user can have:

1) Download the Fourier Shell Occupancy using next command
```git clone https://github.com/Vilax/FSO.git```
Git is neccesary to execute this command, if an error related to it appears, then install git `sudo apt install git`
2) Run the installation script
```source installFSO.sh```
3) Execute the software go to the software folder and run
```./FSO```


## Using in Scipion

Before using the algoritm, Scipion needs to be installed. To do that, see Scipion installation instructions in the [Scipion Official web site](http://scipion.i2pc.es/).

Once Scipipion have been installed, the Xmipp package is required, but it can be easily installed in the [plugin manager](https://scipion-em.github.io/docs/docs/user/plugin-manager.html#plugin-manager) inside Scipion.
Then, the algorithm will be available to be used in Scipion. You can find the algorithm searching by `Ctrl+F`, or in the left lateral panel, in `3D->Analysis->Resolution->Xmipp - Forioer Shell Occupancy`




