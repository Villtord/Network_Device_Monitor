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
#        self.get_pressure("COM,0")   # request pressure values each 100 ms
        self.data_to_return = ""

    def get_pressure(self, *args: "optional command"):
        self.data_to_return = ""
        """ Opens serial connection and request/read the pressure values    """
        ser = serial.Serial(self.com_name,
                            baudrate=9600,
                            bytesize=serial.EIGHTBITS,
                            stopbits=serial.STOPBITS_ONE,
                            parity=serial.PARITY_NONE,
                            timeout=0.5)
        ser_io = io.TextIOWrapper(io.BufferedRWPair(ser, ser, 1),
                                  newline='\r\n',
                                  line_buffering=True)
        """Write a command(s) to the controller and read the reply """
        if args:
            try:
                command_full = str(args[0]) + "\r\n"
                ser_io.write(command_full)
                self.read_str_raw = ser_io.readline()
            except Exception as e:
                logging.exception(e)
                print (e)
                pass
        else:
            self.read_str_raw = ser_io.readline()
        ser.close()
        """Handle the received data and decide what to transmit"""
        try:
            self.gauge_status = int(self.read_str_raw.split(',')[0])
        except:
            self.gauge_status = 5
            pass
        try:
            self.pressure_value = float(self.read_str_raw.split(',')[1])
        except:
            self.pressure_value = "NAN"
            pass
        if (self.gauge_status == 0) and (self.pressure_value < 0.01):
            self.data_to_return = self.pressure_value
        elif self.gauge_status == 1:
            self.data_to_return = "under"
        elif self.gauge_status == 2:
            self.data_to_return = "over"
        try:
            # self.read_str = str("{:.10f}".format(float(0.000001)))
            return str(self.data_to_return)
        except Exception as e:
            logging.exception(e)
            pass
