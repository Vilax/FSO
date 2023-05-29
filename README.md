# FourierShellOccupancy

The Fourier Shell Occupancy (FSO) algorithm measures the Global resolution anisotropy for cryo-EM maps, determining the quality of the map as well as infere if the particle distribution used to reconstruct the map is compatible with the resolution distributionvia directional FSC.

For a detailed information about the algorithm see our [article](https://doi.org/10.1038/s41592-023-01874-3). 

# How to use it

There are two independent ways of using this algorithm:

* Inside Scipion (recommended): This version is much faster than the standalone version. The code is updated and provides mucho more visualization tools
* As Stand-alone application: It is slow but it does not require anything else

For shake of simplicity we encourage to use the FSO inside Scipion. 

## FSO in Scipion

Before using the algorithm, Scipion needs to be installed. To do that, see Scipion installation instructions in the [Scipion Official web site](http://scipion.i2pc.es/).

Once Scipipion have been installed, the Xmipp package is required, but it can be easily installed in the [plugin manager](https://scipion-em.github.io/docs/docs/user/plugin-manager.html#plugin-manager) inside Scipion.
Then, the algorithm will be available to be used in Scipion. You can find the algorithm searching by `Ctrl+F`, `xmipp - resolution fso`

# Stand-alone version

To use the stand alone version, you only need to clone this repository and execute the installer

1) Cloning the repository

```
git clone https://github.com/Vilax/FSO

```
2) Installing the software. This step creates a virtual environment and install: numpy, mrcfile, matplotlib and pyqt

```
source installFSO.sh
```

3) Execute FSO or ```python3 fso.py```

Any comment please contact us, visit the article to find our email

# Reference :

[J.L. Vilas, H.D. Tagare, New measures of anisotropy of cryo-EM maps, Nature Methods (2023)](https://doi.org/10.1038/s41592-023-01874-3)










