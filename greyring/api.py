from dataclasses import dataclass

from .model_utils import mismatch_complex
from .sxs_processing import prepare_fit_data
from .fitting import (
    build_theory_interpolants,
    fit_full_model,
    build_complex_model,
)
from .plotting import (
    set_latex_style,
    make_final_figure,
    build_plot_data,
)


@dataclass
class GreyRingResult:
    """
    Container for the output of a GreyRing fit.
    """
    sim_number: int
    ell: int
    m: int

    M_final: float
    chi_final: float

    omega_x: float
    omega_i: float
    omega_f: float

    A: float
    p: float
    a: float
    b: float
    c: float

    mismatch: float
    output_file: str | None = None


def fit(
    sim_number,
    ell,
    m,
    abs_file,
    phase_file,
    omega_theory,
    omega_i_factor=0.7,
    omega_f_amp_ratio=20.0,
    omega_max_search=1.0,
    left_plot=0.15,
    make_plot=True,
    output_file=None,
    use_latex=True,
):
    """
    Fit one SXS multipole with the GreyRing frequency-domain model.

    Parameters
    ----------
    sim_number : int
        SXS simulation number, e.g. 3617.
    ell, m : int
        Multipole indices.
    abs_file : str
        Path to the file containing |R_lm| or |Zed_lm|.
    phase_file : str
        Path to the file containing arg(R_lm) or arg(Zed_lm).
    omega_theory : array_like
        Frequency array corresponding to the reflectivity values in
        abs_file and phase_file.
    omega_i_factor : float, optional
        Defines omega_i = omega_i_factor * omega_x.
    omega_f_amp_ratio : float, optional
        Defines omega_f as the first frequency after omega_x where
        |h(omega_f)| <= |h(omega_x)| / omega_f_amp_ratio.
    omega_max_search : float, optional
        Maximum dimensionless frequency used in the SXS FFT.
    left_plot : float, optional
        Left boundary of the plot.
    make_plot : bool, optional
        If True, build and save the amplitude/phase plot.
    output_file : str or None, optional
        Name of the output plot file. If None, a default name is used.
    use_latex : bool, optional
        If True, use the matplotlib LaTeX style defined in plotting.py.

    Returns
    -------
    GreyRingResult
        Best-fit parameters, remnant data, selected frequency interval,
        mismatch, and output plot filename.
    """
    if use_latex:
        set_latex_style()

    if output_file is None:
        output_file = f"greyring_fit_SXS{sim_number}_l{ell}m{m}.pdf"

    (
        omega_fit,
        H_fit,
        omega_all,
        H_all,
        M_final,
        chi_final,
        omega_x,
        omega_i,
        omega_f,
    ) = prepare_fit_data(
        sim_number=sim_number,
        omega_max_search=omega_max_search,
        ell=ell,
        m=m,
        omega_i_factor=omega_i_factor,
        ratio_factor=omega_f_amp_ratio,
    )

    f_abs, f_phase = build_theory_interpolants(
        sim_number=sim_number,
        abs_file=abs_file,
        phase_file=phase_file,
        omega_theory=omega_theory,
        ell=ell,
        m=m,
    )

    fit_data = fit_full_model(
        omega_fit=omega_fit,
        H_fit=H_fit,
        f_abs=f_abs,
        f_phase=f_phase,
        M_final=M_final,
    )

    H_model = build_complex_model(
        omega=omega_fit,
        f_abs=f_abs,
        f_phase=f_phase,
        M_final=M_final,
        fit_data=fit_data,
    )

    mismatch = mismatch_complex(omega_fit, H_fit, H_model)

    if make_plot:
        plot_data = build_plot_data(
            omega_all=omega_all,
            H_all=H_all,
            omega_fit=omega_fit,
            omega_f=omega_f,
            left_plot=left_plot,
            f_abs=f_abs,
            f_phase=f_phase,
            M_final=M_final,
            fit_data=fit_data,
        )

        make_final_figure(
            sim_number=sim_number,
            ell=ell,
            m=m,
            omega_plot=plot_data["omega_plot"],
            abs_num_plot=plot_data["abs_num_plot"],
            amp_fit_plot=plot_data["amp_fit_plot"],
            phi_th_det_plot=plot_data["phi_th_det_plot"],
            phi_sxs_det_plot=plot_data["phi_num_det_plot"],
            phi_fit_plot=plot_data["phi_fit_plot"],
            omega_i=omega_i,
            omega_f=omega_f,
            omega_x=omega_x,
            left_plot=left_plot,
            output_file=output_file,
        )
    else:
        output_file = None

    return GreyRingResult(
        sim_number=sim_number,
        ell=ell,
        m=m,
        M_final=M_final,
        chi_final=chi_final,
        omega_x=omega_x,
        omega_i=omega_i,
        omega_f=omega_f,
        A=fit_data["A_fit"],
        p=fit_data["p_fit"],
        a=fit_data["a_fit"],
        b=fit_data["b_fit"],
        c=fit_data["c_fit"],
        mismatch=mismatch,
        output_file=output_file,
    )