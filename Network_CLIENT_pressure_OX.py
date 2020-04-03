# -*- coding: utf-8 -*-
"""
GUI application which shows updated pressure from the
Oxidation Chamber pressure controller.

Last update: 03 Arp 2020
Created on Sat Apr 21 14:12:26 2018

@author: Victor Rogalev
"""
import sys

from PyQt5.QtWidgets import QApplication

from Network_Client_Class import NetworkClientMonitor
from List_Of_Servers import *  # server_list is imported from List_Of_Servers.py

server_number = 0
server_name = list(server_list.keys())[server_number]
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
