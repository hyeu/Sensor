# -*- coding:utf-8 -*-
#FND.py
import smbus
import time
import threading

bus = smbus.SMBus(1)

#FND configuration
addr_fnd = 0x20
config_port = 0x06
out_port = 0x02

data_fnd = (0xFC, 0x60, 0xDA, 0xF2, 0x66, 0xB6, 0x3E, 0xE0, 0xFE, 0xF6, 0x01,0x02,0x1A)
digit = (0x7F, 0xBF, 0xDF, 0xEF, 0xF7, 0xFB)

out_disp = 0

      
#Temp/Humi configuration
addr_temp = 0x40
cmd_temp = 0xf3
soft_reset = 0xfe

ns_new = ""
stop = 0


def temp_read():
    temp = 0.0
    val = 0
    data = [0, 0]
    bus.write_byte(addr_temp, soft_reset)
    time.sleep(0.05)

    #temperature
    bus.write_byte(addr_temp, cmd_temp)
    time.sleep(0.260)
    for i in range(0,2,1):
        data[i] = bus.read_byte(addr_temp)
    val = data[0] << 8 | data[1]
    temp = -46.85 + 175.72 / 65536 * val

    print ('temp : %.2f' %(temp))

    tp = str(temp)
    
    if (tp[1] != '.'):
        return tp[0:2]+tp[3:5]
    else:
        return '0'+tp[0]+tp[2:4]

def fnd_disp():
    ns_new = temp_read()
    while (ns_new == ""):
        time.sleep(0)
        bus.write_word_data(addr_fnd, config_port, 0x0000)

    while (ns_new != ""):
        #ns_new = temp_read()
        while True:
            #ns_new = temp_read()
            for i in range(0,len(ns_new),1):
                if (ns_new[i] == '-'):
                    out_disp = data_fnd[11] << 8 | digit[0]
                    bus.write_word_data(addr_fnd, out_port, out_disp)
                # notation of dot(.)
                out_disp = data_fnd[10] << 8 | digit[1]
                bus.write_word_data(addr_fnd, out_port, out_disp)
            
                n = int(ns_new[i])
                
                out_disp = data_fnd[n] << 8 | digit[i]
                bus.write_word_data(addr_fnd, out_port, out_disp)
                time.sleep(0.01)
                #ns_new = temp_read()
            if (stop == 1):
                break

def doFND():
    try:
        #th = threading.Thread(target=fnd_disp)
        #th.start()
        while True:
            ns_new = temp_read()
            if ns_new != "":
                fnd_disp()
    except KeyboardInterrupt:
        stop = 1
        pass
    finally:
        pass

#if __name__ == '__main__':
#    doFND()
