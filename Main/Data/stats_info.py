from Main.Data.structs import Stat, Range

DEFAULT_NUM_PIXELS = 1704

PUMP_INFO = {
             "Turbo Power(Watts)": Stat(good_ranges=(Range(3, 4),), tolerable_ranges=(Range(5, 7),), unsafe_ranges=(Range(0, 2), Range(8, 29))),
             "Turbo Current (Amps)": Stat(good_ranges=(Range(0, .12),), tolerable_ranges=(), unsafe_ranges=(.12, 1.03)),
             "Turbo Pressure (Torr)": Stat(good_ranges=(Range(0, 5 * pow(10.0, -5.0)),),
                                               tolerable_ranges=(Range(5 * pow(10.0, -5.0), 7 * pow(10.0, -5.0)), ),
                                               unsafe_ranges=(Range(7 * pow(10.0, -5.0), 1000), )),
             "Turbo Rotational Speed (Hz)": Stat(good_ranges=(Range(1499, 1500),), tolerable_ranges=(Range(1400, 1499),), unsafe_ranges=(Range(0, 1400),)),
             "Rough Speed (Hz)": Stat(good_ranges=(Range(20, 30),), tolerable_ranges=(), unsafe_ranges=(Range(0, 20), Range(31, 50))),
             "Rough Power (Watts)": Stat(good_ranges=(Range(7, 10),), tolerable_ranges=(), unsafe_ranges=(Range(0, 7), Range(11, 14)))
            }

PUMP_PROPERTIES = list(PUMP_INFO.keys())
PUMP_STAT_COLUMNS = 2
PUMP_FRAME_LABEL = "Pump Status"

VOLTAGE_INFO = {
                "Main 24v": Stat(),
                "Main 5v": Stat(),
                "Main +12v": Stat(),
                "Main -12v": Stat(),
                "Thermal Electric": Stat(),
                "TE Temp": Stat()
                }

VOLTAGE_PROPERTIES = list(VOLTAGE_INFO.keys())
VOLTAGE_STAT_COLUMNS = 2
VOLTAGE_FRAME_LABEL="Voltage Display"

ELEC_SEC_INFO = {
                "Electric Sector Positive": Stat(),
                "Electric Sector Negative": Stat()
                 }

ELEC_SEC_PROPERTIES = list(ELEC_SEC_INFO.keys())
ELEC_SEC_STAT_COLUMNS = 2
ELEC_SEC_FRAME_LABEL = "Electric Sector Status"


ALL_INFO = {**VOLTAGE_INFO, **PUMP_INFO}
ALL_INFO = {**ALL_INFO, **ELEC_SEC_INFO}

PWM_MAX_PERCENT = .5

TURBO_ADDRESS = 1
ROUGHING_ADDRESS = 0