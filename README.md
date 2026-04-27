# GreyRing

GreyRing is a frequency-domain model for black-hole ringdown analyses based on greybody factors.

This repository contains two layers:

- `greyring/`: importable Python code;
- `examples/`: executable examples and custom Bilby runs.

The current package includes:

- SXS multipole fits with GreyRing;
- amplitude/phase fit plots;
- mismatch computation;
- injection-recovery Bilby example;
- real-data Bilby example;
- mathematica notebook for Reflection amplitude computation.

## Installation (To change)

From the root of the repository, run:

```bash
pip install -e .
```

The `-e` flag installs the package in editable mode, so local changes to the source files are immediately visible.

## SXS fit example

The SXS fitting example is in:

```text
examples/sxs_fit/
```

Before running it, place the required theory files in the appropriate location, as described in:

```text
examples/sxs_fit/theory/README.md
```

Then run:

```bash
python examples/sxs_fit/example_fit.py
```

## Injection-recovery example

The injection-recovery Bilby run is in:

```text
examples/injection_recovery/
```

Before running it, place the greybody tables and PSD curve in:

```text
examples/injection_recovery/theory/
```

See:

```text
examples/injection_recovery/theory/README.md
```

Then run:

```bash
cd examples/injection_recovery
python injection_recovery.py
```

This example is intentionally a custom Bilby workflow. The model used by this run lives in the package core under a dedicated injection-recovery name.

## Real-data example

The real-data Bilby run is in:

```text
examples/real_data/
```

Before running it, place the greybody tables in:

```text
examples/real_data/theory/
```

See:

```text
examples/real_data/theory/README.md
```

Then run:

```bash
cd examples/real_data
python run.py
```

This example downloads strain and PSD data using GWpy and runs a custom GreyRing analysis with Bilby.

### Optional LaTeX support

Some plotting routines can use LaTeX rendering through Matplotlib.
For this, a working LaTeX installation is required on your system.