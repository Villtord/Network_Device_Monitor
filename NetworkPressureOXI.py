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
import socket
from PyQt5.QtWidgets import QApplication
from Network_Client_Class import NetworkClientMonitor

host = socket.gethostname()
port = 63207
index = 0
color = "blue"

def main():
    app = QApplication(sys.argv)  # A new instance of QApplication
    form = NetworkClientMonitor(host, port, index, color)  # We set the form to be our ExampleApp (design)
    form.setWindowTitle("Oxidation Chamber - client") # Change window name
    form.resize (380,150)        # Resize the form
    form.show()                  # Show the form
    sys.exit(app.exec_())        # Handle exit case

if __name__ == '__main__':       # if we're running file directly and not importing it
    main()                       # run the main function