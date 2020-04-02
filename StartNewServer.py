"""
Created on Fri Feb 21 15:47:30 2020

First, connects to the Pfeiffer TPG_261 pressure control box and
receives pressure values for DC through serial connection.
Creates a server and monitors port 63206 waiting for connected client
When client is connected and asks smth - sends back pressure values.
Finally, logs pressure values in a text file.

Updated: 04 Feb 2020
Created on Sat Apr 21 13:54:20 2018

@author: Victor Rogalev
"""
import socket
import _thread
import time
import datetime as dt
import shutil
from Driver_Pfeiffer_TPG261 import get_pressure
from RepeatedTimer import RepeatedTimer
from List_Of_Servers import *  # server_list is imported from List_Of_Servers.py


class PressureServer():
    """Desciption of a pressure server class"""
    def __init__(self, name_id):
        super(self.__class__, self).__init__()
        self.name_id = name_id
        self.host = socket.gethostname()  # TODO: make explicit hostname in List_Of_Servers.py file!!!
        """find out parameters for the given server name_id"""
        self.port = server_list[self.name_id][0]
        self.com_port_name = server_list[self.name_id][1]
        self.filename_dynamic = self.name_id + '-Log-Dynamic.dat'
        self.connections_counter = 0
        self.pressure = ''
        print('new server initialized')
        self.old_filename = ""
        with open(self.filename_dynamic, "w+") as f:
            f.write('Time, Status Code, Pressure\n')

    def start(self):
        """
        Main functions of server
        """
        """ self.get_pressure_thread every self.timing second receives pressure
            string from controller unit and logs it to a text file. Moved to a 
            separate thread. """
        self.timing = 1
        self.get_pressure_thread = RepeatedTimer(self.timing, self.update_pressure_thread)
        _thread.start_new_thread(self.get_pressure_thread.start, ())

        self.s = socket.socket()  # Create a socket object
        self.s.bind((self.host, self.port))  # Bind to the port
        self.s.listen()  # Enable client connection.
        print('Server started!\n Waiting for clients...')

        """ Here tell controller to send pressure every 100 ms"""
        try:
            self.pressure = get_pressure(self.com_port_name, 'COM,0\r\n')
            print(self.pressure)
        except:
            print('setting controller error')

        """ Here comes infinite loop constantly trying to accept connection """
        while True:
            try:
                print('now will try to accept connection')
                c, addr = self.s.accept()  # Establish connection with client.
                print('Got connection from', addr)
                self.connections_counter += 1
                print('connected ', str(self.connections_counter), ' client(s)')
                _thread.start_new_thread(self.on_new_client, (c,))
            except:
                pass

    def on_new_client(self, client_socket):
        """
        This function is called in a separate thread from start() function!
        Waits for incoming message from client and sends back pressure string.
        """
        while True:
            time.sleep(0.5)  # while loop discriminator - otherwise overload
            msg = client_socket.recv(1024)
            if not msg:
                self.connections_counter -= 1
                break
            client_socket.send(self.pressure.encode())

        print('connected ', str(self.connections_counter), ' client(s)')
        client_socket.shutdown(socket.SHUT_RDWR)
        client_socket.close()

    def update_pressure_thread(self):
        """ Receive pressure string """
        try:
            self.pressure = get_pressure(self.com_port_name)
            print(self.pressure)
            self.log_the_data()
        except:
            print('no pressure received')
            pass

    def log_the_data(self):
        """ Log the data to a file """
        filename = self.name_id + '_pressure_Log_' + dt.datetime.now().strftime("%y-%m-%d") + '.dat'

        """ empty dynamic file if new day """
        if (self.old_filename != filename):
            with open(self.filename_dynamic, "w+") as f:
                f.write('Time, Status Code, Pressure\n')
        self.old_filename = filename

        """ write the value into dynamic file and copy it to log file """
        with open(self.filename_dynamic, "a+") as f:
            try:
                self.gauge_status = int(self.pressure.split(',')[0])
            except:
                self.gauge_status = 5
                pass
            try:
                self.pressure_value = float(self.pressure.split(',')[1])
            except:
                self.pressure_value = 0.0
                pass
            if (self.gauge_status == 0) and (self.pressure_value < 0.01):
                f.write(dt.datetime.now().strftime("%H:%M:%S") +
                        ',' + str(self.gauge_status) +
                        ', ' + str("{:.14f}".format(self.pressure_value)) + '\n')
            elif (self.gauge_status == 1):
                f.write(dt.datetime.now().strftime("%H:%M:%S") +
                        ',' + str(self.gauge_status) +
                        ', ' + str("{:.14f}".format(0.0)) + '\n')
            elif (self.gauge_status == 2):
                f.write(dt.datetime.now().strftime("%H:%M:%S") +
                        ',' + str(self.gauge_status) +
                        ', ' + str("{:.14f}".format(0.01)) + '\n')

        shutil.copy2(self.filename_dynamic, filename)


def new_server(*args):
    """
    This function is called from the MainServer script to start a new
    server.
    """
    print('no connection - starting a new server')
    server_1 = PressureServer(*args)
    server_1.start()
