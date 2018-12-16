#-*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import finedust as dust
import weather as we
import time
from flask import Flask, render_template

app = Flask(__name__)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO_RP = 4  #Input Pin
GPIO_RN = 25 #Input Pin
GPIO_EN = 12 #Enable Pin

GPIO.setup(GPIO_RP, GPIO.OUT)
GPIO.setup(GPIO_RN, GPIO.OUT)
GPIO.setup(GPIO_EN, GPIO.OUT)

rp = GPIO.PWM(GPIO_RP,100)
rn = GPIO.PWM(GPIO_RN,100)
rp.start(90)
rn.start(90)

@app.route('/')
def index():
        value = dust.display_value10()
        state = dust.grade_state()
        precipitation = we.requestCurrentPrec()
        return render_template('layout.html',pm10value=value,pm10grade=state, prec=precipitation)

@app.route('/forward')
def window_open():
        rp.ChangeDutyCycle(1)
        GPIO.output(GPIO_RP, True)
        GPIO.output(GPIO_RN, False)
        GPIO.output(GPIO_EN, True)
        time.sleep(1)
        GPIO.output(GPIO_EN, False)
        return (''), 204

@app.route('/backward')        
def window_close():
        rn.ChangeDutyCycle(1)
	GPIO.output(GPIO_RP, False)
        GPIO.output(GPIO_RN, True)
        GPIO.output(GPIO_EN, True)
        time.sleep(1)
        GPIO.output(GPIO_EN, False)
        return (''), 204        
 


#if __name__ == "__main__":
#	app.run(debug=True, host='0.0.0.0',port=8080)
