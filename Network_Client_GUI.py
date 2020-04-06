# -*- coding: utf-8 -*-
"""
Universal GUI application which shows data values from the corresponding server.
To start print in the command line:

path_to_and_python.exe path_to_and_Network_Client_GUI.py server_number

Here server number is an integer corresponding to the server number in List_Of_Servers.py file

Last update: 06 Arp 2020
Created on Sat Apr 21 14:12:26 2018

@author: Victor Rogalev
"""

import sys

import PyQt5.QtWidgets

import Network_Client_Class as NCC
import List_Of_Servers as LoS


def main(server_number):
    server_name = list(LoS.server_list.keys())[server_number]
    host = LoS.server_list[server_name][0]
    port = LoS.server_list[server_name][1]
    index = int(LoS.server_list[server_name][4])
    color = LoS.server_list[server_name][5]
    app = PyQt5.QtWidgets.QApplication(sys.argv)  # A new instance of QApplication
    form = NCC.NetworkClientMonitor(host, port, index, color)  # We set the form to be our ExampleApp (design)
    form.setWindowTitle(server_name+' - client')  # Change window name
    form.resize(380, 150)  # Resize the form
    form.show()  # Show the form
    sys.exit(app.exec_())  # Handle exit case


if __name__ == '__main__':  # if we're running file directly and not importing it
    a = int(sys.argv[1])  # this is a server number which must be provided on start from the command line
    main(a)  # run the main function
