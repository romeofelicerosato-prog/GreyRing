# Kerr gravitational greybody factors

This folder contains the Mathematica code used to compute gravitational greybody factors for Kerr black holes. Specifically, current version computes the Complex Reflection amplitude for gravitational perturbations.

The code is organized so that the precomputed series can be loaded directly in standard use, while the symbolic series-generation blocks can be rerun only when longer series expansions are needed. Current in series.m an 8th order expansion is used.


## Code structure

The Mathematica notebook is organized into the following main blocks.

### 1. Useful definitios

The first 2 block defines the general variables, conventions, and auxiliary quantities used throughout the calculation.

This block should always be evaluated before running the rest of the notebook.

### 2. Equations and Series

The block that computes the near-horizon series expansion and the asymptotic one at infinity.

This block is optional in normal use, because the precomputed series are already stored in `series.m`.

### 3. Integrator

For standard usage, the two symbolic series-generation blocks can be skipped.

The file
```
series.m
```
currently contains the precomputed series up to order 8. In this section the function for computing complex reflection amplitude is defined.


## 4. SXS:BBH:3617

This section contains an example of usage of the function.
