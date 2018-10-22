
import glob
from hypoddpy import HypoDDRelocator

relocator = HypoDDRelocator(working_dir="Hangay378_cc_relocator_working_dir",
    cc_time_before=0.20,
    cc_time_after=0.80,
    cc_maxlag=0.3,
    cc_filter_min_freq=1.0,
    cc_filter_max_freq=10.0,
    cc_p_phase_weighting={"Z": 1.0},
    cc_s_phase_weighting={"Z": 1.0, "E": 1.0, "N": 1.0},
    cc_min_allowed_cross_corr_coeff=0.6)


dlseed="/data2/WORK/Mongolia/Workshop2018/EQ/RUN/XL_dataless_noHD20AHD47A"
relocator.add_station_files(glob.glob(dlseed))
relocator._parse_station_files()
relocator._write_station_input_file()

efls="/home/stach/Work/Mongolia/Workshop2018/EQ/db_from_tomo/qml_files_evtsubdb/*"
relocator.add_event_files(glob.glob(efls))
relocator._read_event_information()

relocator._write_ph2dt_inp_file()

relocator._create_event_id_map()

relocator._write_catalog_input_file()

relocator._compile_hypodd()

relocator._run_ph2dt()

#msdir = "/home/stach/Work/Mongolia/Workshop2018/EQ/db_from_tomo/MSEED"
msdir = "/home/stach/Work/Mongolia/Workshop2018/EQ/db_from_tomo/MSEED_evtsubdb_v1"
relocator.add_waveform_files(glob.glob(msdir+"/*/*"))
relocator._parse_waveform_files()
output_cross_correlation_file='out_cc.txt'
relocator._cross_correlate_picks(outfile=output_cross_correlation_file)

