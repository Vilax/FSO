# FourierShellOccupancy

The Fourier Shell Occupancy (FSO) algorithm measures the Global resolution anisotropy for cryo-EM maps, determining the quality of the map as well as infere if the particle distribution used to reconstruct the map is compatible with the resolution distributionvia directional FSC.

For a detailed information about the algorithm see our manuscript SETLINK TO MANUSCRIPT

# Installation

There are two independent ways of using/install this algorithm:

* Stand-alone installation - Nothind is required
* As a Xmipp protocol inside Scipion - Requires Scipion (encouraged)

## Stand-alone installation

Fourier Shell Occupancy uses a conda enviroment to do not interfer with the system that each user can have. Thus, the first step is to create a conda enviroment:

1) Creation of the conda enviaroment
1.1) Install anaconda Python 3x version from https://www.anaconda.com/distribution/
1.2) Create an enviroment for Fourier Shell Occupancy algorithm
    `conda create -n FourierShell python=3.7`
    If conda command does not work, a solution is to export the path `export PATH=~/anaconda3/bin:$PATH` or even better to create an alias in your .bashrc file.
1.3) Activate the conda enviroment
`conda activate FourierShell`
Note that every time you will want to use the Fourier Shell Occupancy, the command `conda activate FourierShell` will be required.


1) Download the Fourier Occupancy Shell GUI an dall its dependencies
 `https://github.com/Vilax/FourierOccupancyShell.git`
2) Install Xmipp-light with the Fourier Occupancy Shell algorithm and preparing the conda enviroment using (Anaconda or miniconda is required (Anaconda installation info [here](https://docs.anaconda.com/anaconda/install/))
`source install.sh`
3) Execute the software
`FourierShell`

If for any reason this installation fails you can also do a manual installation (however, you will need to install all required dependencies manually, following next steps

1) Download the FourierShell Occupancy Graphical Interface
`git clone https://github.com/Vilax/FourierOccupancyShell.git`
2) Download Xmipp-light
`https://github.com/Vilax/xmipp-light.git`
3) Compile Xmipp-light
`chmod +x xmipp; ./xmipp`
4) Create a conda enviroment
`conda create -n FourierShell`
5) Activate conda enviroment
`conda activate FourierShell`
6) Install dependencies in the conda enviroment
`conda install -c anaconda pyqt` and `conda install -c anaconda matplotlib` 
7) Execute the software
`FourierShell`

## Using in Scipion

Before use the algoritm, Scipion needs to be installed. To do that see, Scipion installation instructions in the [Scipion Official web site](http://scipion.i2pc.es/).

Once Scipipion have been installed, the Xmipp package is required, but it can be easily installed in the [plugin manager](https://scipion-em.github.io/docs/docs/user/plugin-manager.html#plugin-manager) inside Scipion.
Then, the algorithm will be available to be used in Scipion. You can find the algorithm searching by `Ctrl+F`, or in the left lateral panel, in `3D->Analysis->Resolution->Xmipp - Forioer Occupancy Shell`


