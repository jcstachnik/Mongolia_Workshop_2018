

import glob
from hypoddpy import HypoDDRelocator


gsefile = "/data2/WORK/Mongolia/Workshop2018/EQ/WEEK_1/Vel_out/hyp-hangay.out"

relocator = HypoDDRelocator(working_dir="HangayIAG_relocator_working_dir",
    cc_time_before=0.20,
    cc_time_after=0.8,
    cc_maxlag=0.3,
    cc_filter_min_freq=1.0,
    cc_filter_max_freq=10.0,
    cc_p_phase_weighting={"Z": 1.0},
    cc_s_phase_weighting={"Z": 1.0, "E": 1.0, "N": 1.0},
    cc_min_allowed_cross_corr_coeff=0.6)

dldir = "/data2/WORK/Mongolia/Workshop2018/EQ/WEEK_1/3_RESPONSE/DATALESS"
relocator.add_station_files(glob.glob(dldir+'/AFTAC/*.seed'))
#relocator.add_station_files(glob.glob(dldir+'/Khangay_experiment/XL_Mongolia_dataless_2014265'))
relocator.add_station_files(glob.glob('/data2/WORK/Mongolia/Workshop2018/EQ/RUN/XL_dataless_noHD20AHD47A'))
relocator.add_station_files(glob.glob(dldir+'/Regional/*.seed'))
relocator.add_station_files(glob.glob(dldir+'/UB_network/*.seed'))
relocator._parse_station_files()

newstations = {}
for k,v in relocator.stations.items():
    st = k.split('.')[1]
    nk = 'NA.'+st
    newstations[nk] = v

relocator.stations = newstations

relocator._write_station_input_file()

relocator.add_event_files(glob.glob(gsefile))
relocator._read_event_information()

relocator._write_ph2dt_inp_file()

relocator._create_event_id_map()
relocator._write_catalog_input_file()

relocator._compile_hypodd()

relocator._run_ph2dt()

wfdir = "/data2/WORK/Mongolia/Workshop2018/EQ/WEEK_1/5_SAC/Sac_HANGAY"
relocator.add_waveform_files(glob.glob(wfdir+"/*/*/*"))
relocator._parse_waveform_files()
output_cross_correlation_file='HangayIAG_relocator_working_dir/out_cc.txt'
relocator._cross_correlate_picks(outfile=output_cross_correlation_file)

