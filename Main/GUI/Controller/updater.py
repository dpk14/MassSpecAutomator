from Main.BackEnd.msp430.Functions.Queries.GetPumpCurrent import GetPumpCurrent
from Main.BackEnd.msp430.Functions.Queries.GetPumpPower import GetPumpPower
from Main.BackEnd.msp430.Functions.Queries.GetPumpPressure import GetPumpPressure
from Main.BackEnd.msp430.Functions.Queries.GetPumpSpeed import GetPumpSpeed
from Main.BackEnd.msp430.Functions.Queries.GetVoltages import GetVoltages
from Main.BackEnd.msp430.Functions.Queries.Interrogate import Interrogate
from Main.Data import stats_info
from Main.GUI.Tools import defaults

WRITE_READ_DELAY = SYSTEM_DELAY = 1500
BYTES_PER_INT = 4

def connected(communicator):
    try:
        communicator.query(Interrogate())
    except:
        return False
    return True

class LoopManager:

    def __init__(self, main, communicator, stats_panel, connect_button, connection_event):
        self.main = main
        self.communicator = communicator
        self.stats_panel = stats_panel
        self.connect_button = connect_button
        self.connection_event = connection_event
        self.main.after(SYSTEM_DELAY, func=self.communication_loop)

    def communication_loop(self):
        if connected(self.communicator):
            self.update_voltages()
            #self.update_pump_stats()
        elif self.connect_button['text'] == defaults.CONNECTED:
            self.connection_event.set()
        self.main.after(SYSTEM_DELAY, self.communication_loop)

    def restore_defaults(self):
        self.stats_panel.voltage_display.reset()

    def update_voltages(self):
        query = GetVoltages()
        voltages = self.communicator.query(query)
        stats_frame = self.stats_panel.voltage_display
        stats_frame.display_stats(values=voltages)

    def update_pump_stats(self):
        turbo_power = self.communicator.query(query=GetPumpPower(pump_address=stats_info.TURBO_ADDRESS))
        turbo_current = self.communicator.execute(function=GetPumpCurrent(pump_address=stats_info.TURBO_ADDRESS))
        turbo_pressure = self.communicator.execute(function=GetPumpPressure(pump_address=stats_info.TURBO_ADDRESS))
        turbo_speed = self.communicator.execute(function=GetPumpSpeed(pump_address=stats_info.TURBO_ADDRESS))
        rough_speed = self.communicator.execute(function=GetPumpSpeed(pump_address=stats_info.ROUGHING_ADDRESS))
        rough_power = self.communicator.execute(function=GetPumpPower(pump_address=stats_info.ROUGHING_ADDRESS))
        return {
                stats_info.PUMP_PROPERTIES[0]: turbo_power,
                stats_info.PUMP_PROPERTIES[1]: turbo_current,
                stats_info.PUMP_PROPERTIES[2]: turbo_pressure,
                stats_info.PUMP_PROPERTIES[3]: turbo_speed,
                stats_info.PUMP_PROPERTIES[4]: rough_speed,
                stats_info.PUMP_PROPERTIES[5]: rough_power
                }

def generate_test_stats(stat_names=list(stats_info.ALL_INFO.keys())):    #only for debugging. Ignore this
    test_vals = {}
    for name in stat_names:
        range_set = stats_info.ALL_INFO[name]
        if len(range_set.green_ranges) > 0:
            val = (range_set.green_ranges[0].max + range_set.green_ranges[0].min) / 2
        else:
            val = 0
        test_vals[name] = val
    return test_vals
