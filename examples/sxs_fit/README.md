# SXS fit example

This folder contains an example showing how to fit an SXS multipole with the GreyRing model.
Currently, the code only fits SXS:BBH:3617. To fit other simulations or multipoles you have to compute the complex reflection amplitude for the specific configuration, following the instructions in the README.md file in the theory folder.  
 

Run from the repository root with:

```bash
python examples/sxs_fit/example_fit.py
```

The example calls the public API:

```python
import greyring as gr

result = gr.fit(
    sim_number=3617,
    ell=2,
    m=2,
    abs_file="examples/sxs_fit/theory/dataAbs22.txt",
    phase_file="examples/sxs_fit/theory/dataPhase22.txt",
)
```

The frequency range can be customized with:

```python
omega_i_factor=0.7
omega_f_amp_ratio=20.0
```

where `omega_i_factor=0.7` sets `omega_i = 0.7 omega_x`, and `omega_f_amp_ratio=20.0` selects the upper frequency through the condition that the amplitude has dropped by a factor of 20. See https://arxiv.org/pdf/2512.15877 for general details and   https://arxiv.org/pdf/2604.11895 (Supplemental Material Sec.B) for this specific example.
