---
title: Kerr gravitational greybody factors with Mathematica
---
# Kerr gravitational greybody factors with Mathematica

This page documents the optional Mathematica workflow used to compute greybody factors for gravitational perturbations of Kerr black holes.

This part of the repository is independent of the Python examples. The Python package and Bilby examples use precomputed greybody-factor tables, while the Mathematica code is meant for users who want to reproduce or extend the computation of the underlying greybody factors.

## What this code does

The Mathematica workflow computes Kerr greybody factors for gravitational perturbations by solving the radial problem with controlled asymptotic expansions.

The computation is structured around two local series solutions:

1. a near-horizon expansion, used to impose the physical boundary condition at the black-hole horizon;
2. an asymptotic expansion at infinity, used to impose the outgoing/ingoing behavior far from the black hole.

The two solutions are then combined to extract the scattering coefficients and hence the greybody factors used by the GreyRing model.

## Folder

The repository structure is:

```text
mathematica/
  kerr_gf/
    KerrGF.nb
    series.m
```

The precomputed series file `series.m` should live next to the notebook that imports it.

## Precomputed series file

The repository currently includes a precomputed file:

```text
series.m
```

This file stores the near-horizon and asymptotic series coefficients up to order 8.

For most standard tests, this file can be imported directly without recomputing the symbolic series. This is faster and avoids repeating the most expensive symbolic part of the calculation.

## Computing longer series

If a higher-order expansion is needed, the notebook also contains the symbolic block that generates the series coefficients.

In that case, instead of importing only the precomputed `series.m` file, run the section that computes the near-horizon and infinity expansions with the desired truncation order.

## Practical recommendation

For SXS fits, use the Mathematica code to compute the complex reflectivity for \(M=1\) and for the remnant spin of the specific simulation. Then export two files, one for the absolute value and one for the phase of the reflectivity. The required file format is described in [SXS fit example]({{ site.baseurl }}/sxs_fit/).

For real-data analyses and injection-recovery studies with `(l,m)=(2,2)`, use the precomputed greybody-factor table available on [Zenodo](https://zenodo.org/records/19811974).
