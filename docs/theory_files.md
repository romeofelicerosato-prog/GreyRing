---
title: Theory files
---

# Theory files

Some examples require local greybody-factor tables.

Each example has a local `theory/` folder where the required files should be placed:

```text
examples/
  sxs_fit/
    theory/
  injection_recovery/
    theory/
  real_data/
    theory/
```

The exact files required by each example are listed in the corresponding example README.

## Example

For an example that requires the files

```text
Zed_abs.txt
Zed_phase.txt
```

place them in the local `theory/` folder before running the script:

```text
examples/example_name/theory/
  Zed_abs.txt
  Zed_phase.txt
```
Then, run each example from within its own folder. The required theory files are specified in the corresponding README.

## Data availability

Greybody factors can be computed with the Mathematica codes included in this repository; see [Mathematica greybody-factor code]({{ site.baseurl }}/kerr_gf_mathematica/) for details.

A precomputed table of greybody factors, sampled in spin and frequency for the `(l,m)=(2,2)` mode, is also available on [Zenodo](https://zenodo.org/records/19811974). This is the table required by the real-data and injection-recovery examples.

Download the Zenodo files and place them in the corresponding local `theory/` folder before running the examples.