---
title: Injection-recovery example
---

# Injection-recovery example

This example performs a controlled Bilby injection-recovery run with the GreyRing waveform model.

## Folder

```text
examples/injection_recovery/
```

Structure:

```text
examples/injection_recovery/
  injection_recovery.py
  theory/
    Zed_abs.txt
    Zed_phase.txt
    Sensitivity_curves/
      aligo_O4high.txt
```

## Required files

Place the greybody tables in:

```text
examples/injection_recovery/theory/
```

```text
Zed_abs.txt
Zed_phase.txt
```

Place the PSD curve in:

```text
examples/injection_recovery/theory/Sensitivity_curves/
```

For example:

```text
aligo_O4high.txt
```

See [Theory files](theory_files.md) for details on the needed structure of the files.

## Run

From the repository root:

```bash
cd examples/injection_recovery
python injection_recovery.py
```
The script defines the detector network, injected parameters, priors, waveform generator, PSDs, likelihood, and Dynesty sampler.

## Reference injection run

The figure below shows a representative injection-recovery result for a GW250114-like signal, similar to the example discussed in [the paper](https://arxiv.org/pdf/2604.11895) with an analysis frequency range of `[120, 500] Hz`.

<div class="single-figure">
  <img
    src="{{ '/assets/examples/greyring_inj_recover_corner_all.png' | relative_url }}"
    alt="Injection-recovery posterior"
  >
</div>
