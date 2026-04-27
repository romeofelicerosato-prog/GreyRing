---
title: Installation
---

# Installation

Clone the [GreyRing GitHub repository](https://github.com/romeofelicerosato-prog/GreyRing):

```bash
git clone https://github.com/romeofelicerosato-prog/GreyRing.git
cd GreyRing
```

Create and activate a clean environment:

```bash
conda create -n greyring python=3.11
conda activate greyring
```

Install GreyRing in editable mode:

```bash
pip install -e .
```

## Dependencies

GreyRing has a small core set of Python dependencies, plus optional dependencies for SXS waveforms, Bilby inference, public strain-data access, and publication-style plots.

## Dependency levels

| Level | Needed for | Packages |
|---|---|---|
| Core | Importing GreyRing and using basic model utilities | `numpy`, `scipy`, `matplotlib` |
| SXS fit | Running the numerical-relativity fit example | `sxs` |
| Injection-recovery | Running controlled Bilby injections | `bilby`, `lalsuite` |
| Real data | Downloading and analyzing public strain data | `bilby`, `gwpy`, `lalsuite` |
| Plot styling | Labels with LaTeX | local LaTeX distribution |

## Optional dependencies

Some examples require additional packages:

```bash
pip install sxs
pip install bilby gwpy lalsuite
```

## LaTeX for plots

Some plotting functions may use Matplotlib with LaTeX rendering, for example for labels such as `$M_f$`, `$\chi_f$`, or `$\omega$`.

If LaTeX rendering is enabled, install a LaTeX distribution. If you do not want to install LaTeX, disable external LaTeX rendering in the plotting style and use Matplotlib mathtext instead.

## Suggested full environment

For running all examples, a typical installation is:

```bash
pip install -e .
pip install numpy scipy matplotlib sxs bilby gwpy lalsuite
```

## Examples

Examples are available in the [`examples/`](https://github.com/romeofelicerosato-prog/GreyRing/tree/main/examples) folder.

```bash
cd examples/sxs_fit
python run.py
```

```bash
cd ../injection_recovery
python injection_recovery.py
```

```bash
cd ../real_data
python run.py
```

## Repository

[GitHub repository](https://github.com/romeofelicerosato-prog/GreyRing)