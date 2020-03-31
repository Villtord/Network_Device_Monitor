"""
This script should start when the computer starts. First, it checks if the measurement
server is running or not. If it is not running, it starts the corresponding
server (tries only one time!).
The list of measurement servers with parameters is read from the file List_Of_Servers.py
"""
from __future__ import unicode_literals
import sys, gc, socket
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow
from PyQt5.QtCore import Qt
import _thread, time
from List_Of_Servers import *  # server_list is imported from List_Of_Servers.py
import StartNewServer


class ExampleApp(QMainWindow):
    """
    Creates a small window and immediately starts to check all servers
    from the list of servers and corresponding ports
    """

    def __init__(self, *args, **kwargs):
        super(__class__, self).__init__(*args, **kwargs)
        self.label = QLabel("WE ARE OFFLINE")
        self.label.setAlignment(Qt.AlignCenter)
        self.setCentralWidget(self.label)

    def start(self, **kwargs):
        self.port_server_list = kwargs
        print(self.port_server_list)
        host = socket.gethostname()
        for item in self.port_server_list.items():
            try:
                name_id, port = item[0], item[1][0]
                check_connection(host, port, name_id)
                time.sleep(1)
            except:
                raise
                print('some error in check connection')
        self.label.setText("ONLINE")
        self.label.setStyleSheet("QLabel { background-color : white; color : green; }")
        gc.collect()


def check_connection(host, port, server_name):
    """
    Checks if server is already running:
    first it tries to connect to server port
    if it is not successful it starts the server in a separate thread
    """
    print('host is ', host)
    my_socket = socket.socket()
    try:
        my_socket.connect((host, port))
        print('connection established')
    except:
        print('starting a server', server_name)
        _thread.start_new_thread(StartNewServer.new_server, (server_name,))
        time.sleep(0.5)
        try:
            my_socket.connect((host, port))
            print('finally connected')
        except:
            print('failed to connect')
        pass


def main():
    app = QApplication.instance()  # checks if QApplication already exists
    if not app:  # create QApplication if it doesnt exist
        app = QApplication(sys.argv)
    form = ExampleApp()  # We set the form to be our ExampleApp (design)
    form.setWindowTitle("Servers control")
    form.resize(250, 120)
    form.show()  # Show the form
    form.start(**server_list)  # server_list is imported from List_Of_Servers.py
    sys.exit(app.exec_())


if __name__ == '__main__':  # if we're running file directly and not importing it
    main()  # run the main function
