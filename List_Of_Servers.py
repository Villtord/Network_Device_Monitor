"""
List of servers for ARPES computer (AC computer)
Structure: {NAME:[Port, Driver, COM-port,pressure_index in received string,color of the display]}
"""
import Driver_Pfeiffer_TPG261

server_list = {"OXICHAMBER":[63207, Driver_Pfeiffer_TPG261, 192.168.'COM22',0,"blue"]}