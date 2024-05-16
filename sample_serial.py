import serial
import serial.tools.list_ports
from pprint import pprint as pp
serial_list = []
def Get_ALLCom():
    port_list = serial.tools.list_ports.comports()
    print(port_list[0])
    if len(port_list) <= 0:
        print("No COM")
        return ""
    else:
        print("ALL COM")
        for com in port_list:
            #print("com:",list(com)[0])
            serial_list.append(serial.Serial(list(com)[0], 115200,timeout=3))
        
        pp(serial_list)
        serial_list[0].write("begin".encode('UTF-8'))
        serial_list[0].reset_input_buffer()
        
Get_FristCom()