# Real-data example

This folder contains a custom Bilby run on real gravitational-wave data.

Run it from this folder:

```bash
cd examples/real_data
python run.py
```

The run downloads strain and PSD data using GWpy, builds the Bilby interferometers, and analyzes the selected frequency band with the GreyRing model.

The corresponding GreyRing model and auxiliary functions live in the package core with dedicated real-data names.

The theory file expects the presence of the greybody factor grid for the (22) multipole available at https://zenodo.org/records/19811974. In particular, current version expects the paths "theory/Zed_abs.txt" and "theory/Zed_phase.txt" for absolute value and phase of the (22) greybody factor.
