from pathlib import Path

import numpy as np
import greyring as gr


HERE = Path(__file__).resolve().parent
THEORY = HERE / "theory"

omega_theory = np.linspace(0.001, 1.2, 1200)

result = gr.fit(
    sim_number=3617,
    ell=2,
    m=-2,
    abs_file=str(THEORY / "dataAbs22.txt"),
    phase_file=str(THEORY / "dataPhase22.txt"),
    omega_theory=omega_theory,
    omega_i_factor=0.7,
    omega_f_amp_ratio=20.0,
    make_plot=True,
    output_file=str(HERE / "example_l2m-2.png"),
)

print(f"(ell, m) = ({result.ell}, {result.m})")
print(f"M_final = {result.M_final:.6f}")
print(f"chi_final = {result.chi_final:.6f}")
print(f"omega_x = {result.omega_x:.6f}")
print(f"omega_i = {result.omega_i:.6f}")
print(f"omega_f = {result.omega_f:.6f}")
print(f"A = {result.A}")
print(f"p = {result.p}")
print(f"a = {result.a}")
print(f"b = {result.b}")
print(f"c = {result.c}")
print(f"mismatch = {result.mismatch}")
print(f"plot saved to {result.output_file}")