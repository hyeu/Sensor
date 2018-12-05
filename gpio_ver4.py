#-*-coding:utf-8-*-
import RPi.GPIO as GPIO
import weather as we
import finedust_ver2 as dust
import FND
import time
import threading
from multiprocessing import Process

def setGPIO():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

#----------------------LCD--------------------------
#Define GPIO to LCD mapping
LCD_E = 26
LCD_RS = 23
LCD_RW = 24
LCD_D4 = 17
LCD_D5 = 18
LCD_D6 = 27
LCD_D7 = 22

#Define some device constants
LCD_WIDTH = 16  #Maximum characters per line
LCD_CHR = True
LCD_CMD = False
    
LCD_LINE_1 = 0x80 #LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 #LCD RAM address for the 2nd line

#Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005

#창문 LCD 기본값
def setLCD1():
    GPIO.setup(LCD_E, GPIO.OUT)
    GPIO.setup(LCD_RS, GPIO.OUT)
    #GPIO.setup(LCD_RW, GPIO.OUT)
    GPIO.setup(LCD_D4, GPIO.OUT)
    GPIO.setup(LCD_D5, GPIO.OUT)
    GPIO.setup(LCD_D6, GPIO.OUT)
    GPIO.setup(LCD_D7, GPIO.OUT)

    #initialise display
    lcd_init()

    while True:

        value10 = dust.display_value10()
        value25 = dust.display_value25()

        today_temp = we.requestCurrentTemp()
        today_prec = we.requestCurrentPrec()
        tomorrow_temp = we.requestForecastTomtemp()
        tomorrow_prec = we.requestForecastTomprec()
        
        #창문 LCD 첫번째 표시 (미세먼지) / 3초 동안 지속
        lcd_string(value10, LCD_LINE_1)
        lcd_string(value25, LCD_LINE_2)
        time.sleep(5)
        
        #창문 LCD 두번째 표시 (오늘날씨) / 3초 동안 지속
        lcd_string("today",LCD_LINE_1)
        lcd_string(today_temp, LCD_LINE_2)
        time.sleep(3)
        lcd_string("today",LCD_LINE_1)
        lcd_string(today_prec, LCD_LINE_2)
        time.sleep(2.5)

        #창문 LCD 세번째 표시 (내일날씨) / 3초 동안 지속
        lcd_string("tomorrow", LCD_LINE_1)
        lcd_string(tomorrow_temp, LCD_LINE_2)
        time.sleep(3)
        lcd_string("tomorrow", LCD_LINE_1)
        lcd_string(tomorrow_prec, LCD_LINE_2)
        time.sleep(2.5)

#창문 열렸을 때 LCD 기본값
def setLCD2():
    GPIO.setup(LCD_E, GPIO.OUT)
    GPIO.setup(LCD_RS, GPIO.OUT)
    #GPIO.setup(LCD_RW, GPIO.OUT)
    GPIO.setup(LCD_D4, GPIO.OUT)
    GPIO.setup(LCD_D5, GPIO.OUT)
    GPIO.setup(LCD_D6, GPIO.OUT)
    GPIO.setup(LCD_D7, GPIO.OUT)

    #initialise display
    lcd_init()

    #창문 열렸을 때 표시할 문구 입력
    state = dust.grade_state()
    order = dust.grade_order()
    
    lcd_string(state, LCD_LINE_1)
    lcd_string(order, LCD_LINE_2)
    time.sleep(3)
        
def lcd_init():
    lcd_byte(0x33, LCD_CMD)
    lcd_byte(0x32, LCD_CMD)
    lcd_byte(0x06, LCD_CMD)
    lcd_byte(0x0C, LCD_CMD)
    lcd_byte(0x28, LCD_CMD)
    lcd_byte(0x01, LCD_CMD)
    time.sleep(E_DELAY)

def lcd_byte(bits, mode):
    GPIO.output(LCD_RS, mode)

    #High bits
    GPIO.output(LCD_D4, False)
    GPIO.output(LCD_D5, False)
    GPIO.output(LCD_D6, False)
    GPIO.output(LCD_D7, False)
    if bits&0x10==0x10:
        GPIO.output(LCD_D4, True)
    if bits&0x20==0x20:
        GPIO.output(LCD_D5, True)
    if bits&0x40==0x40:
        GPIO.output(LCD_D6, True)
    if bits&0x80==0x80:
        GPIO.output(LCD_D7, True)
    #toggle 'enable' pin
    lcd_toggle_enable()

    #Low bits
    GPIO.output(LCD_D4, False)
    GPIO.output(LCD_D5, False)
    GPIO.output(LCD_D6, False)
    GPIO.output(LCD_D7, False)
    if bits&0x01==0x01:
        GPIO.output(LCD_D4, True)
    if bits&0x02==0x02:
        GPIO.output(LCD_D5, True)
    if bits&0x04==0x04:
        GPIO.output(LCD_D6, True)
    if bits&0x08==0x08:
        GPIO.output(LCD_D7, True)
    #toggle 'enable' pin
    lcd_toggle_enable()

def lcd_toggle_enable():
    time.sleep(E_DELAY)
    GPIO.output(LCD_E, True)
    time.sleep(E_PULSE)
    GPIO.output(LCD_E, False)
    time.sleep(E_DELAY)

def lcd_string(message, line):
    message = message.ljust(LCD_WIDTH," ") #left side
    lcd_byte(line, LCD_CMD)
    for i in range(LCD_WIDTH):
        lcd_byte(ord(message[i]),LCD_CHR)
#------------------------------------------------------------
#-------------setUltrasonic&setPiezo-------------------------
GPIO_TRIGGER = 0
GPIO_ECHO = 1

def setUltrasonic():
    GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
    GPIO.setup(GPIO_ECHO, GPIO.IN, pull_up_down = GPIO.PUD_UP)

    while True:    
        dist = distance()
        print "Measured Distance = %.1f cm" %dist
        time.sleep(0.5)
        
    #창문 열렸을 때 거리 기준값 설정
        if (dist >= 20):
            #미세먼지 등급
            dust_state = '2'

            if (dust_state == '2') or (dust_state == '3') or (dust_state == '4'):           
                #setPiezo()
                #setLCD2()
                tha = threading.Thread(target=setPiezo)
                thb = threading.Thread(target=setLCD2)
                thb.start()
                tha.start()
                tha.join()
                thb.join()

def distance():
    GPIO.output(GPIO_TRIGGER, True)
    time.sleep(0.00001)
    
    GPIO.output(GPIO_TRIGGER, False)
    StartTime = time.time()
    StopTime = time.time()

    while GPIO.input(GPIO_ECHO) == 1:
        StartTime = time.time()
    while GPIO.input(GPIO_ECHO) == 0:
        StopTime = time.time()

    TimeElapsed = StopTime - StartTime

    distance = (TimeElapsed * 34300) / 2

    return distance

def setPiezo():
    GPIO_PIEZO = 13
    GPIO.setup(GPIO_PIEZO, GPIO.OUT)

    p = GPIO.PWM(GPIO_PIEZO, 100)
    p.start(100)
    p.ChangeDutyCycle(90)
    
    #창문 열렸을 때 소리 지속 시간 설정
    for i in range(0, 3, 1):
        for j in range(0, 3, 1):        
            p.ChangeFrequency(392)
            time.sleep(0.3)
    p.stop()
#----------------------------------------------------
if __name__=='__main__':
    try:
        setGPIO()
                    
        proc = Process(target=setUltrasonic)
        proc.start()

        proc_fnd = Process(target=FND.fnd_disp)
        proc_fnd.start()

        proc_disp = Process(target=setLCD1)
        proc_disp.start()

       
    except KeyboardInterrupt:
        pass
    finally:
        lcd_init()
        GPIO.cleanup()
