"""
Driver for Pfeiffer TPG261 pressure control device.
The latter must be connected through a certain COM port (virtual or real).
Driver first initializes, then opens serial connection and reads the pressure values.
Driver handles the correct pressure to transmit
"""
import serial.tools.list_ports
import logging
import io


class Driver:
    def __init__(self, com_name):
        self.com_name = com_name
        self.get_pressure("COM,0")   # request pressure values each 100 ms

    def get_pressure(self, *args: "optional command"):
        """ Opens serial connection and request/read the pressure values    """
        # ser = serial.Serial(self.com_name,
        #                     baudrate=9600,
        #                     bytesize=serial.EIGHTBITS,
        #                     stopbits=serial.STOPBITS_ONE,
        #                     parity=serial.PARITY_NONE,
        #                     timeout=0.5)
        # ser_io = io.TextIOWrapper(io.BufferedRWPair(ser, ser, 1),
        #                           newline='\r\n',
        #                           line_buffering=True)
        """Write a command(s) to the controller and read the reply """
        # if args:
        #     try:
        #         command_full = str(args[0]) + "\r\n"
        #         ser_io.write(command_full)
        #         self.read_str_raw = ser_io.readline()
        #     except Exception as e:
        #         logging.exception(e)
        #         pass
        # else:
        #     self.read_str_raw = ser_io.readline()
        # ser.close()
        """Handle the received data and decide what to transmit"""
        # try:
        #     self.gauge_status = int(self.read_str_raw.split(',')[0])
        # except:
        #     self.gauge_status = 5
        #     pass
        # try:
        #     self.pressure_value = float(self.read_str_raw.split(',')[1])
        # except:
        #     self.pressure_value = 0.0
        #     pass
        # if (self.gauge_status == 0) and (self.pressure_value < 0.01):
        #     self.read_str = self.pressure_value
        # elif (self.gauge_status == 1):
        #     self.read_str = 0.0  # underrange
        # elif (self.gauge_status == 2):
        #     self.read_str = 0.01  # overrange
        try:
            self.read_str = str("{:.10f}".format(float(0.000001)))
            return self.read_str
        except Exception as e:
            logging.exception(e)
