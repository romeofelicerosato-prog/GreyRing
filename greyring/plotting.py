#Plot

############################# IMPORTS #############################

import matplotlib.pyplot as plt
import numpy as np

from .model_utils import amp_model, phase_model


############################## STYLE ##############################

def set_latex_style():
    """
    Set the matplotlib style used for the final figure.
    """
    plt.rcParams.update({
        "text.usetex": True,
        "font.family": "serif",
        "font.serif": ["Computer Modern Roman"],
        "axes.unicode_minus": False,
        "font.size": 12,
        "axes.labelsize": 14,
        "legend.fontsize": 9.5,
        "xtick.labelsize": 11,
        "ytick.labelsize": 11,
    })


############################### PLOT ################################

def make_final_figure(sim_number,omega_plot,abs_num_plot,amp_fit_plot,phi_th_det_plot,phi_sxs_det_plot,phi_fit_plot,omega_i,omega_f,omega_x,ell,m,left_plot=0.15,yphase_lim=(-2.5, 6.9),output_file="model_phase_amp.pdf"):
    """
    Build and save the final amplitude-and-phase figure.
    """
    mask_fit_plot = (omega_plot >= omega_i) & (omega_plot <= omega_f)
    right_plot = 0.97 * omega_f

    fig, ax = plt.subplots(2, 1, figsize=(6, 7), sharex=True)

    # AMPLITUDE
    ax[0].plot(omega_plot,abs_num_plot,color="black",lw=2.5,label=rf"$\left|\tilde{{h}}_{{{ell}{m}}}\right|$  SXS:BBH:{sim_number}")
    ax[0].plot(omega_plot[mask_fit_plot],amp_fit_plot[mask_fit_plot],color="#EE6677",linestyle=(0, (5, 4)),lw=2.0,label=rf"fit  $M A\,\left|R_{{{ell}{m}}}\right|/(M\omega)^p$")

    ax[0].axvline(x=omega_x, color="gray", linestyle=":", linewidth=1.5)
    ax[0].text(omega_x - 0.0025,ax[0].get_ylim()[1] * 0.05,rf"$\mathrm{{Re}}[\omega_{{{ell}{m}0}}]$",rotation=90,va="top",ha="right",color="gray")

    ax[0].set_ylabel(rf"$\left|\tilde{{h}}_{{{ell}{m}}}\right|$", fontsize=14)
    ax[0].set_yscale("log")
    ax[0].set_xlim(left_plot, right_plot)
    ax[0].legend(frameon=True,facecolor="white",edgecolor="none",framealpha=1.0,fontsize=10)
    ax[0].tick_params(axis="both",which="both",direction="in",top=True,bottom=True,left=True,right=True)
    ax[0].axvspan(omega_i, ax[0].get_xlim()[1], color="gray", alpha=0.1)

    # PHASE
    ax[1].plot(omega_plot,phi_th_det_plot,color="#4477AA",label=rf"$\arg(R_{{{ell}{m}}})$")
    ax[1].plot(omega_plot,phi_sxs_det_plot,color="black",lw=2.5,label=rf"$\arg(\tilde{{h}}_{{{ell}{m}}})$  SXS:BBH:{sim_number}")
    ax[1].plot(omega_plot[mask_fit_plot],phi_fit_plot[mask_fit_plot],color="#EE6677",linestyle=(0, (5, 4)),lw=2.0,label=rf"fit  $\arg(R_{{{ell}{m}}}) + a + b M\omega + \frac{{c}}{{M\omega}}$")
    ax[1].axvline(x=omega_x, color="gray", linestyle=":", linewidth=1.5)
    if m>= 0:
        ax[1].set_xlabel(r"$M\omega$", fontsize=14)
    else:
        ax[1].set_xlabel(r"$-M\omega$", fontsize=14)
    ax[1].set_ylabel(rf"$\arg(\tilde{{h}}_{{{ell}{m}}})$", fontsize=14)
    ax[1].set_xlim(left_plot, right_plot)
    ax[1].legend(frameon=True,facecolor="white",edgecolor="none",framealpha=1.0,fontsize=10)
    ax[1].tick_params(axis="both",which="both",direction="in",top=True,bottom=True,left=True,right=True)
    ax[1].axvspan(omega_i, ax[0].get_xlim()[1], color="gray", alpha=0.1)

    plt.tight_layout()
    plt.savefig(output_file, dpi=200)
    plt.show()


def align_phase_branch(omega_plot, omega_fit, phi_fit_det, phi_plot_det):
    """
    Input:
        omega_plot: frequency array used for the plot, ndarray
        omega_fit: frequency array used for the fit, ndarray
        phi_fit_det: detrended phase in the fit interval, ndarray
        phi_plot_det: detrended phase on the plot interval, ndarray
    Output:
        phi_plot_det: phase shifted by an integer multiple of 2pi, ndarray
    """
    phi_ref_on_plot = np.interp(omega_plot, omega_fit, phi_fit_det)

    overlap_mask = (omega_plot >= omega_fit.min()) & (omega_plot <= omega_fit.max())
    core_idx = np.where(overlap_mask)[0]

    if len(core_idx) > 0:
        delta = np.median(phi_plot_det[core_idx] - phi_ref_on_plot[core_idx])
    else:
        delta = np.median(phi_plot_det - phi_ref_on_plot)

    k = int(np.round(delta / (2 * np.pi)))
    return phi_plot_det - 2 * np.pi * k


def build_plot_data(omega_all,H_all,omega_fit,omega_f,left_plot,f_abs,f_phase,M_final,fit_data):
    """
    Input:
        omega_all: full frequency array, ndarray
        H_all: full waveform array, ndarray
        omega_fit: fit frequency array, ndarray
        omega_f: final fit frequency, float
        left_plot: left boundary of the plot, float
        f_abs: interpolant of the theory amplitude, callable
        f_phase: interpolant of the theory phase, callable
        M_final: remnant mass, float
        fit_data: dictionary returned by fit_full_model
    Output:
        plot_data: dictionary containing arrays needed for the final plot
    """
    right_plot = 0.97 * omega_f
    mask_plot = (omega_all >= left_plot) & (omega_all <= right_plot)

    omega_plot = omega_all[mask_plot]
    H_plot = H_all[mask_plot]

    abs_num_plot = np.abs(H_plot)

    phi_num_plot = np.unwrap(np.angle(H_plot))
    phi_num_det_plot = phi_num_plot - (fit_data["m_num"] * omega_plot + fit_data["q_num"])

    phi_num_det_plot = align_phase_branch(omega_plot,omega_fit,fit_data["phi_num_det_fit"],phi_num_det_plot)

    phi_th_plot = f_phase(omega_plot)
    phi_th_det_plot = phi_th_plot - (fit_data["m_th"] * omega_plot + fit_data["q_th"])

    amp_fit_plot = amp_model(omega_plot,f_abs(omega_plot),M_final,fit_data["A_fit"],fit_data["p_fit"])

    phi_fit_plot = phi_th_det_plot + phase_model(omega_plot,fit_data["a_fit"],fit_data["b_fit"],fit_data["c_fit"])

    return {
        "omega_plot": omega_plot,
        "abs_num_plot": abs_num_plot,
        "phi_num_det_plot": phi_num_det_plot,
        "phi_th_det_plot": phi_th_det_plot,
        "amp_fit_plot": amp_fit_plot,
        "phi_fit_plot": phi_fit_plot,
    }
