import requests
import base64
import json
import picamera
import RPi.GPIO as GPIO
import time

def main():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(7,GPIO.IN)
    GPIO.setup(13,GPIO.OUT)
    
    while True:
        i = GPIO.input(7)
        
        if i==0:
            print("No car detected")
            GPIO.output(13, 0)
            time.sleep(0.1)
        elif i==1:
            print("Car Detected")
            Pic()
            plate = Get()
            if (plate == "A454I6"):
                GPIO.output(13, 1)
                print("Garage open")
            else:
                print("Unauthorized Car")
    

def Get():
    IMAGE_PATH = '/home/pi/Desktop/newimage.jpg'
    SECRET_KEY = 'sk_d720175ba44d962caa8b33db'

    with open(IMAGE_PATH, 'rb') as image_file:
        img_base64 = base64.b64encode(image_file.read())

    url = 'https://api.openalpr.com/v2/recognize_bytes?recognize_vehicle=1&country=me&secret_key=%s'%(SECRET_KEY)
    r = requests.post(url, data = img_base64)

    x = r.json()

    k = x["results"]
    plate = (k[0]['plate'])
    return plate

def Pic():
    print ("taking picture")
    with picamera.PiCamera() as camera:
        camera.resolution = (1280,720)
        camera.capture("/home/pi/Desktop/newimage.jpg")
    print ("Picture taken")
        
if __name__ == "__main__":
    main()