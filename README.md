# FourierOccupancyShell

The Fourier Occupancy Shell algorithm measures the Global resolution anisotropy for cryo-EM maps, determining the quality of the map as well as infere if the particle distribution used to reconstruct the map is compatible with the resolution distributionvia directional FSC.

For a detailed information about the algorithm see our manuscript SETLINK TO MANUSCRIPT

# Installation

There are two independent ways of using/install this algorithm:

* Stand-alone installation - Nothind is required
* As a Xmipp protocol inside Scipion - Requires Scipion (encouraged)

## Stand-alone installation

The most simple manner is to install The Fourier Shell Occupancy algorithm via pip.

Download the Fourier Occupancy Shell GUI an dall its dependencies
1) `pip install fouriershell`
Install Xmipp-light with the Fourier Occupancy Shell algorithm using
2) `source install.sh`

If for any reason this installation fails you can also do a manual installation (however, you will need to install all required dependencies manually, following next steps

1) Download the FourierShell Occupancy Graphical Interface
`git clone https://github.com/Vilax/FourierOccupancyShell.git`
2) Download Xmipp-light
`https://github.com/Vilax/xmipp-light.git`
3) Compile Xmipp-light
`chmod +x xmipp`
`./xmipp`

Once the Fourier Occupancy Shell is installed you will be able to run it by executing the file
`FourierOccupancyShell`


## Using in Scipion

Before use the algoritm, Scipion needs to be installed. To do that see, Scipion installation instructions in the [Scipion Official web site](http://scipion.i2pc.es/).

Once Scipipion have been installed, the Xmipp package is required, but it can be easily installed in the [plugin manager](https://scipion-em.github.io/docs/docs/user/plugin-manager.html#plugin-manager) inside Scipion.
Then, the algorithm will be available to be used in Scipion. You can find the algorithm searching by `Ctrl+F`, or in the left lateral panel, in `3D->Analysis->Resolution->Xmipp - Forioer Occupancy Shell`


