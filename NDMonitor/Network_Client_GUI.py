# -*- coding: utf-8 -*-
"""
Universal GUI application which shows data values from the corresponding server.
To start GUI print in the command line:

path_to_and_python.exe path_to_and_Network_Client_GUI.py server_number

Here server number is an integer corresponding to the server number in List_Of_Servers.py file

Last update: 06 Arp 2020
Created on Sat Apr 21 14:12:26 2018

@author: Victor Rogalev
"""

import sys
import PyQt5.QtWidgets

from NDMonitor import Network_Client_Class
from NDMonitor import List_Of_Servers


def main(server_number):
    """
    Creates an instance of QtWidget which displays values for a given server_number from server list.
    :param server_number:
    :return:
    """
    server_name = list(List_Of_Servers.server_list.keys())[server_number]
    host = List_Of_Servers.server_list[server_name][0]
    port = List_Of_Servers.server_list[server_name][1]
    index = int(List_Of_Servers.server_list[server_name][4])
    color = List_Of_Servers.server_list[server_name][5]
    app = PyQt5.QtWidgets.QApplication(sys.argv)  # A new instance of QApplication
    form = Network_Client_Class.NetworkClientMonitor(host, port, index, color)
    form.setWindowTitle(server_name+' - client')  # Change window name
    form.resize(380, 150)  # Resize the form
    form.show()  # Show the form
    sys.exit(app.exec_())  # Handle exit case


if __name__ == '__main__':  # if we're running file directly and not importing it
    a = int(sys.argv[1])  # this is a server number which must be provided on start from the command line
    main(a)  # run the main function
