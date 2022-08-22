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
from PyQt5 import QtCore, QtWidgets
import logging
import gc
from typing import List, Tuple, Union, TypeVar

from NDMonitor.NetworkGetPressure import NetworkGetPressure


class UiMainWindow(object):
    def __init__(self):
        self.label = QtWidgets.QLabel(self)

    def setupUi(self, MainWindow) -> None:
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(380, 150)
        self.label.setGeometry(QtCore.QRect(0, 0, MainWindow.width(), MainWindow.height()))
        self.label.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.label.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label.setLineWidth(1)
        self.label.setText("")
        self.label.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")


class NetworkClientMonitor(QWidget, UiMainWindow):
    def __init__(self, host: str, port: int, pressure_index_to_take: int, color: str, **kwargs):
        """

        :param host: IP of the server to connect to
        :param port: Port to connect to
        :param pressure_index_to_take: If there are more than one values coming from gauge - this is a filter.
        :param color: color as a string
        :param kwargs:
        """
        super(self.__class__, self).__init__()
        self.host = host
        self.port = port
        self.pressure_index_to_take = pressure_index_to_take
        self.color = color
        self.pressure_to_show = ''
        self.setupUi(self)
        """ Special background color and start value for temperature GUI """
        if self.port == 63205:
            self.label.setStyleSheet("QLabel { background-color : green; color : "
                                     + self.color + "; }")
            self.start_pressure = 273
        else:
            self.label.setStyleSheet("QLabel { background-color : black; color : "
                                     + self.color + "; }")
            self.start_pressure = 0.0000000001
        self.label.setText("{:.01e}".format(self.start_pressure))
        """ Make a separate thread to accept pressure values from server """
        self.networking = NetworkGetPressure(self.host, self.port)  # thread
        self.networking.new_value_trigger.connect(self.update_screen)
        self.networking.start()  # start this separate thread to get pressure
        gc.collect()

    def update_screen(self, pressure: str):
        """ Update window when a new pressure value in networking thread
        :param pressure:trigger string
        """
        try:
            self.pressure_to_show = float(pressure.split(',')[self.pressure_index_to_take])  # take index value
            """ If we are getting temperature from the Lakeshore"""
            if self.port == 63205:
                if self.pressure_to_show < 500:
                    self.label.setText(str(self.pressure_to_show))
            else:
                """ If we are getting pressure values"""
                if (self.pressure_to_show > 0) and (self.pressure_to_show < 1):
                    self.label.setText("{:.01e}".format(self.pressure_to_show))
        except Exception as e:
            logging.exception(e)
            self.label.setText(pressure.split(',')[self.pressure_index_to_take])
            pass
        gc.collect()

    def resizeEvent(self, evt):
        """ Possibility to resize GUI window """
        font = self.font()
        font.setPixelSize(int(self.height() * 0.7))
        self.label.setFont(font)
        self.label.setGeometry(0, 0, self.width(), self.height())
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
