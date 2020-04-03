"""
GUI application which shows updated pressure from the
AML pressure controller (Analysis Chamber).

Last updated: 03 Apr 2020
Created on Thu Apr 19 14:57:38 2018

@author: Victor Rogalev
"""

import sys

from PyQt5.QtWidgets import QApplication

from Network_Client_Class import NetworkClientMonitor
from List_Of_Servers import *  # server_list is imported from List_Of_Servers.py

server_number = 1
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
