# model and utils

############################# IMPORTS #############################

import ast
import numpy as np

############################## UTILS ##############################

def mismatch_complex(omega, h1, h2):
    """
     Inputs:
       omega : ndarray
           Frequency array.
       h1, h2 : ndarray
           Complex signal and model.
     Output:
       mismatch : float
    """
        
    omega = np.asarray(omega, float)
    h1 = np.asarray(h1, complex)
    h2 = np.asarray(h2, complex)

    domega = np.mean(np.diff(omega))

    inner12 = np.sum(np.conj(h1) * h2) * domega
    inner11 = np.sum(np.conj(h1) * h1) * domega
    inner22 = np.sum(np.conj(h2) * h2) * domega

    overlap = np.abs(inner12) / np.sqrt(inner11 * inner22)
    mismatch=1 - overlap.real
    return mismatch


def load_key_from_assignment_file(filename, target_key):
    """
     Input:
       filename: path to the input text file, str
       target_key: name of the variable to load, str
     Output:
       array: value associated with target_key, ndarray
    """
    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            if not line or "=" not in line:
                continue
            name, value = line.split("=", 1)
            if name.strip() == target_key:
                return np.array(ast.literal_eval(value.strip()), dtype=float)
    raise KeyError(f"Key {target_key!r} not found")

############################## MODEL ##############################

def amp_model(omega, abs_th, M_final, A, p):
    return M_final * A * abs_th / (omega ** p)

def phase_model(omega, a, b, c):
    return a + b * omega + c / omega
