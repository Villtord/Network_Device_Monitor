# -*- coding: utf-8 -*-
"""
Thread to get pressure values from network server located at given host, port.

Last update: 06 April 2020
Created on Wed Feb  5 15:34:14 2020

@author: Victor Rogalev
"""
import PyQt5.QtCore
import socket
import select


class NetworkGetPressure(PyQt5.QtCore.QThread):
    """
    Thread to connect to a server and start getting values
    """
    new_value_trigger = PyQt5.QtCore.pyqtSignal('QString')

    def __init__(self, host, port, **kwargs):
        super(self.__class__, self).__init__()
        self.connection_flag = False
        self.host = host
        self.port = port

        """Every self.timing [ms] checking connection with server/new values"""
        self.timing = 1000
        self.timer_x = PyQt5.QtCore.QTimer(self)
        self.timer_x.timeout.connect(self.check_connection)
        self.timer_x.start(self.timing)

    def check_connection(self):
        """ Checks connection prior to updating pressure """
        if not self.connection_flag:
            print('establishing connection with host ', self.host)
            self.mySocket = socket.socket()
            try:
                self.mySocket.connect((self.host, self.port))
                self.connection_flag = True
                print('connection established')
                self.update_pressure()
            except:
                self.connection_flag = False
                self.mySocket.close()
                print('no connection')
        else:
            self.update_pressure()

    def update_pressure(self):
        """ Ask server and receive new pressure values """
        try:
            print(self.mySocket.getsockname())
            message = 'so you think you can tell'
            print('attempt to send: ', message)
            self.mySocket.setblocking(0)
            try:
                self.mySocket.send(message.encode())
                print('message send')
                timeout = 2
                ready = select.select([self.mySocket], [], [], timeout)
                if ready[0]:
                    self.pressure = self.mySocket.recv(1024).decode()
                    print('Received from server: ' + self.pressure)
            except:
                print('error here')
                self.connection_flag = False
                pass
            self.new_value_trigger.emit(self.pressure)
        except:
            pass

    def close(self):
        try:
            self.mySocket.close()
        except:
            pass
        self.timer_x.stop()
        self.timer_x.deleteLater()