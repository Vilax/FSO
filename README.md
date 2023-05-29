# FourierShellOccupancy

The Fourier Shell Occupancy (FSO) algorithm measures the Global resolution anisotropy for cryo-EM maps, determining the quality of the map as well as infere if the particle distribution used to reconstruct the map is compatible with the resolution distributionvia directional FSC.

For a detailed information about the algorithm see our manuscript https://www.researchsquare.com/article/rs-1585291/v1

# Important Note about use and installation

The stand-along version is under refactorization (May 29th 2023), it will be released during the following. Until this refactorization will be finished, the FSO can be used vía Scipion

# How to use it

There are two independent ways of using this algorithm:

* Inside Scipion (recommended)
* As Stand-alone application (Under refactorization)

For shake of simplicity we encourage to use the FSO inside Scipion. However, it is also possible to use the FSO as stand alone application.

## Using in Scipion

Before using the algorithm, Scipion needs to be installed. To do that, see Scipion installation instructions in the [Scipion Official web site](http://scipion.i2pc.es/).

Once Scipipion have been installed, the Xmipp package is required, but it can be easily installed in the [plugin manager](https://scipion-em.github.io/docs/docs/user/plugin-manager.html#plugin-manager) inside Scipion.
Then, the algorithm will be available to be used in Scipion. You can find the algorithm searching by `Ctrl+F`, or in the left lateral panel, in `3D->Analysis->Resolution->Xmipp - Fourier Shell Occupancy`






