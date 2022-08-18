"""
List of servers for the ARPES lab
Structure:
{NAME:[server_ip(must be static!!!), Port, COM-port, Driver, pressure_index in received string,color of the display]}
"""
import socket  # temporary

temporary_ip = socket.gethostbyname(socket.gethostname())

server_list = dict(
                    OXIDATION_CHAMBER=[temporary_ip, 63207, 'COM22', "Driver_Pfeiffer_TPG261", 0, "blue"],
                    LAKESHORE_T_A=[temporary_ip, 63205, 'COM20', "Driver_Lakeshore", 0, "orange"],
                    ANALYSIS_CHAMBER=[temporary_ip, 63202, 'COM104', "Driver_AML", 0, "green"],
                    PREPARATION_CHAMBER=[temporary_ip, 63200, 'COM99', "Driver_Agilent", 1, "red"],
                    DISTRIBUTION_CHAMBER=[temporary_ip, 63206, 'COM105', "Driver_Pfeiffer_TPG261", 0, "darkviolet"],
                    HE_CHAMBER=[temporary_ip, 63201, 'COM106', "Driver_Leybold", 1, "white"],
                    LOAD_LOCK_CHAMBER=[temporary_ip, 63201, 'COM106', "Driver_Leybold", 0, "orange"],
                   )