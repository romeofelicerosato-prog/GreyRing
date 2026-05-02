# GW250114 analysis with GreyRing


######################      FIXED EVENT SETTINGS    ######################## 
#    
FIXED_PARAMS = {  # from LVK paper https://arxiv.org/pdf/2509.08054
    "luminosity_distance": 403,
    "theta_jn": 0.78,
    "psi": 1.329,
    "ra": 2.333,
    "dec": 0.190,
    "geocent_time": 1420878141.235932,
}
  
############################      IMPORTS     ##############################
  
import bilby
import numpy as np
from gwpy.timeseries import TimeSeries

from greyring.waveforms import greyring_22_free_ampl_phase

#######################      INITIAL SETTINGS     ##########################

logger = bilby.core.utils.logger
outdir = "outdir"
label = "GW250114_greyring"

trigger_time = FIXED_PARAMS["geocent_time"]
detectors = ["H1", "L1"]

# Ringdown analysis band (Hz)
minimum_frequency = 120
maximum_frequency = 512

roll_off = 0.4  # duration (s) of the tapering at the edges of the Tukey window used below
duration = 4
post_trigger_duration = 2 

end_time = trigger_time + post_trigger_duration
start_time = end_time - duration

psd_duration = 32 * duration
psd_start_time = start_time - psd_duration
psd_end_time = start_time


####################      DATA AND INTERFEROMETERS    ######################

ifo_list = bilby.gw.detector.InterferometerList([])

for det in detectors:
    logger.info(f"Downloading analysis data for ifo {det}")
    ifo = bilby.gw.detector.get_empty_interferometer(det)

    data = TimeSeries.fetch_open_data(det, start_time, end_time)
    ifo.strain_data.set_from_gwpy_timeseries(data)

    logger.info(f"Downloading PSD data for ifo {det}")
    psd_data = TimeSeries.fetch_open_data(det, psd_start_time, psd_end_time)
    psd_alpha = 2 * roll_off / duration

    psd = psd_data.psd(
        fftlength=duration,
        overlap=0,
        window=("tukey", psd_alpha),
        method="median",
    )

    ifo.power_spectral_density = bilby.gw.detector.PowerSpectralDensity(
        frequency_array=psd.frequencies.value,
        psd_array=psd.value,
    )

    ifo.minimum_frequency = minimum_frequency
    ifo.maximum_frequency = maximum_frequency
    ifo_list.append(ifo)

bilby.core.utils.check_directory_exists_and_if_not_mkdir(outdir)
ifo_list.plot_data(outdir=outdir, label=label)

############################      PRIORS     ###############################

priors = bilby.core.prior.PriorDict()

# Priors for intrinsic GreyRing parameters, slightly larger of the injection ones
priors["final_mass"] = bilby.core.prior.Uniform(50.0, 100.0, name="final_mass")
priors["final_spin"] = bilby.core.prior.Uniform(0.0, 0.99, name="final_spin")
priors["A"] = bilby.core.prior.Uniform(0.0, 15.0, name="A")
priors["p"] = bilby.core.prior.Uniform(-0.5, 1.5, name="p")
priors["c"] = bilby.core.prior.Uniform(0.0, 3.0, name="c")

# Extrinsic parameters (source model / detector response)
priors["luminosity_distance"] = FIXED_PARAMS["luminosity_distance"]
# Here the inclination is fixed. Sampling over it does not influence results on the intrinsic parameters
# final_mass, final_spin, p, c. Only A is slightly affected.

#priors["theta_jn"] = bilby.core.prior.Sine(name="theta_jn")
priors["theta_jn"] = FIXED_PARAMS["theta_jn"]

priors["ra"] = FIXED_PARAMS["ra"]
priors["dec"] = FIXED_PARAMS["dec"]

# Polarization angle
# Here the polarization angle is fixed. Sampling over it has the same effect of sampling over the inclination.

#priors["psi"] = bilby.core.prior.Uniform(-np.pi / 2, np.pi / 2, name="psi", boundary="periodic")
priors["psi"] = FIXED_PARAMS["psi"]

priors["phase"] = bilby.core.prior.Uniform(-np.pi, np.pi, name="phase", boundary="periodic")

priors["geocent_time"] = bilby.core.prior.Uniform(trigger_time - 0.01, trigger_time + 0.01,name="geocent_time")

######################      WAVEFORM GENERATOR     #########################

def identity_map_conversion(parameters):
    return parameters, [] #identity transformation

waveform_generator = bilby.gw.WaveformGenerator(
    frequency_domain_source_model=greyring_22_free_ampl_phase,
    parameter_conversion=identity_map_conversion,
    waveform_arguments={},
)

##########################      LIKELIHOOD     #############################

likelihood = bilby.gw.likelihood.GravitationalWaveTransient(
    interferometers=ifo_list,
    waveform_generator=waveform_generator,
    priors=priors,
    time_marginalization=True,
    phase_marginalization=True,
    distance_marginalization=False,
)

##############################      RUN    #################################

result = bilby.run_sampler(
    likelihood=likelihood,
    priors=priors,
    sampler="dynesty",
    outdir=outdir,
    label=label,
    nlive=1000,
    check_point_delta_t=600,
    check_point_plot=True,
    npool=32,
    queue_size=32,
    resume=True,
)

result.plot_corner()
