# -*- coding: utf-8 -*-
"""
Typical GUI for showing pressure and temperature (port 63205) values.
Pressure/temperature values are obtained from the network server (host,port)
as a string of N values (N>=1) separated with comma.
Pressure index specifies which value from the string to take. Color option used
to distinguish between different pressure/temperature gauges.

Updated: 05 Feb 2020
Created on Sat Apr 21 14:05:33 2018

@author: Victor Rogalev
"""
from __future__ import unicode_literals
from PyQt5.QtWidgets import QWidget
from NetworkGetPressure import NetworkGetPressure
from PyQt5 import QtCore, QtWidgets
import gc


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(380, 150)
        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(0, 0, MainWindow.width(), MainWindow.height()))
        self.label.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.label.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label.setLineWidth(1)
        self.label.setText("")
        self.label.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")


class NetworkClientMonitor(QWidget, Ui_MainWindow):
    def __init__(self, host, port, pressure_index_to_take, color, **kwargs):
        super(self.__class__, self).__init__()
        self.host = host
        self.port = port
        self.pressure_index_to_take = pressure_index_to_take
        self.color = color
        self.setupUi(self)
        """ Special backgound color and start value for temperature GUI """
        if self.port == 63205:
            self.label.setStyleSheet("QLabel { background-color : green; color : "
                                     + self.color + "; }")
            self.start_pressure = 273
        else:
            self.label.setStyleSheet("QLabel { background-color : black; color : "
                                     + self.color + "; }")
            self.start_pressure = 0.0000000001
        self.label.setText("{:.01e}".format(self.start_pressure))
        self.main_start()

    def resizeEvent(self, evt):
        """ Possibility to resize GUI window """
        font = self.font()
        font.setPixelSize(self.height() * 0.7)
        self.label.setFont(font)
        self.label.setGeometry(0, 0, self.width(), self.height())
        gc.collect()

    def main_start(self):
        """ Make a separate thread to accept pressure values from server """
        self.networking = NetworkGetPressure(self.host, self.port)  # thread
        self.networking.new_value_trigger.connect(self.update_screen)
        self.networking.start()  # start this separate thread to get pressure
        gc.collect()

    def update_screen(self, pressure):
        """ Update window when a new pressure value in networking thread"""
        try:
            self.pressure = float(pressure.split(',')[self.pressure_index_to_take])  # take index value
            """ If we are getting temperature from the Lakeshore"""
            if self.port == 63205:
                if (self.pressure < 500):
                    self.label.setText(str(self.pressure))
            else:
                """ If we are getting pressure values"""
                if (self.pressure > 0) and (self.pressure < 1):
                    self.label.setText("{:.01e}".format(self.pressure))
        except:
            pass
        gc.collect()

    def __del__(self):
        try:
            self.networking.close()
        except:
            pass
        self.networking.timer_x.stop()
        self.networking.timer_x.deleteLater()

    def closeEvent(self, event):
        try:
            self.networking.close()
        except:
            pass
        self.networking.timer_x.stop()
        self.networking.timer_x.deleteLater()
