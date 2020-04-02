"""
List of servers for ARPES computer (AC computer)
Structure: {NAME:[server_ip, Port, COM-port, Driver, pressure_index in received string,color of the display]}
"""
import Driver_Pfeiffer_TPG261

server_list = dict(OXICHAMBER=["10.3.0.1", 63207, 'COM22', Driver_Pfeiffer_TPG261, 0, "blue"],
                   ANALYSISCHAMBER=["10.3.0.2", 63207, 'COM22', Driver_Pfeiffer_TPG261, 0, "blue"],
                   PREPCHAMBER=["10.3.0.2", 63207, 'COM22', Driver_Pfeiffer_TPG261, 0, "blue"])