"""
List of servers for the ARPES lab
Structure:
{NAME:[server_ip(must be static!!!), Port, COM-port, Driver, pressure_index in received string,color of the display]}
"""
import socket  # TODO: remove later - this is temporary


temporary_ip = socket.gethostbyname(socket.gethostname()) # TODO: remove later - this is temporary
server_list = dict(OXICHAMBER=[temporary_ip, 63207, 'COM22', "Driver_Pfeiffer_TPG261", 0, "blue"],
                   ANALYSISCHAMBER=["10.3.0.2", 63207, 'COM22', "Driver_Pfeiffer_TPG261", 0, "blue"],
                   PREPCHAMBER=["10.3.0.2", 63207, 'COM22', "Driver_Pfeiffer_TPG261", 0, "blue"])