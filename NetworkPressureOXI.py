# -*- coding: utf-8 -*-
"""
GUI application which shows updated pressure from the
Dist Chamber pressure controller.

Updated: 24 Feb 2020 Separate server for OxiChamber added
Updated: 05 Feb 2020
Created on Sat Apr 21 14:12:26 2018

@author: Victor Rogalev
"""
import sys

from PyQt5.QtWidgets import QApplication

from List_Of_Servers import *  # server_list is imported from List_Of_Servers.py
from Network_Client_Class import NetworkClientMonitor

server_name = "OXICHAMBER"
host = server_list[server_name][0]
port = server_list[server_name][1]
index = int(server_list[server_name][4])
color = server_list[server_name][5]


def main():
    app = QApplication(sys.argv)  # A new instance of QApplication
    form = NetworkClientMonitor(host, port, index, color)  # We set the form to be our ExampleApp (design)
    form.setWindowTitle(server_name+' - client')  # Change window name
    form.resize(380, 150)  # Resize the form
    form.show()  # Show the form
    sys.exit(app.exec_())  # Handle exit case


if __name__ == '__main__':  # if we're running file directly and not importing it
    main()  # run the main function
