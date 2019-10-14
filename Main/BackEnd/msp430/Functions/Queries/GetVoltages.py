from Main.BackEnd.msp430.Functions.Queries.Query import Query
import Main.BackEnd.msp430.Library.commands as commands
import Main.Data.stats_info as stats

class GetVoltages(Query):

    def __init__(self):
        super().__init__(command=commands.GET_ANALOG_DIGITAL_SYST_DEFAULTS)

    def parse(self, response):
        voltages=response.split(" ")
        v_24 = str(float(voltages[1])/3904.0*24.0)
        v_5 = str(float(voltages[2])/4095.0*5.0)
        v_pos_12 = str(float(voltages[3])/4095.0*12.0)
        v_neg_12 = str(float(voltages[4])/3591.0*-12.0)
        v_te = voltages[5]
        te_temp = voltages[10]
        return {
            stats.VOLTAGE_PROPERTIES[0]: v_24,
            stats.VOLTAGE_PROPERTIES[1]: v_5,
            stats.VOLTAGE_PROPERTIES[2]: v_pos_12,
            stats.VOLTAGE_PROPERTIES[3]: v_neg_12,
            stats.VOLTAGE_PROPERTIES[4]: v_te,
            stats.VOLTAGE_PROPERTIES[5]: te_temp
                }