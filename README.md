# FourierShellOccupancy

The Fourier Shell Occupancy (FSO) algorithm measures the Global resolution anisotropy for cryo-EM maps, determining the quality of the map as well as infere if the particle distribution used to reconstruct the map is compatible with the resolution distributionvia directional FSC.

For a detailed information about the algorithm see our manuscript SETLINK TO MANUSCRIPT

# Installation

There are two independent ways of using/install this algorithm:

* Stand-alone installation - Nothing is required
* As a Xmipp protocol inside Scipion - Requires Scipion (encouraged)

## Stand-alone installation

Fourier Shell Occupancy uses a conda enviroment to do not interfer with the system that each user can have. Thus, the first step is to create a conda enviroment:

1) Creation of the conda enviaroment
- Install anaconda Python 3x version from https://www.anaconda.com/distribution/

- Create an enviroment for Fourier Shell Occupancy algorithm
    `conda create -n FourierShell python=3.6`
    If conda command does not work, a solution is to export the path `export PATH=~/anaconda3/bin:$PATH` or even better to create an alias in your .bashrc file.
- Activate the conda enviroment
`conda activate FourierShell`
Note that every time you will want to use the Fourier Shell Occupancy, the command `conda activate FourierShell` will be required
- Now the dependencies will be created, in particular, pyqt, numpy and matplotlib
`conda install -c anaconda python=3.6 pyqt=5` and `conda install -c conda-forge matplotlib`

2) Download the Fourier Occupancy Shell GUI an dall its dependencies
 `git clone https://github.com/Vilax/FourierOccupancyShell.git`
3) Run the installer script
`source install.sh`
3) Execute the software
`python main.py`

If for any reason this installer of step 2 fails. Open the file installer.sh and launch the commands one by one.

## Using in Scipion (still under development)

Before use the algoritm, Scipion needs to be installed. To do that see, Scipion installation instructions in the [Scipion Official web site](http://scipion.i2pc.es/).

Once Scipipion have been installed, the Xmipp package is required, but it can be easily installed in the [plugin manager](https://scipion-em.github.io/docs/docs/user/plugin-manager.html#plugin-manager) inside Scipion.
Then, the algorithm will be available to be used in Scipion. You can find the algorithm searching by `Ctrl+F`, or in the left lateral panel, in `3D->Analysis->Resolution->Xmipp - Forioer Shell Occupancy`

## Troubleshooting

There are some dependencies that are required. If in the Xmipp compilation some dependences are needed run
```
sudo apt-get install libsqlite3-dev libtiff5-dev libhdf5-dev python-numpy
```



