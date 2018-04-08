#!/usr/bin/env python
"""
Eastron SDM630-Modbus 100A 3P4W SW:1.3 Smart Meter Three Phase Electrical System. The Python plugin for Domoticz
Author: MFxMF
Requirements: 
    1.python module minimalmodbus -> http://minimalmodbus.readthedocs.io/en/master/
        (pi@raspberrypi:~$ sudo pip3 install minimalmodbus)
    2.Communication module Modbus USB to RS485 converter module
"""
"""
<plugin key="SDM630" name="Eastron SDM630-Modbus" version="1.0.0" author="MFxMF">
    <params>
        <param field="SerialPort" label="Modbus Port" width="200px" required="true" default="/dev/ttyUSB0" />
        <param field="Mode1" label="Baud rate" width="40px" required="true" default="9600"  />
        <param field="Mode2" label="Device ID" width="40px" required="true" default="1" />
        <param field="Mode3" label="Reading Interval min." width="40px" required="true" default="1" />
        <param field="Mode6" label="Debug" width="75px">
            <options>
                <option label="True" value="Debug"/>
                <option label="False" value="Normal"  default="true" />
            </options>
        </param>
    </params>
</plugin>

"""

import minimalmodbus
import serial
import Domoticz
from datetime import datetime, timedelta
import time


class BasePlugin:
    def __init__(self):
        self.runInterval = 1
        self.rs485 = "" 
        return

    def onStart(self):
        self.rs485 = minimalmodbus.Instrument(Parameters["SerialPort"], int(Parameters["Mode2"]))
        self.rs485.serial.baudrate = Parameters["Mode1"]
        self.rs485.serial.bytesize = 8
        self.rs485.serial.parity = minimalmodbus.serial.PARITY_NONE
        self.rs485.serial.stopbits = 1
        self.rs485.serial.timeout = 1
        self.rs485.debug = False
                          

        self.rs485.mode = minimalmodbus.MODE_RTU
        devicecreated = []
        Domoticz.Log("Eastron SDM630 Modbus plugin start")
        self.runInterval = int(Parameters["Mode3"]) * 1 
        if 1 not in Devices:
            Domoticz.Device(Name="Voltage L1", Unit=1,TypeName="Voltage",Used=0).Create()
        if 2 not in Devices:
            Domoticz.Device(Name="Voltage L2", Unit=2,TypeName="Voltage",Used=0).Create()
        if 3 not in Devices:
            Domoticz.Device(Name="Voltage L3", Unit=3,TypeName="Voltage",Used=0).Create()
        if 4 not in Devices:
            Domoticz.Device(Name="Current L1,L2,L3", Unit=4,TypeName="Current/Ampere",Used=0).Create()
        if 5 not in Devices:
            Domoticz.Device(Name="Active Power L1", Unit=5,TypeName="Usage",Used=0).Create()
        if 6 not in Devices:
            Domoticz.Device(Name="Active Power L2", Unit=6,TypeName="Usage",Used=0).Create()
        if 7 not in Devices:
            Domoticz.Device(Name="Active Power L3", Unit=7,TypeName="Usage",Used=0).Create()
        Options = { "Custom" : "1;VA"} 
        if 8 not in Devices:
            Domoticz.Device(Name="Apparent Power L1", Unit=8,TypeName="Custom",Used=0,Options=Options).Create()
        if 9 not in Devices:
            Domoticz.Device(Name="Apparent Power L2", Unit=9,TypeName="Custom",Used=0,Options=Options).Create()
        if 10 not in Devices:
            Domoticz.Device(Name="Apparent Power L3", Unit=10,TypeName="Custom",Used=0,Options=Options).Create()
        if 11 not in Devices:
            Domoticz.Device(Name="Power Meter L1", Unit=11,TypeName="General",Subtype=0x1D,Used=0).Create()
        if 12 not in Devices:
            Domoticz.Device(Name="Power Meter L2", Unit=12,TypeName="General",Subtype=0x1D,Used=0).Create()
        if 13 not in Devices:
            Domoticz.Device(Name="Power Meter L3", Unit=13,TypeName="General",Subtype=0x1D,Used=0).Create()
        Options = { "Custom" : "1;VAr"} 
        if 14 not in Devices:
            Domoticz.Device(Name="Reactive Power L1", Unit=14,TypeName="Custom",Used=0,Options=Options).Create()
        if 15 not in Devices:
            Domoticz.Device(Name="Reactive Power L2", Unit=15,TypeName="Custom",Used=0,Options=Options).Create()
        if 16 not in Devices:
            Domoticz.Device(Name="Reactive Power L3", Unit=16,TypeName="Custom",Used=0,Options=Options).Create()
        Options = { "Custom" : "1;PF"} 
        if 17 not in Devices:
            Domoticz.Device(Name="Power Factor L1", Unit=17,TypeName="Custom",Used=0,Options=Options).Create()
        if 18 not in Devices:
            Domoticz.Device(Name="Power Factor L2", Unit=18,TypeName="Custom",Used=0,Options=Options).Create()
        if 19 not in Devices:
            Domoticz.Device(Name="Power Factor L3", Unit=19,TypeName="Custom",Used=0,Options=Options).Create()
        Options = { "Custom" : "1;Degrees"} 
        if 20 not in Devices:
            Domoticz.Device(Name="Phase Angle L1", Unit=20,TypeName="Custom",Used=0,Options=Options).Create()
        if 21 not in Devices:
            Domoticz.Device(Name="Phase Angle L2", Unit=21,TypeName="Custom",Used=0,Options=Options).Create()
        if 22 not in Devices:
            Domoticz.Device(Name="Phase Angle L3", Unit=22,TypeName="Custom",Used=0,Options=Options).Create()
        if 23 not in Devices:
            Domoticz.Device(Name="Average Line To Neutral Volts", Unit=23,TypeName="Voltage",Used=0).Create()
        if 24 not in Devices:
            Domoticz.Device(Name="Average Line Current", Unit=24,TypeName="Current (Single)",Used=0).Create()
        if 25 not in Devices:
            Domoticz.Device(Name="Sum of Line Currents", Unit=25,TypeName="Current (Single)",Used=0).Create()
        if 26 not in Devices:
            Domoticz.Device(Name="Total System Active Power", Unit=26,TypeName="Usage",Used=0).Create()
        Options = { "Custom" : "1;VA"} 
        if 27 not in Devices:
            Domoticz.Device(Name="Total System Apparent Power", Unit=27,TypeName="Custom",Used=0,Options=Options).Create()
        Options = { "Custom" : "1;VAr"} 
        if 28 not in Devices:
            Domoticz.Device(Name="Total System Reactive Power", Unit=28,TypeName="Custom",Used=0,Options=Options).Create()
        Options = { "Custom" : "1;PF"} 
        if 29 not in Devices:
            Domoticz.Device(Name="Total System Power Factor", Unit=29,TypeName="Custom",Used=0,Options=Options).Create()
        Options = { "Custom" : "1;Degrees"} 
        if 30 not in Devices:
            Domoticz.Device(Name="Total System Phase Angle", Unit=30,TypeName="Custom",Used=0,Options=Options).Create()
        Options = { "Custom" : "1;Hz"} 
        if 31 not in Devices:
            Domoticz.Device(Name="Frequency of supply voltages", Unit=31,TypeName="Custom",Used=0,Options=Options).Create()
        if 32 not in Devices:
            Domoticz.Device(Name="Import Wh since last reset", Unit=32,Type=0x71,Subtype=0x0,Used=0).Create()
        if 33 not in Devices:
            Domoticz.Device(Name="Export Wh since last reset", Unit=33,Type=0x71,Subtype=0x0,Used=0).Create()
        Options = { "Custom" : "1;kVArh"} 
        if 34 not in Devices:
            Domoticz.Device(Name="Import VArh since last reset", Unit=34,TypeName="Custom",Used=0,Options=Options).Create()
        Options = { "Custom" : "1;kVArh"} 
        if 35 not in Devices:
            Domoticz.Device(Name="Export VArh since last reset", Unit=35,TypeName="Custom",Used=0,Options=Options).Create()
        Options = { "Custom" : "1;kVAh"} 
        if 36 not in Devices:
            Domoticz.Device(Name="VAh since last reset", Unit=36,TypeName="Custom",Used=0,Options=Options).Create()
        Options = { "Custom" : "1;Ah"} 
        if 37 not in Devices:
            Domoticz.Device(Name="Ah since last reset", Unit=37,TypeName="Custom",Used=0,Options=Options).Create()
        if 38 not in Devices:
            Domoticz.Device(Name="Total system power demand", Unit=38,TypeName="Usage",Used=0).Create()
        Options = { "Custom" : "1;VA"} 
        if 39 not in Devices:
            Domoticz.Device(Name="Maximum total system power demand", Unit=39,TypeName="Custom",Used=0,Options=Options).Create()
        Options = { "Custom" : "1;VA"} 
        if 40 not in Devices:
            Domoticz.Device(Name="Total system VA demand", Unit=40,TypeName="Custom",Used=0,Options=Options).Create()
        Options = { "Custom" : "1;VA"} 
        if 41 not in Devices:
            Domoticz.Device(Name="Maximum total system VA demand", Unit=41,TypeName="Custom",Used=0,Options=Options).Create()
        if 42 not in Devices:
            Domoticz.Device(Name="Neutral current demand", Unit=42,TypeName="Current (Single)",Used=0).Create()
        if 43 not in Devices:
            Domoticz.Device(Name="Maximum neutral current demand", Unit=43,TypeName="Current (Single)",Used=0).Create()
        if 44 not in Devices:
            Domoticz.Device(Name="Line 1 to Line 2 volts", Unit=44,TypeName="Voltage",Used=0).Create()
        if 45 not in Devices:
            Domoticz.Device(Name="Line 2 to Line 3 volts", Unit=45,TypeName="Voltage",Used=0).Create()
        if 46 not in Devices:
            Domoticz.Device(Name="Line 3 to Line 1 volts", Unit=46,TypeName="Voltage",Used=0).Create()
        if 47 not in Devices:
            Domoticz.Device(Name="Average line to line volts", Unit=47,TypeName="Voltage",Used=0).Create()
        if 48 not in Devices:
            Domoticz.Device(Name="Neutral current", Unit=48,TypeName="Current (Single)",Used=0).Create()
        if 49 not in Devices:
            Domoticz.Device(Name="Phase 1 L/N volts THD", Unit=49,TypeName="General",Subtype=0x06,Used=0).Create()
        if 50 not in Devices:
            Domoticz.Device(Name="Phase 2 L/N volts THD", Unit=50,TypeName="General",Subtype=0x06,Used=0).Create()
        if 51 not in Devices:
            Domoticz.Device(Name="Phase 3 L/N volts THD", Unit=51,TypeName="General",Subtype=0x06,Used=0).Create()
        if 52 not in Devices:
            Domoticz.Device(Name="Phase 1 Current THD", Unit=52,TypeName="General",Subtype=0x06,Used=0).Create()
        if 53 not in Devices:
            Domoticz.Device(Name="Phase 2 Current THD", Unit=53,TypeName="General",Subtype=0x06,Used=0).Create()
        if 54 not in Devices:
            Domoticz.Device(Name="Phase 3 Current THD", Unit=54,TypeName="General",Subtype=0x06,Used=0).Create()
        if 55 not in Devices:
            Domoticz.Device(Name="Average line to neutral volts THD", Unit=55,TypeName="General",Subtype=0x06,Used=0).Create()
        if 56 not in Devices:
            Domoticz.Device(Name="Average line current THD", Unit=56,TypeName="General",Subtype=0x06,Used=0).Create()
        Options = { "Custom" : "1;Degrees"} 
        if 57 not in Devices:
            Domoticz.Device(Name="Total system power factor", Unit=57,TypeName="Custom",Used=0,Options=Options).Create()
        if 58 not in Devices:
            Domoticz.Device(Name="Phase 1 current demand", Unit=58,TypeName="Current (Single)",Used=0).Create()
        if 59 not in Devices:
            Domoticz.Device(Name="Phase 2 current demand", Unit=59,TypeName="Current (Single)",Used=0).Create()
        if 60 not in Devices:
            Domoticz.Device(Name="Phase 3 current demand", Unit=60,TypeName="Current (Single)",Used=0).Create()
        if 61 not in Devices:
            Domoticz.Device(Name="Maximum phase 1 current demand", Unit=61,TypeName="Current (Single)",Used=0).Create()
        if 62 not in Devices:
            Domoticz.Device(Name="Maximum phase 2 current demand", Unit=62,TypeName="Current (Single)",Used=0).Create()
        if 63 not in Devices:
            Domoticz.Device(Name="Maximum phase 3 current demand", Unit=63,TypeName="Current (Single)",Used=0).Create()
        if 64 not in Devices:
            Domoticz.Device(Name="Line 1 to line 2 volts THD", Unit=64,TypeName="General",Subtype=0x06,Used=0).Create()
        if 65 not in Devices:
            Domoticz.Device(Name="Line 2 to line 3 volts THD", Unit=65,TypeName="General",Subtype=0x06,Used=0).Create()
        if 66 not in Devices:
            Domoticz.Device(Name="Line 3 to line 1 volts THD", Unit=66,TypeName="General",Subtype=0x06,Used=0).Create()
        if 67 not in Devices:
            Domoticz.Device(Name="Average line to line volts THD", Unit=67,TypeName="General",Subtype=0x06,Used=0).Create()
        if 68 not in Devices:
            Domoticz.Device(Name="Total kWh", Unit=68,Type=0x71,Subtype=0x0,Used=0).Create()
        Options = { "Custom" : "1;kVArh"} 
        if 69 not in Devices:
            Domoticz.Device(Name="Total kVArh", Unit=69,TypeName="Custom",Used=0,Options=Options).Create()
        if 70 not in Devices:
            Domoticz.Device(Name="L1 import kWh", Unit=70,Type=0x71,Subtype=0x0,Used=0).Create()
        if 71 not in Devices:
            Domoticz.Device(Name="L2 import kWh", Unit=71,Type=0x71,Subtype=0x0,Used=0).Create()
        if 72 not in Devices:
            Domoticz.Device(Name="L3 import kWh", Unit=72,Type=0x71,Subtype=0x0,Used=0).Create()
        if 73 not in Devices:
            Domoticz.Device(Name="L1 export kWh", Unit=73,Type=0x71,Subtype=0x0,Used=0).Create()
        if 74 not in Devices:
            Domoticz.Device(Name="L2 export kWh", Unit=74,Type=0x71,Subtype=0x0,Used=0).Create()
        if 75 not in Devices:
            Domoticz.Device(Name="L3 export kWh", Unit=75,Type=0x71,Subtype=0x0,Used=0).Create()
        if 76 not in Devices:
            Domoticz.Device(Name="L1 total kWh", Unit=76,Type=0x71,Subtype=0x0,Used=0).Create()
        if 77 not in Devices:
            Domoticz.Device(Name="L2 total kWh", Unit=77,Type=0x71,Subtype=0x0,Used=0).Create()
        if 78 not in Devices:
            Domoticz.Device(Name="L3 total kWh", Unit=78,Type=0x71,Subtype=0x0,Used=0).Create()
        Options = { "Custom" : "1;kVArh"} 
        if 79 not in Devices:
            Domoticz.Device(Name="L1 import kVArh", Unit=79,TypeName="Custom",Used=0,Options=Options).Create()
        Options = { "Custom" : "1;kVArh"} 
        if 80  not in Devices:
            Domoticz.Device(Name="L2 import kVArh", Unit=80,TypeName="Custom",Used=0,Options=Options).Create()
        Options = { "Custom" : "1;kVArh"} 
        if 81 not in Devices:
            Domoticz.Device(Name="L3 import kVArh", Unit=81,TypeName="Custom",Used=0,Options=Options).Create()
        Options = { "Custom" : "1;kVArh"} 
        if 82 not in Devices:
            Domoticz.Device(Name="L3 export kVArh", Unit=82,TypeName="Custom",Used=0,Options=Options).Create()
        Options = { "Custom" : "1;kVArh"} 
        if 83 not in Devices:
            Domoticz.Device(Name="L3 export kVArh", Unit=83,TypeName="Custom",Used=0,Options=Options).Create()
        Options = { "Custom" : "1;kVArh"} 
        if 84 not in Devices:
            Domoticz.Device(Name="L3 export kVArh", Unit=84,TypeName="Custom",Used=0,Options=Options).Create()
        Options = { "Custom" : "1;kVArh"} 
        if 85 not in Devices:
            Domoticz.Device(Name="L1 total kVArh", Unit=85,TypeName="Custom",Used=0,Options=Options).Create()
        Options = { "Custom" : "1;kVArh"} 
        if 86 not in Devices:
            Domoticz.Device(Name="L2 total kVArh", Unit=86,TypeName="Custom",Used=0,Options=Options).Create()
        Options = { "Custom" : "1;kVArh"} 
        if 87 not in Devices:
            Domoticz.Device(Name="L3 total kVArh", Unit=87,TypeName="Custom",Used=0,Options=Options).Create()
        if 88 not in Devices:
            Domoticz.Device(Name="Total Power Meter", Unit=88,TypeName="General",Subtype=0x1D,Used=0).Create()


    def onStop(self):
        Domoticz.Log("Eastron SDM630 Modbus plugin stop")

    def onHeartbeat(self):
        self.runInterval -=1;
        if self.runInterval <= 0:
            # Get data from SDM630
            Volts_L1 = self.rs485.read_float(0, functioncode=4, numberOfRegisters=2)
            Volts_L2 = self.rs485.read_float(2, functioncode=4, numberOfRegisters=2)
            Volts_L3 = self.rs485.read_float(4, functioncode=4, numberOfRegisters=2)
            Current_L1 = self.rs485.read_float(6, functioncode=4, numberOfRegisters=2)
            Current_L2 = self.rs485.read_float(8, functioncode=4, numberOfRegisters=2)
            Current_L3 = self.rs485.read_float(10, functioncode=4, numberOfRegisters=2)
            Active_Power_L1 = self.rs485.read_float(12, functioncode=4, numberOfRegisters=2)
            Active_Power_L2 = self.rs485.read_float(14, functioncode=4, numberOfRegisters=2)
            Active_Power_L3 = self.rs485.read_float(16, functioncode=4, numberOfRegisters=2)
            Apparent_Power_L1 = self.rs485.read_float(18, functioncode=4, numberOfRegisters=2)
            Apparent_Power_L2 = self.rs485.read_float(20, functioncode=4, numberOfRegisters=2)
            Apparent_Power_L3 = self.rs485.read_float(22, functioncode=4, numberOfRegisters=2)
            Reactive_Power_L1 = self.rs485.read_float(24, functioncode=4, numberOfRegisters=2)
            Reactive_Power_L2 = self.rs485.read_float(26, functioncode=4, numberOfRegisters=2)
            Reactive_Power_L3 = self.rs485.read_float(28, functioncode=4, numberOfRegisters=2)
            Power_Factor_L1 = self.rs485.read_float(30, functioncode=4, numberOfRegisters=2)
            Power_Factor_L2 = self.rs485.read_float(32, functioncode=4, numberOfRegisters=2)
            Power_Factor_L3 = self.rs485.read_float(34, functioncode=4, numberOfRegisters=2)
            Phase_Angle_L1 = self.rs485.read_float(36, functioncode=4, numberOfRegisters=2)
            Phase_Angle_L2 = self.rs485.read_float(38, functioncode=4, numberOfRegisters=2)
            Phase_Angle_L3 = self.rs485.read_float(40, functioncode=4, numberOfRegisters=2)
            Average_line_to_neutral_volts = self.rs485.read_float(42, functioncode=4,numberOfRegisters=2)
            Average_line_current = self.rs485.read_float(46, functioncode=4,numberOfRegisters=2)
            Sum_of_line_current = self.rs485.read_float(48, functioncode=4,numberOfRegisters=2)
            Total_System_Active_Power = self.rs485.read_float(52, functioncode=4,numberOfRegisters=2)
            Total_System_Apparent_Power = self.rs485.read_float(56, functioncode=4,numberOfRegisters=2)
            Total_System_Reactive_Power = self.rs485.read_float(60, functioncode=4,numberOfRegisters=2)
            Total_System_Power_Factor = self.rs485.read_float(62, functioncode=4,numberOfRegisters=2)
            Total_System_Phase_Angle = self.rs485.read_float(66, functioncode=4, numberOfRegisters=2)
            Frequency_Of_Supply_Voltages = self.rs485.read_float(70, functioncode=4, numberOfRegisters=2)
            Import_Wh_since_last_reset = self.rs485.read_float(72, functioncode=4, numberOfRegisters=2)
            Export_Wh_since_last_reset = self.rs485.read_float(74, functioncode=4, numberOfRegisters=2)
            Import_VArh_since_last_reset = self.rs485.read_float(76, functioncode=4, numberOfRegisters=2)
            Export_VArh_since_last_reset = self.rs485.read_float(78, functioncode=4, numberOfRegisters=2)
            VAh_since_last_reset = self.rs485.read_float(80, functioncode=4, numberOfRegisters=2)
            Ah_since_last_reset = self.rs485.read_float(82, functioncode=4, numberOfRegisters=2)
            Total_system_power_demand = self.rs485.read_float(84, functioncode=4, numberOfRegisters=2)
            Maximum_total_system_power_demand = self.rs485.read_float(86, functioncode=4, numberOfRegisters=2)
            Total_system_VA_demand = self.rs485.read_float(100, functioncode=4, numberOfRegisters=2)
            Maximum_total_system_VA_demand = self.rs485.read_float(102, functioncode=4, numberOfRegisters=2)
            Neutral_current_demand = self.rs485.read_float(104, functioncode=4, numberOfRegisters=2)
            Maximum_neutral_current_demand = self.rs485.read_float(106, functioncode=4, numberOfRegisters=2)
            Line_1_to_Line_2_volts = self.rs485.read_float(200, functioncode=4, numberOfRegisters=2)
            Line_2_to_Line_3_volts = self.rs485.read_float(202, functioncode=4, numberOfRegisters=2)
            Line_3_to_Line_1_volts = self.rs485.read_float(204, functioncode=4, numberOfRegisters=2)
            Average_line_to_line_volts = self.rs485.read_float(206, functioncode=4, numberOfRegisters=2)
            Neutral_current = self.rs485.read_float(224, functioncode=4, numberOfRegisters=2)
            Phase_1_LN_volts_THD = self.rs485.read_float(234, functioncode=4, numberOfRegisters=2)
            Phase_2_LN_volts_THD = self.rs485.read_float(236, functioncode=4, numberOfRegisters=2)
            Phase_3_LN_volts_THD = self.rs485.read_float(238, functioncode=4, numberOfRegisters=2)
            Phase_1_Current_THD = self.rs485.read_float(240, functioncode=4, numberOfRegisters=2)
            Phase_2_Current_THD = self.rs485.read_float(242, functioncode=4, numberOfRegisters=2)
            Phase_3_Current_THD = self.rs485.read_float(244, functioncode=4, numberOfRegisters=2)
            Average_line_to_neutral_volts_THD = self.rs485.read_float(248, functioncode=4, numberOfRegisters=2)
            Average_line_current_THD = self.rs485.read_float(250, functioncode=4, numberOfRegisters=2)
            Total_system_power_factor = self.rs485.read_float(254, functioncode=4, numberOfRegisters=2)
            Phase_1_current_demand = self.rs485.read_float(258, functioncode=4, numberOfRegisters=2)
            Phase_2_current_demand = self.rs485.read_float(260, functioncode=4, numberOfRegisters=2)
            Phase_3_current_demand = self.rs485.read_float(262, functioncode=4, numberOfRegisters=2)
            Maximum_phase_1_current_demand = self.rs485.read_float(264, functioncode=4, numberOfRegisters=2)
            Maximum_phase_2_current_demand = self.rs485.read_float(266, functioncode=4, numberOfRegisters=2)
            Maximum_phase_3_current_demand = self.rs485.read_float(268, functioncode=4, numberOfRegisters=2)
            Line_1_to_line_2_volts_THD = self.rs485.read_float(334, functioncode=4, numberOfRegisters=2)
            Line_2_to_line_3_volts_THD = self.rs485.read_float(336, functioncode=4, numberOfRegisters=2)
            Line_3_to_line_1_volts_THD = self.rs485.read_float(338, functioncode=4, numberOfRegisters=2)
            Average_line_to_line_volts_THD = self.rs485.read_float(340, functioncode=4, numberOfRegisters=2)
            Total_kwh = self.rs485.read_float(342, functioncode=4, numberOfRegisters=2)
            Total_kvarh = self.rs485.read_float(344, functioncode=4, numberOfRegisters=2)
            L1_import_kwh = self.rs485.read_float(346, functioncode=4, numberOfRegisters=2)
            L2_import_kwh = self.rs485.read_float(348, functioncode=4, numberOfRegisters=2)
            L3_import_kwh = self.rs485.read_float(350, functioncode=4, numberOfRegisters=2)
            L1_export_kwh = self.rs485.read_float(352, functioncode=4, numberOfRegisters=2)
            L2_export_kwh = self.rs485.read_float(354, functioncode=4, numberOfRegisters=2)
            L3_export_kwh = self.rs485.read_float(356, functioncode=4, numberOfRegisters=2)
            L1_total_kwh = self.rs485.read_float(358, functioncode=4, numberOfRegisters=2)
            L2_total_kwh = self.rs485.read_float(360, functioncode=4, numberOfRegisters=2)
            L3_total_kwh = self.rs485.read_float(362, functioncode=4, numberOfRegisters=2)
            L1_import_kvarh = self.rs485.read_float(364, functioncode=4, numberOfRegisters=2)
            L2_import_kvarh = self.rs485.read_float(366, functioncode=4, numberOfRegisters=2)
            L3_import_kvarh = self.rs485.read_float(368, functioncode=4, numberOfRegisters=2)
            L1_export_kvarh = self.rs485.read_float(370, functioncode=4, numberOfRegisters=2)
            L2_export_kvarh = self.rs485.read_float(372, functioncode=4, numberOfRegisters=2)
            L3_export_kvarh = self.rs485.read_float(374, functioncode=4, numberOfRegisters=2)
            L1_total_kvarh = self.rs485.read_float(376, functioncode=4, numberOfRegisters=2)
            L2_total_kvarh = self.rs485.read_float(378, functioncode=4, numberOfRegisters=2)
            L3_total_kvarh = self.rs485.read_float(380, functioncode=4, numberOfRegisters=2)


            #Update devices
            Devices[1].Update(0,str(Volts_L1))
            Devices[2].Update(0,str(Volts_L2))
            Devices[3].Update(0,str(Volts_L3))
            Devices[4].Update(0,str(Current_L1)+";"+str(Current_L2)+";"+str(Current_L3))
            Devices[5].Update(0,str(Active_Power_L1))
            Devices[6].Update(0,str(Active_Power_L2))
            Devices[7].Update(0,str(Active_Power_L3))
            Devices[8].Update(0,str(Apparent_Power_L1))
            Devices[9].Update(0,str(Apparent_Power_L2))
            Devices[10].Update(0,str(Apparent_Power_L3))
            Devices[11].Update(0,str(Active_Power_L1)+";"+str(Active_Power_L1))
            Devices[12].Update(0,str(Active_Power_L2)+";"+str(Active_Power_L2))
            Devices[13].Update(0,str(Active_Power_L3)+";"+str(Active_Power_L3))
            Devices[14].Update(0,str(Reactive_Power_L1))
            Devices[15].Update(0,str(Reactive_Power_L2))
            Devices[16].Update(0,str(Reactive_Power_L3))
            Devices[17].Update(0,str(Power_Factor_L1))
            Devices[18].Update(0,str(Power_Factor_L2))
            Devices[19].Update(0,str(Power_Factor_L3))
            Devices[20].Update(0,str(Phase_Angle_L1))
            Devices[21].Update(0,str(Phase_Angle_L2))
            Devices[22].Update(0,str(Phase_Angle_L3))
            Devices[23].Update(0,str(Average_line_to_neutral_volts))
            Devices[24].Update(0,str(Average_line_current))
            Devices[25].Update(0,str(Sum_of_line_current))
            Devices[26].Update(0,str(Total_System_Active_Power))
            Devices[27].Update(0,str(Total_System_Apparent_Power))
            Devices[28].Update(0,str(Total_System_Reactive_Power))
            Devices[29].Update(0,str(Total_System_Power_Factor))
            Devices[30].Update(0,str(Total_System_Phase_Angle))
            Devices[31].Update(0,str(Frequency_Of_Supply_Voltages))
            Devices[32].Update(0,str(Import_Wh_since_last_reset*1000))
            Devices[33].Update(0,str(Export_Wh_since_last_reset*1000))
            Devices[34].Update(0,str(Import_VArh_since_last_reset))
            Devices[35].Update(0,str(Export_VArh_since_last_reset))
            Devices[36].Update(0,str(VAh_since_last_reset))
            Devices[37].Update(0,str(Ah_since_last_reset))
            Devices[38].Update(0,str(Total_system_power_demand))
            Devices[39].Update(0,str(Maximum_total_system_power_demand))
            Devices[40].Update(0,str(Total_system_VA_demand))
            Devices[41].Update(0,str(Maximum_total_system_VA_demand))
            Devices[42].Update(0,str(Neutral_current_demand))
            Devices[43].Update(0,str(Maximum_neutral_current_demand))
            Devices[44].Update(0,str(Line_1_to_Line_2_volts))
            Devices[45].Update(0,str(Line_2_to_Line_3_volts))
            Devices[46].Update(0,str(Line_3_to_Line_1_volts))
            Devices[47].Update(0,str(Average_line_to_line_volts))
            Devices[48].Update(0,str(Neutral_current))
            Devices[49].Update(0,str(Phase_1_LN_volts_THD))
            Devices[50].Update(0,str(Phase_2_LN_volts_THD))
            Devices[51].Update(0,str(Phase_3_LN_volts_THD))
            Devices[52].Update(0,str(Phase_1_Current_THD))
            Devices[53].Update(0,str(Phase_2_Current_THD))
            Devices[54].Update(0,str(Phase_3_Current_THD))
            Devices[55].Update(0,str(Average_line_to_neutral_volts_THD))
            Devices[56].Update(0,str(Average_line_current_THD))
            Devices[57].Update(0,str(Total_system_power_factor))
            Devices[58].Update(0,str(Phase_1_current_demand))
            Devices[59].Update(0,str(Phase_2_current_demand))
            Devices[60].Update(0,str(Phase_3_current_demand))
            Devices[61].Update(0,str(Maximum_phase_1_current_demand))
            Devices[62].Update(0,str(Maximum_phase_2_current_demand))
            Devices[63].Update(0,str(Maximum_phase_3_current_demand))
            Devices[64].Update(0,str(Line_1_to_line_2_volts_THD))
            Devices[65].Update(0,str(Line_2_to_line_3_volts_THD))
            Devices[66].Update(0,str(Line_3_to_line_1_volts_THD))
            Devices[67].Update(0,str(Average_line_to_line_volts_THD))
            Devices[68].Update(0,str(Total_kwh*1000))
            Devices[69].Update(0,str(Total_kvarh))
            Devices[70].Update(0,str(L1_import_kwh*1000))
            Devices[71].Update(0,str(L2_import_kwh*1000))
            Devices[72].Update(0,str(L3_import_kwh*1000))
            Devices[73].Update(0,str(L1_export_kwh*1000))
            Devices[74].Update(0,str(L2_export_kwh*1000))
            Devices[75].Update(0,str(L3_export_kwh*1000))
            Devices[76].Update(0,str(L1_total_kwh*1000))
            Devices[77].Update(0,str(L2_total_kwh*1000))
            Devices[78].Update(0,str(L3_total_kwh*1000))
            Devices[79].Update(0,str(L1_import_kvarh))
            Devices[80].Update(0,str(L2_import_kvarh))
            Devices[81].Update(0,str(L3_import_kvarh))
            Devices[82].Update(0,str(L1_export_kvarh))
            Devices[83].Update(0,str(L2_export_kvarh))
            Devices[84].Update(0,str(L3_export_kvarh))
            Devices[85].Update(0,str(L1_total_kvarh))
            Devices[86].Update(0,str(L2_total_kvarh))
            Devices[87].Update(0,str(L3_total_kvarh))
            Devices[88].Update(0,str(Total_System_Active_Power)+";"+str(Total_System_Active_Power))


            if Parameters["Mode6"] == 'Debug':
                Domoticz.Log("Eastron SDM630 Modbus Data")
                Domoticz.Log('Voltage L1: {0:.3f} V'.format(Volts_L1))
                Domoticz.Log('Voltage L2: {0:.3f} V'.format(Volts_L2))
                Domoticz.Log('Voltage L3: {0:.3f} V'.format(Volts_L3))
                Domoticz.Log('Current L1: {0:.3f} A'.format(Current_L1))
                Domoticz.Log('Current L2: {0:.3f} A'.format(Current_L2))
                Domoticz.Log('Current L3: {0:.3f} A'.format(Current_L3))
                Domoticz.Log('Active power L1: {0:.3f} W'.format(Active_Power_L1))
                Domoticz.Log('Active power L2: {0:.3f} W'.format(Active_Power_L2))
                Domoticz.Log('Active power L3: {0:.3f} W'.format(Active_Power_L3))
                Domoticz.Log('Apparent power L1: {0:.3f} VA'.format(Apparent_Power_L1))
                Domoticz.Log('Apparent power L2: {0:.3f} VA'.format(Apparent_Power_L2))
                Domoticz.Log('Apparent power L3: {0:.3f} VA'.format(Apparent_Power_L3))
                Domoticz.Log('Reactive power L1: {0:.3f} VAr'.format(Reactive_Power_L1))
                Domoticz.Log('Reactive power L2: {0:.3f} VAr'.format(Reactive_Power_L2))
                Domoticz.Log('Reactive power L3: {0:.3f} VAr'.format(Reactive_Power_L3))
                Domoticz.Log('Power factor L1: {0:.3f}'.format(Power_Factor_L1))
                Domoticz.Log('Power factor L2: {0:.3f}'.format(Power_Factor_L2))
                Domoticz.Log('Power factor L3: {0:.3f}'.format(Power_Factor_L3))
                Domoticz.Log('Phase angle L1: {0:.3f} Degree'.format(Phase_Angle_L1))
                Domoticz.Log('Phase angle L2: {0:.3f} Degree'.format(Phase_Angle_L2))
                Domoticz.Log('Phase angle L3: {0:.3f} Degree'.format(Phase_Angle_L3))
                Domoticz.Log('Average line to neutral volts: {0:.3f} V'.format(Average_line_to_neutral_volts))
                Domoticz.Log('Average line current: {0:.3f} A'.format(Average_line_current))
                Domoticz.Log('Sum of line current: {0:.3f} A'.format(Sum_of_line_current))
                Domoticz.Log('Total system power: {0:.3f} W'.format(Total_System_Active_Power))
                Domoticz.Log('Total system apparent power: {0:.3f} VA'.format(Total_System_Apparent_Power))
                Domoticz.Log('Total system reactive  power: {0:.3f} VA'.format(Total_System_Reactive_Power))
                Domoticz.Log('Total system power factor: {0:.3f} PF'.format(Total_System_Power_Factor))
                Domoticz.Log('Total system phase angle: {0:.3f} Degree'.format(Total_System_Phase_Angle))
                Domoticz.Log('Frequency of supply voltages: {0:.3f} Hz'.format(Total_System_Phase_Angle))
                Domoticz.Log('Import Wh since last reset: {0:.3f} kWh'.format(Import_Wh_since_last_reset))
                Domoticz.Log('Export Wh since last reset: {0:.3f} kWh'.format(Export_Wh_since_last_reset))
                Domoticz.Log('Import VArh since last reset: {0:.3f} kVArh'.format(Import_VArh_since_last_reset))
                Domoticz.Log('Export VArh since last reset: {0:.3f} kVArh'.format(Export_VArh_since_last_reset))
                Domoticz.Log('VAh since last reset: {0:.3f} kVAh'.format(VAh_since_last_reset))
                Domoticz.Log('Ah since last reset: {0:.3f} Vh'.format(Ah_since_last_reset))
                Domoticz.Log('Total system power demand: {0:.3f} W'.format(Total_system_power_demand))
                Domoticz.Log('Maximum total system power_demand: {0:.3f} VA'.format(Maximum_total_system_power_demand))
                Domoticz.Log('Total system VA demand: {0:.3f} VA'.format(Total_system_VA_demand))
                Domoticz.Log('Maximum total system VA demand: {0:.3f} VA'.format(Maximum_total_system_VA_demand))
                Domoticz.Log('Neutral current demand: {0:.3f} A'.format(Neutral_current_demand))
                Domoticz.Log('Maximum neutral current demand: {0:.3f} A'.format(Maximum_neutral_current_demand))
                Domoticz.Log('Line 1 to Line 2 volts: {0:.3f} V'.format(Line_1_to_Line_2_volts))
                Domoticz.Log('Line 2 to Line 3 volts: {0:.3f} V'.format(Line_2_to_Line_3_volts))
                Domoticz.Log('Line 3 to Line 1 volts: {0:.3f} V'.format(Line_3_to_Line_1_volts))
                Domoticz.Log('Average line to line volts: {0:.3f} V'.format(Average_line_to_line_volts))
                Domoticz.Log('Neutral current: {0:.3f} A'.format(Neutral_current))
                Domoticz.Log('Phase 1 L/N volts THD: {0:.3f} %'.format(Phase_1_LN_volts_THD))
                Domoticz.Log('Phase 2 L/N volts THD: {0:.3f} %'.format(Phase_2_LN_volts_THD))
                Domoticz.Log('Phase 3 L/N volts THD: {0:.3f} %'.format(Phase_3_LN_volts_THD))
                Domoticz.Log('Phase 1 Current THD: {0:.3f} %'.format(Phase_1_Current_THD))
                Domoticz.Log('Phase 2 Current THD: {0:.3f} %'.format(Phase_2_Current_THD))
                Domoticz.Log('Phase 3 Current THD: {0:.3f} %'.format(Phase_3_Current_THD))
                Domoticz.Log('Average line to neutral volts THD: {0:.3f} %'.format(Average_line_to_neutral_volts_THD))
                Domoticz.Log('Average line current THD: {0:.3f} %' .format(Average_line_current_THD))
                Domoticz.Log('Total system power factor: {0:.3f} Degree'.format(Total_system_power_factor))
                Domoticz.Log('Phase 1 current demand: {0:.3f} A'.format(Phase_1_current_demand))
                Domoticz.Log('Phase 2 current demand: {0:.3f} A'.format(Phase_2_current_demand))
                Domoticz.Log('Phase 3 current demand: {0:.3f} A'.format(Phase_3_current_demand))
                Domoticz.Log('Maximum phase 1 current demand: {0:.3f} A'.format(Maximum_phase_1_current_demand))
                Domoticz.Log('Maximum phase 2 current demand: {0:.3f} A'.format(Maximum_phase_2_current_demand))
                Domoticz.Log('Maximum phase 3 current demand: {0:.3f} A'.format(Maximum_phase_3_current_demand))
                Domoticz.Log('Line 1 to line 2 volts THD: {0:.3f} %'.format(Line_1_to_line_2_volts_THD))
                Domoticz.Log('Line 2 to line 3 volts THD: {0:.3f} %'.format(Line_2_to_line_3_volts_THD))
                Domoticz.Log('Line 3 to line 1 volts THD: {0:.3f} %'.format(Line_3_to_line_1_volts_THD))
                Domoticz.Log('Average line to line volts THD: {0:.3f} %'.format(Average_line_to_line_volts_THD))
                Domoticz.Log('Total kWh: {0:.3f} kWh'.format(Total_kwh))
                Domoticz.Log('Total kVArh: {0:.3f} kWh'.format(Total_kvarh))
                Domoticz.Log('L1 import kWh: {0:.3f} kWh'.format(L1_import_kwh))
                Domoticz.Log('L2 import kWh: {0:.3f} kWh'.format(L2_import_kwh))
                Domoticz.Log('L3 import kWh: {0:.3f} kWh'.format(L3_import_kwh))
                Domoticz.Log('L1 export kWh: {0:.3f} kWh'.format(L1_export_kwh))
                Domoticz.Log('L2 export kWh: {0:.3f} kWh'.format(L2_export_kwh))
                Domoticz.Log('L3 export kWh: {0:.3f} kWh'.format(L3_export_kwh))
                Domoticz.Log('L1 total kWh: {0:.3f} kWh'.format(L1_total_kwh))
                Domoticz.Log('L2 total kWh: {0:.3f} kWh'.format(L2_total_kwh))
                Domoticz.Log('L3 total kWh: {0:.3f} kWh'.format(L3_total_kwh))
                Domoticz.Log('L1 import kVArh: {0:.3f} kVArh'.format(L1_import_kvarh))
                Domoticz.Log('L2 import kVArh: {0:.3f} kVArh'.format(L2_import_kvarh))
                Domoticz.Log('L3 import kVArh: {0:.3f} kVArh'.format(L3_import_kvarh))
                Domoticz.Log('L1 export kVArh: {0:.3f} kVArh'.format(L1_export_kvarh))
                Domoticz.Log('L2 export kVArh: {0:.3f} kVArh'.format(L2_export_kvarh))
                Domoticz.Log('L3 export kVArh: {0:.3f} kVArh'.format(L3_export_kvarh))
                Domoticz.Log('L1 total kvarh: {0:.3f} kVArh'.format(L1_total_kvarh))
                Domoticz.Log('L2 total kvarh: {0:.3f} kVArh'.format(L2_total_kvarh))
                Domoticz.Log('L3 total kvarh: {0:.3f} kVArh'.format(L3_total_kvarh))

            self.runInterval = int(Parameters["Mode3"]) * 6


global _plugin
_plugin = BasePlugin()


def onStart():
    global _plugin
    _plugin.onStart()


def onStop():
    global _plugin
    _plugin.onStop()


def onHeartbeat():
    global _plugin
    _plugin.onHeartbeat()

# Generic helper functions
def DumpConfigToLog():
    for x in Parameters:
        if Parameters[x] != "":
            Domoticz.Debug("'" + x + "':'" + str(Parameters[x]) + "'")
    Domoticz.Debug("Device count: " + str(len(Devices)))
    for x in Devices:
        Domoticz.Debug("Device:           " + str(x) + " - " + str(Devices[x]))
        Domoticz.Debug("Device ID:       '" + str(Devices[x].ID) + "'")
        Domoticz.Debug("Device Name:     '" + Devices[x].Name + "'")
        Domoticz.Debug("Device nValue:    " + str(Devices[x].nValue))
        Domoticz.Debug("Device sValue:   '" + Devices[x].sValue + "'")
        Domoticz.Debug("Device LastLevel: " + str(Devices[x].LastLevel))
    return
