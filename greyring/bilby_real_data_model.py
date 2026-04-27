# Definition of the GREYRING model

##########################      IMPORTS    #################################

import os
import numpy as np
import lal
from .bilby_real_data_auxiliary import *

######################      CONVERSION CONSTANTS    ########################

twopi = 2.0 * np.pi
C_mt = (lal.MSUN_SI * lal.G_SI) / (lal.C_SI**3) # to convert a mass (M☉) into a time (s)
C_md = (lal.MSUN_SI * lal.G_SI) / (1e6 * lal.PC_SI * lal.C_SI**2) # to convert a mass (M☉) into a distance (Mpc)

######################      MODEL DEFINITION    ############################

def model(
    frequency_array,
    final_mass,
    final_spin,
    A,
    p,
    c,
    luminosity_distance
):
    """
    Return the model in physical units.

    Parameters
    ----------
    frequency_array : array-like
        Frequencies in Hz.
    final_mass : float
        Final black-hole mass in solar masses.
    final_spin : float
        Dimensionless final spin.
    A : flot
        Amplitude of the model.
    p : float
        Power index of the model.
    c : float
        Phase parameter of the model.
    luminosity_distance : float
        Luminostity distance of the source.
    Returns
    -------
    H2 : ndarray
        Amplitude of the model.
    phi : ndarray
        Phase of the model.
    """

    frequency_array = np.asarray(frequency_array, dtype=float)

    #Here we import the theoretical values for the Reflection amplitude.
    R, Rphase = greybody_factor(frequency_array, final_mass, final_spin)
    omega = 2.0 * np.pi * final_mass * C_mt * frequency_array

    #Here we compute absolute value and phase of the model given the parameters.
    H2 = (A * R) / (omega ** p)
    phi = c / omega + Rphase

    #Conversion to physical units.
    H2 *= final_mass**2 * C_md * C_mt / luminosity_distance

    #We need to conjugate the model (phi->-phi) given the different Fourier convention among
    #Bilby and the fits of the model, see details in https://arxiv.org/pdf/2604.11895, Appendix B, Extrinsic parameters and angular dependence.
    return H2, -phi

def greyring_22_free_ampl_phase(
    frequency_array,
    final_mass,
    final_spin,
    A,
    p,
    c,
    luminosity_distance,
    theta_jn,
    **kwargs
 ):
    
     """
    Return the model in physical units.

    Parameters
    ----------
    frequency_array : array-like
        Frequencies in Hz.
    final_mass : float
        Final black-hole mass in solar masses.
    final_spin : float
        Dimensionless final spin.
    A : flot
        Amplitude of the model.
    p : float
        Power index of the model.
    c : float
        Phase parameter of the model.
    theta_jn : float
        Inclination of the source.
    luminosity_distance : float
        Luminostity distance of the source.
    Returns
    -------
    wave_plus : ndarray
        Plus plarization.
    wave_cross : ndarray
        Cross polarization.
    """
     f = np.asarray(frequency_array, dtype=float)

     wave_plus = np.zeros_like(f, dtype=complex)
     wave_cross = np.zeros_like(f, dtype=complex)
     m = f > 0.0
     if not np.any(m):
        return {"plus": wave_plus, "cross": wave_cross}

     H2, phi = model(
        f[m],
        final_mass,
        final_spin,
        A,
        p,
        c,
        luminosity_distance,
     )

    #Compute the angular dependence and the polarization, considering (22) and (2-2) modes, 
    #following https://arxiv.org/pdf/2604.11895, Appendix B, Extrinsic parameters and angular dependence.
     H2 = H2 / 2.0

     ampl_plus = H2 * (1.0 + np.cos(theta_jn)**2) / 2.0
     ampl_cross = H2 * np.cos(theta_jn)

     wave_plus[m] = np.sqrt(5.0 / (4.0 * np.pi)) * ampl_plus * np.exp(1j * phi)
     wave_cross[m] = np.sqrt(5.0 / (4.0 * np.pi)) * ampl_cross * (-1j) * np.exp(1j * phi)

     return {"plus": wave_plus, "cross": wave_cross}
