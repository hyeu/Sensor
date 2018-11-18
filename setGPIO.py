def setGPIO():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    
def setLed():
    led_pin1 = 14
    led_pin2 = 15
    GPIO.setup(led_pin1,GPIO.OUT)
    GPIO.setup(led_pin2,GPIO.OUT)

    led1 = GPIO.PWM(led_pin1,50)
    led2 = GPIO.PWM(led_pin2,50)
    led1.start(90)
    led2.start(90)


def setMotor():
    GPIO_RP = 4
    GPIO_RN = 25
    GPIO_EN = 12

    GPIO_TRIGGER = 0
    GPIO_ECHO = 1

    GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
    GPIO.setup(GPIO_ECHO, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    GPIO.setup(GPIO_RN, GPIO.OUT)
    GPIO.setup(GPIO_RP, GPIO.OUT)
    GPIO.setup(GPIO_EN, GPIO.OUT)

    dcp = GPIO.PWM(GPIO_RP,100)
    dcn = GPIO.PWM(GPIO_RN,100)
    dcp.start(0)
    dcn.start(0)


def setPiezo():
    piezo = 13
    GPIO.setup(piezo,GPIO.OUT)
    GPIO.output(piezo,True)

    _piezo = GPIO.PWM(piezo,100)
