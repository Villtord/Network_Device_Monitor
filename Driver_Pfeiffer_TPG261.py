"""
Driver for Pfeiffer TPG261 pressure control device.
The latter must be connected through a certain COM port (virtual or real).
Driver opens serial connection and reads the pressure values.
"""
import serial.tools.list_ports
import logging
import io


def get_pressure(com_name, *args: 'command to pass'):
    """ Opens serial connection and request/read the pressure values    """
    read_str = '0.000001'
    # ser = serial.Serial(com_name,
    #                     baudrate=9600,
    #                     bytesize=serial.EIGHTBITS,
    #                     stopbits=serial.STOPBITS_ONE,
    #                     parity=serial.PARITY_NONE,
    #                     timeout=0.5)
    # ser_io = io.TextIOWrapper(io.BufferedRWPair(ser, ser, 1),
    #                           newline='\r\n',
    #                           line_buffering=True)
    #        ser_io.write("COM,0\r\n")   # request pressure values each 100 ms
    """Write a command(s) to the controller and read the reply """
    # if args:
    #     try:
    #         command_full = str(args[0]) + "\r\n"
    #         ser_io.write(command_full)
    #         read_str = ser_io.readline()
    #     except Exception as e:
    #         logging.exception(e)
    #         pass
    # else:
    #     read_str = ser_io.readline()
    # ser.close()

    try:
        return read_str
    except Exception as e:
        logging.exception(e)
