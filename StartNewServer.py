"""
General server class.
Should not depend on the monitored device.

        Main functions of server:
        1. start server waiting for clients to connect, if connected - send values
        2. start reading from device using driver file
        3. log the data to the text file

Last updated: 02 Apr 2020
Created on Sat Apr 21 13:54:20 2018

@author: Victor Rogalev
"""
import _thread
import datetime as dt
import importlib
import shutil
import time
import os

from List_Of_Servers import *  # server_list is imported from List_Of_Servers.py
from RepeatedTimer import RepeatedTimer


class PressureServer():
    """Desciption of a pressure server class"""

    def __init__(self, name_id):
        super(self.__class__, self).__init__()
        print('new server being initialized')
        self.connections_counter = 0
        self.pressure = ''
        self.name_id = name_id
        """find out parameters for the given server name_id"""
        self.host = server_list[self.name_id][0]
        self.port = server_list[self.name_id][1]
        self.com_port_name = server_list[self.name_id][2]
        self.driver_module = importlib.import_module(server_list[self.name_id][3])  # import driver module
        self.driver = self.driver_module.Driver(self.com_port_name)  # initialize driver
        """configure initial logging"""
        self.filename_dynamic = self.name_id + '-log-dynamic.dat'
        self.old_filename = ""
        self.path = os.getcwd()
        self.log_path = self.path + "/logs"
        with open(self.filename_dynamic, "w+") as f:
            f.write('\n')

    def start(self):
        """
        Main functions of server:
        1. start server waiting for clients to connect, if connected - send values
        2. start reading from device using driver file
        3. log the data
        """
        """ self.get_pressure_thread every self.timing second receives pressure
            string from controller unit and logs it to a text file. Moved to a 
            separate thread. """
        self.timing = 1
        self.get_pressure_loop = RepeatedTimer(self.timing, self.update_pressure_thread)
        _thread.start_new_thread(self.get_pressure_loop.start, ())

        self.s = socket.socket()  # Create a socket object
        self.s.bind((self.host, self.port))  # Bind to the port
        self.s.listen()  # Enable client connection.
        print('Server started!\n Waiting for clients...')

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
            if msg.decode() == 'so you think you can tell':
                #                print ("received from host: ", msg.decode())
                client_socket.send(self.pressure.encode())
            elif ("SETP" in msg.decode()) or ("RANGE" in msg.decode()):
                self.get_pressure_loop.stop()
                print("sending command ", msg.decode())
                flag = True
                while flag:
                    time.sleep(0.4)
                    try:
                        value = self.driver.get_pressure(msg.decode())
                        flag = False if value else True
                    except:
                        print("error setting command")
                        pass
                client_socket.send(value.encode())
                self.get_pressure_loop.start()
            else:
                pass

        print('connected ', str(self.connections_counter), ' client(s)')
        client_socket.shutdown(socket.SHUT_RDWR)
        client_socket.close()

    def update_pressure_thread(self):
        """ start reading from device using driver file """
        try:
            self.pressure = self.driver.get_pressure()  # self.pressure is a STRING!
            print(self.pressure)
            self.log_the_data()
        except:
            print('no pressure received')
            pass

    def log_the_data(self):  # TODO: save log files to a separate folder
        """ Log the data to a file """
        filename = self.name_id + '_log_' + dt.datetime.now().strftime("%y-%m-%d") + '.dat'

        """ empty dynamic file if new day """
        if self.old_filename != filename:
            with open(self.filename_dynamic, "w+") as f:
                f.write('\n')
        self.old_filename = filename

        """ add comma in the end if missing """
        if self.pressure[-1]!=",":
            self.pressure += ","
        """ write the value into dynamic file and copy it to log file """
        with open(self.filename_dynamic, "a+") as f:
            log_data = dt.datetime.now().strftime("%H:%M:%S") + ',' + self.pressure + '\n'
            f.write(log_data)
        shutil.copy2(self.filename_dynamic, filename)


def new_server(*args):
    """ This function is called from the MainServer script to start a new server """
    print('starting a new server')
    server_1 = PressureServer(*args)
    server_1.start()
