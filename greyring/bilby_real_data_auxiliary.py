# Auxiliary functions useful to define the model

##########################      IMPORTS    #################################

import os
import numpy as np
import lal
from scipy.interpolate import RegularGridInterpolator

######################      CONVERSION CONSTANTS    ########################

twopi = 2.0 * np.pi
C_mt = (lal.MSUN_SI * lal.G_SI) / (lal.C_SI**3) # to convert a mass (M☉) into a time (s)
C_md = (lal.MSUN_SI * lal.G_SI) / (1e6 * lal.PC_SI * lal.C_SI**2) # to convert a mass (M☉) into a distance (Mpc)

#########################      FUNCTIONS    ################################

def _theory_path(fname: str) -> str:
    """
    Read files in the folder "theory", containing the tabulated complex reflection amplitudes.
    """
    local_path = os.path.join(os.getcwd(), "theory", fname)
    if os.path.exists(local_path):
        return local_path

    base_dir = os.path.dirname(__file__)
    return os.path.join(base_dir, "theory", fname)

def greybody_factor(frequency_array, final_mass, final_spin):
    """
    Return the interpolated reflection amplitude and detrended phase.

    Parameters
    ----------
    frequency_array : array-like
        Frequencies in Hz.
    final_mass : float
        Final black-hole mass in solar masses.
    final_spin : float
        Dimensionless final spin.

    Returns
    -------
    Zabs : ndarray
        Absolute value of the reflection amplitude.
    Zphase : ndarray
        Interpolated phase of the reflection amplitude with its best-fit linear trend removed, as this latter
        only depends on the boundary conditions used in the theoretical computation of the reflection amplitude.
    """
    
    # Here we build the interpolators the first time the function is called, 
    # with no need of recomputing it everytime we call it during an inference.
    # This helps speeding up the computation.
    
    if not hasattr(greybody_factor, "_zed_abs_interp"): 
        abs_tab = np.loadtxt(_theory_path("Zed_abs.txt"))
        phase_tab = np.loadtxt(_theory_path("Zed_phase.txt"))

        a_vals = abs_tab[:, 0]
        zabs_grid = abs_tab[:, 1:]
        zphase_grid = phase_tab[:, 1:]

        # This works for greybody factors computed along the grid of Momega. 
        # If using a different grid change the array below.
        
        omega_vals = np.linspace(0.001, 1.600, zabs_grid.shape[1])
        

        # Sort depending on the remnant spin
        
        order = np.argsort(a_vals)
        a_vals = a_vals[order]
        zabs_grid = zabs_grid[order, :]
        zphase_grid = zphase_grid[order, :]

        # Unwrap phase along the omega direction
        
        zphase_grid = np.unwrap(zphase_grid, axis=1)

        greybody_factor._a_vals = a_vals
        greybody_factor._omega_vals = omega_vals

        # Here we interpolate the theoretical results in order to apply them to any frequency array.
        # A 2D-cubic interpolator is used. If more precision is needed this has to be modified.

        greybody_factor._zed_abs_interp = RegularGridInterpolator(
            (a_vals, omega_vals),
            zabs_grid,
            method="cubic", 
            bounds_error=False,
            fill_value=None,
        )
        greybody_factor._zed_phase_interp = RegularGridInterpolator(
            (a_vals, omega_vals),
            zphase_grid,
            method="cubic",
            bounds_error=False,
            fill_value=None,
        )

    # Convert frequencies to dimensionless omega = 2 pi M f
    
    frequency_array = np.asarray(frequency_array, dtype=float)
    omega = 2.0 * np.pi * final_mass * C_mt * frequency_array

    omega_min = greybody_factor._omega_vals[0]
    omega_max = greybody_factor._omega_vals[-1]
    omega_clipped = np.clip(omega, omega_min, omega_max)

    # Interpolation points: (spin, Momega)
    
    points = np.column_stack((
        np.full_like(omega_clipped, float(final_spin)),
        omega_clipped,
    ))

    zabs_interp = greybody_factor._zed_abs_interp
    zphase_interp = greybody_factor._zed_phase_interp

    Zabs = zabs_interp(points)
    Zphase = zphase_interp(points)

    # Remove the best-fit linear trend from the phase
    
    slope, intercept = np.polyfit(omega_clipped, Zphase, 1)
    Zphase = Zphase - (intercept + slope * omega_clipped)

    # Safety check, enforce non-negative amplitude
    
    Zabs = np.clip(Zabs, 0.0, None)

    return Zabs, Zphase
