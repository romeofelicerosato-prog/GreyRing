# Injection-recovery code

##########################      IMPORTS    #################################

import os
import numpy as np
import bilby
import matplotlib.pyplot as plt
from bilby.gw.conversion import identity_map_conversion
from greyring.bilby_injection_model import greyring_22_free_ampl_phase


#########################      THREADING    ################################

os.environ["OMP_NUM_THREADS"] = "12"
os.environ["OPENBLAS_NUM_THREADS"] = "4"


########################      OUTPUT SETUP   ###############################

outdir = "outdir"
os.makedirs(outdir, exist_ok=True)
label = "greyring_inj_recover"
bilby.core.utils.setup_logger(outdir=outdir, label=label)

######################      GLOBAL SETTINGS   ##############################

# Here you can select the frequency range (in Hz) for the analysis
fmin = 120
fmax = 512

duration = 8.0
sampling_frequency = 4096.0

trigger_time = 1420878141.235932
start_time = trigger_time - duration + 2.0
TREF = trigger_time

print(f"Fixed frequency band: f in [{fmin:.6f}, {fmax:.6f}] Hz")

####################      INJECTED PARAMETERS  #############################

# Mf_target, theta_jn, psi, ra, dec, geocent_time, luminosity_distance are set to be compatible with GW250114,  
# while the model parameters are based on the simulation SXS:BBH:3617. Change here to test different configurations


Mf_target = 68.4
A_val = 5.588052499223044
p_val = 0.5168825491261931
c_val = 1.190651409963232

inj = dict(
    luminosity_distance=403.0,
    theta_jn=0.78,
    psi=1.329,
    ra=2.333,
    dec=0.190,
    geocent_time=trigger_time,
    phase=0.0,
    final_mass=68.4,
    final_spin=0.6864402,
    A=A_val,
    p=p_val,
    c=c_val,
)

print("\n[INJECTION PARAMETERS]")
for k in ["final_mass", "final_spin", "A", "p", "c"]:
    print(f"{k:>12s} = {inj[k]}")

####################      WAVEFORM GENERATOR  ##############################

waveform_generator = bilby.gw.WaveformGenerator(
    duration=duration,
    sampling_frequency=sampling_frequency,
    start_time=start_time,
    frequency_domain_source_model=greyring_22_free_ampl_phase,
    parameter_conversion=identity_map_conversion,
    waveform_arguments=dict(
        fmin=fmin,
        fmax=fmax,
        tref=TREF,
    ),
)

##################      INTERFEROMETERS, PSD     ###########################

ifos = bilby.gw.detector.InterferometerList(["H1", "L1"])

ifos[0].power_spectral_density = bilby.gw.detector.PowerSpectralDensity(
    asd_file="theory/Sensitivity_curves/aligo_O4high.txt"
)
ifos[1].power_spectral_density = bilby.gw.detector.PowerSpectralDensity(
    asd_file="theory/Sensitivity_curves/aligo_O4high.txt"
)

for ifo in ifos:
    ifo.minimum_frequency = fmin
    ifo.maximum_frequency = fmax

ifos.set_strain_data_from_zero_noise(
    sampling_frequency=sampling_frequency,
    duration=duration,
    start_time=start_time
)

#########################      INJECTION     ###############################

ifos.inject_signal(
    parameters=inj,
    waveform_generator=waveform_generator,
    raise_error=False
)

##########################      PRIORS     #################################

# The priors below are base on the typical values of the model parameters 
# for comparable mass mergers.

priors = bilby.core.prior.PriorDict()
priors["final_mass"] = bilby.core.prior.Uniform(50.0, 90.0, name="final_mass")
priors["final_spin"] = bilby.core.prior.Uniform(0.0, 0.99, name="final_spin")
priors["A"] = bilby.core.prior.Uniform(0.0, 10.0, name="A")
priors["p"] = bilby.core.prior.Uniform(-0.5, 1.5, name="p")
priors["c"] = bilby.core.prior.Uniform(0.0, 3.0, name="c")

priors["phase"] = bilby.core.prior.Uniform(0.0, 2 * np.pi, name="phase")
priors["geocent_time"] = bilby.core.prior.Uniform(
    trigger_time - 0.01, trigger_time + 0.01, name="geocent_time"
)

priors["luminosity_distance"] = bilby.core.prior.DeltaFunction(inj["luminosity_distance"])
priors["theta_jn"] = bilby.core.prior.DeltaFunction(inj["theta_jn"])
priors["psi"] = bilby.core.prior.DeltaFunction(inj["psi"])
priors["ra"] = bilby.core.prior.DeltaFunction(inj["ra"])
priors["dec"] = bilby.core.prior.DeltaFunction(inj["dec"])

##########################     LIKELIHOOD    ###############################

# In this version we marginalize over time and phase, however since it is an injection 
# you can also fix those parameters as in https://arxiv.org/pdf/2604.11895. 

likelihood = bilby.gw.likelihood.GravitationalWaveTransient(
    interferometers=ifos,
    waveform_generator=waveform_generator,
    priors=priors,
    time_marginalization=True,
    phase_marginalization=True,
    distance_marginalization=False,
)

#############################     RUN    ###################################

result = bilby.run_sampler(
    likelihood=likelihood,
    priors=priors,
    sampler="dynesty",
    nlive=500,
    walks=30,
    naccept=20,
    npool=12,
    sample="acceptance-walk",
    proposals=["diff"],
    bound="live",
    injection_parameters=inj,
    outdir=outdir,
    label=label,
)

result.plot_corner()

print("[DONE] Sampling finished.")
