# alphashapy

[![PyPI](https://img.shields.io/pypi/v/alphashapy.svg)](https://pypi.org/project/alphashapy/)
[![Docs](https://readthedocs.org/projects/alphashapy/badge/?version=latest)](https://alphashapy.readthedocs.io/en/latest/)
[![Tests](https://github.com/itaipelles/alphashapy/actions/workflows/test.yml/badge.svg)](https://github.com/itaipelles/alphashapy/actions/workflows/test.yml)
[![Changelog](https://img.shields.io/github/v/release/itaipelles/alphashapy?include_prereleases&label=changelog)](https://github.com/itaipelles/alphashapy/releases)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/itaipelles/alphashapy/blob/main/LICENSE)

A Python package for constructing 2D alpha hulls for negative alphas. The algorithm is from the [paper](https://ieeexplore.ieee.org/abstract/document/1056714):

H. Edelsbrunner, D. Kirkpatrick and R. Seidel, "On the shape of a set of points in the plane," in IEEE Transactions on Information Theory, vol. 29, no. 4, pp. 551-559, July 1983, doi: 10.1109/TIT.1983.1056714.

And the implementation relies on Qhull's implementation of Voronoi diagrams, wrapped nicely for Python by Scipy [here](https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.Voronoi.html).

In the future I will try to add alpha shapes for negative alphas as well, today there is no python package that does that.

For alpha shapes with positive alphas, please use [alphashape](https://github.com/bellockk/alphashape) (which also supports higher dimensions) or [alpha_shapes](https://github.com/panosz/alpha_shapes), both are great but do not currently (August 2024) support alpha hulls nor negative alphas.

## Installation

Install this library using `pip`:
```bash
pip install alphashapy
```
## Usage

```python
import numpy as np
from alphashapy import alphahull_negative_alpha
points = np.random.rand(100,2)
alpha = -1
alphahull_negative_alpha(points, alpha)
```

## Development

To contribute to this library, first checkout the code. Then create a new virtual environment:
```bash
cd alphashapy
python -m venv venv
source venv/bin/activate
```
Now install the dependencies and test dependencies:
```bash
python -m pip install -e '.[test]'
```
To run the tests:
```bash
python -m pytest
```
