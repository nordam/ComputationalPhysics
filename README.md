# TFY4235 Computational Physics
Jupyter notebooks and scripts with code examples, as shown in the lectures of TFY4235 Computational Physics at NTNU, spring 2016. The examples are shown in class as part of the lectures, and with supporting material. They are not intended to be completely stand-alone or self-explanatory.

## Jupyter notebooks (examples in python)
Try out the code in the notebooks, without installing anything locally, through binder: [![Binder](http://mybinder.org/badge.svg)](http://mybinder.org/repo/nordam/ComputationalPhysics)

## Dependencies
To run the python examples locally, there are some dependencies. To install dependencies with ``conda``, use ``conda env create -f environment.yml``. To install dependencies with ``pip``, use ``pip install -r requirements.txt``. Note that the last part of the notebook on NetCDF and HDF5 uses the library Basemap to plot things on a map. Basemap can be installed with ``conda``, but not with ``pip`` (at least not at the moment, as far as I can tell). Check out https://github.com/matplotlib/basemap if you want to install it yourself.
