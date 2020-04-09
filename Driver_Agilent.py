"""
Driver for Agilent pressure control device.
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
        self.pressure_value = 0.0

    def get_pressure(self, *args: "optional command"):
        """ Opens serial connection and request/read the pressure values    """
        ser = serial.Serial(self.com_name,
                            baudrate=9600,
                            bytesize=serial.EIGHTBITS,
                            parity=serial.PARITY_NONE,
                            stopbits=serial.STOPBITS_ONE,
                            timeout=0.1)
        ser_io = io.TextIOWrapper(io.BufferedRWPair(ser, ser, 1),
                                  newline='\r',
                                  line_buffering=True)
        """Write a command(s) to the controller and read the reply """
        if args:
            try:
                command_full = str(args[0]) + "\r"
                ser_io.write(command_full)
                self.read_str_raw = ser_io.readline()
            except Exception as e:
                logging.exception(e)
                pass
        else:
            ser_io.write("#000F\r")  # request pressure value
            self.read_str_raw = ser_io.readline()  # get only necessary numbers
        ser.close()
        """Handle the received data and decide what to transmit"""
        try:
            self.pressure_value = self.read_str_raw[1:]
        except:
            self.pressure_value = "NAN"
            pass

        self.read_str = self.pressure_value
        try:
            return str(self.read_str)
        except Exception as e:
            logging.exception(e)
