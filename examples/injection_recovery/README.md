# Injection-recovery example

This folder contains a custom Bilby injection-recovery run wiht GreyRing for the (2,2) multipole.

Run it from this folder:

```bash
cd examples/injection_recovery
python injection_recovery.py
```

The run expects the greybody tables and PSD curve inside the local `theory/` folder.

In particular, current version expects the path "theory/Sensitivity_curves/aligo_O4high.txt" for the PSD curve, and the paths "theory/Zed_abs.txt" and "theory/Zed_phase.txt" for absolute value and phase of the (22) greybody factor. These latter files are available at: https://zenodo.org/records/19811974.

The corresponding GreyRing model and auxiliary functions live in the package core with dedicated injection-recovery names.
