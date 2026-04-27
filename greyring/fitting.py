#Fitting utils

############################ IMPORTS ###############################

import numpy as np
from scipy.interpolate import interp1d
from scipy.optimize import curve_fit

from .model_utils import (
    load_key_from_assignment_file,
    amp_model,
    phase_model,
)
from .sxs_processing import detrend_linear


############################ THEORY ###############################

def build_theory_interpolants(
    sim_number,
    abs_file,
    phase_file,
    omega_theory,
    ell=2,
    m=2,
):
    """
    Input:
        sim_number: simulation number, int
        abs_file: path to the theory amplitude file, str
        phase_file: path to the theory phase file, str
        omega_theory: frequency array corresponding to the theory data, ndarray
        ell: multipole index, int
        m: azimuthal index, int
    Output:
        f_abs: interpolant of the theory amplitude, callable
        f_phase: interpolant of the unwrapped theory phase, callable
    """
    key = f"Zed{sim_number}" if sim_number is not None else f"Zed{ell}{abs(m)}"

    try:
        abs_th_raw = load_key_from_assignment_file(abs_file, key)
        phi_th_raw = load_key_from_assignment_file(phase_file, key)
    except KeyError:
        fallback_key = f"Zed{ell}{abs(m)}"
        abs_th_raw = load_key_from_assignment_file(abs_file, fallback_key)
        phi_th_raw = load_key_from_assignment_file(phase_file, fallback_key)

    Momega_th = np.asarray(omega_theory, dtype=float)
    abs_th_raw = np.asarray(abs_th_raw, dtype=float)
    phi_th_raw = np.asarray(phi_th_raw, dtype=float)

    if len(Momega_th) != len(abs_th_raw):
        raise ValueError(
            f"omega_theory has length {len(Momega_th)}, "
            f"but abs_file has length {len(abs_th_raw)}."
        )

    if len(Momega_th) != len(phi_th_raw):
        raise ValueError(
            f"omega_theory has length {len(Momega_th)}, "
            f"but phase_file has length {len(phi_th_raw)}."
        )

    idx = np.argsort(Momega_th)
    Momega_th = Momega_th[idx]
    abs_th_raw = abs_th_raw[idx]
    phi_th_raw = phi_th_raw[idx]

    f_abs_base = interp1d(
        Momega_th,
        abs_th_raw,
        kind="cubic",
        bounds_error=True,
    )

    f_phase_base = interp1d(
        Momega_th,
        np.unwrap(phi_th_raw),
        kind="cubic",
        bounds_error=True,
    )

    def f_abs(omega):
        return f_abs_base(omega)

    def f_phase(omega):
        phi = f_phase_base(omega)

        if m < 0:
            phi = -phi

        return phi

    return f_abs, f_phase


############################# FITS ################################

def fit_amplitude(omega, H_fit, f_abs, M_final):
    """
    Input:
        omega: frequency array, ndarray
        H_fit: numerical Fourier-domain waveform, ndarray
        f_abs: interpolant of the theory amplitude, callable
        M_final: remnant mass, float
    Output:
        A_fit: best-fit amplitude parameter, float
        p_fit: best-fit power-law exponent, float
        pcov: covariance matrix from curve_fit, ndarray
    """
    abs_num = np.abs(H_fit)
    abs_th = f_abs(omega)

    def model_for_curve_fit(og, A, p):
        return amp_model(og, abs_th, M_final, A, p)

    popt, pcov = curve_fit(model_for_curve_fit,omega,abs_num,p0=[1.0, 0.5],maxfev=20000)

    A_fit, p_fit = popt
    return A_fit, p_fit, pcov


def fit_phase(omega, phi_num_det, phi_th_det):
    """
    Input:
        omega: frequency array, ndarray
        phi_num_det: detrended numerical phase, ndarray
        phi_th_det: detrended theory phase, ndarray
    Output:
        a_fit: constant phase coefficient, float
        b_fit: linear phase coefficient, float
        c_fit: inverse-frequency phase coefficient, float
        pcov: covariance matrix from curve_fit, ndarray
    """
    y = phi_num_det - phi_th_det

    popt, pcov = curve_fit(phase_model,omega,y,p0=[0.0, 0.0, 1.0],maxfev=20000)

    a_fit, b_fit, c_fit = popt
    return a_fit, b_fit, c_fit, pcov

def fit_full_model(omega_fit, H_fit, f_abs, f_phase, M_final):
    """
    Input:
        omega_fit: frequency array in the fit interval, ndarray
        H_fit: numerical waveform in the fit interval, ndarray
        f_abs: interpolant of the theory amplitude, callable
        f_phase: interpolant of the theory phase, callable
        M_final: remnant mass, float
    Output:
        fit_data: dictionary containing fit parameters and detrending coefficients
    """
    phi_num_fit = np.unwrap(np.angle(H_fit))
    phi_th_fit = f_phase(omega_fit)

    phi_num_det_fit, m_num, q_num = detrend_linear(omega_fit, phi_num_fit)
    phi_th_det_fit, m_th, q_th = detrend_linear(omega_fit, phi_th_fit)

    A_fit, p_fit, _ = fit_amplitude(omega_fit, H_fit, f_abs, M_final)
    a_fit, b_fit, c_fit, _ = fit_phase(omega_fit, phi_num_det_fit, phi_th_det_fit)

    return {
        "A_fit": A_fit,
        "p_fit": p_fit,
        "a_fit": a_fit,
        "b_fit": b_fit,
        "c_fit": c_fit,
        "m_num": m_num,
        "q_num": q_num,
        "m_th": m_th,
        "q_th": q_th,
        "phi_num_det_fit": phi_num_det_fit,
        "phi_th_det_fit": phi_th_det_fit,
    }


def build_complex_model(omega, f_abs, f_phase, M_final, fit_data):
    """
    Input:
        omega: frequency array, ndarray
        f_abs: interpolant of the theory amplitude, callable
        f_phase: interpolant of the theory phase, callable
        M_final: remnant mass, float
        fit_data: dictionary returned by fit_full_model
    Output:
        H_model: complex fitted waveform, ndarray
    """
    amp = amp_model(
        omega,
        f_abs(omega),
        M_final,
        fit_data["A_fit"],
        fit_data["p_fit"],
    )

    phi_th = f_phase(omega)

    phi_model = (f_phase(omega)
        + phase_model(omega, fit_data["a_fit"], fit_data["b_fit"], fit_data["c_fit"])
        + (fit_data["m_num"] - fit_data["m_th"]) * omega+ (fit_data["q_num"] - fit_data["q_th"]))

    return amp * np.exp(1j * phi_model)
