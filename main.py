import gpio
import webserver as web
import FND
from multiprocessing import Process


if __name__=='__main__':
    try:
        gpio.setGPIO()
                    
        proc_fnd = Process(target=FND.doFND)
        proc_fnd.start()

        proc_disp = Process(target=gpio.setLCD1)
        proc_disp.start()

        proc = Process(target=gpio.setUltrasonic)
        proc.start()

        web.app.run(debug=True, host='203.153.147.116',port=5000)
        
   

    finally:
        gpio.lcd_init()
        gpio.GPIO.cleanup()
