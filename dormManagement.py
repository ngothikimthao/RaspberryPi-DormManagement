import RPi.GPIO as GPIO
import time
import datetime
import sys
import smtplib


POWER = 17
LIGHT208 = 27
LIGHT308 = 22

LASER208 = 11
LASER308 = 10

PHOTORESISTOR208 = 4
PHOTORESISTOR308 = 18


DELAY = 0.5


LIMIT_MAX = 26
LIMIT_MIN = 22

MILESTONES_HOUR = 4


list = []

class inforRoom :
	def __init__(self, name, time):
	    	self.name = name
    	    	self.time = time

def main():
    setup()
    wellcome()
    choose = menu()
    case(choose)
   
def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(POWER, GPIO.OUT)
    GPIO.setup(LASER208, GPIO.OUT)
    GPIO.setup(LASER308, GPIO.OUT)
    GPIO.setup(LIGHT208, GPIO.OUT)
    GPIO.setup(LIGHT308, GPIO.OUT)
    GPIO.setup(PHOTORESISTOR208, GPIO.IN)
    GPIO.setup(PHOTORESISTOR308, GPIO.IN)

def wellcome():
    print("            *****************************************\n")
    print "            *           Welcome to PNV              *\n"
    print("            *****************************************\n")

def display():
    print("Room \t\t\t\t\t\t Time")

    for listRoom in list:
	print(listRoom.name),
	print("\t\t\t\t\t\t"),
	print(listRoom.time )

def app(hourVirtual):
    GPIO.output(POWER, GPIO.HIGH)
    GPIO.output(LIGHT208, GPIO.HIGH)
    GPIO.output(LIGHT308, GPIO.HIGH)
    GPIO.output(LASER208, GPIO.HIGH)
    GPIO.output(LASER308, GPIO.HIGH)
   
    timeNow = datetime.datetime.now()
    hour = '{:02d}'.format(timeNow.hour)

    while True:
	print GPIO.input(PHOTORESISTOR208)
	print GPIO.input(PHOTORESISTOR308)
	photoresistor208 = GPIO.input(PHOTORESISTOR208)
	photoresistor308 = GPIO.input(PHOTORESISTOR308)
	
	validTime = checkTime(hourVirtual)

	if validTime == True:
		turnOffLight()
	 	checkPeople(photoresistor208,photoresistor308)
	 	display()
		print("This time is not vailable for students!")
	else:
            	print("This time is vailable for students!")

        systemTray(validTime)

def menu():
	print ("The system have 2 options:")
	print ("1. Time valid form 10 pm to 4 am")
	print ("2. Time invalid form 5 am to 9 pm")
	print ("3. Information room have mistake")
	print ("4. Back to menu")
	print ("5. Exit")
	print('Please enter option you want:')

	while True:
	    choose = input()
	    if(choose <= 5 and choose > 0 ):
        	break

	return choose

def case(choose):
	if choose == 1:
		app(22)
	elif choose == 2:
		app(10)
	elif choose == 3:
		display()
	elif choose == 4:
		menu()
	elif choose == 5:
		exit()
	elif choose !="":
		print("/n Not valid choice try again")

def systemTray(validTime): 
	timeNow = datetime.datetime.now()

	year = '{:02d}'.format(timeNow.year)
	month = '{:02d}'.format(timeNow.month)
	day = '{:02d}'.format(timeNow.day)
	hour = '{:02d}'.format(timeNow.hour)
	minute = '{:02d}'.format(timeNow.minute)
	second = '{:02d}'.format(timeNow.second)

	currentTime = '{}-{}-{} {}:{}:{}'.format(day, month, year, hour, minute, second)
	print("The app is running at: " + currentTime)
	print("------------------------------------------")
	time.sleep(DELAY)

def checkValidTime(time):
        if time <= MILESTONES_HOUR:
            return time + LIMIT_MIN
        else: 
            return time

def checkTime(hour):
    if checkValidTime(hour) >= LIMIT_MIN and checkValidTime(hour) <= LIMIT_MAX:
	return True
    else:
	return False


def turnOffLight():
    statusLight208 = GPIO.input(LIGHT208)
    statusLight308 = GPIO.input(LIGHT308)

    if statusLight208 == 1:
	GPIO.output(LIGHT208, GPIO.LOW)

    if statusLight308 == 1:
	GPIO.output(LIGHT308, GPIO.LOW)
 
def checkPeople(PHOTORESISTOR208,PHOTORESISTOR308):
    timeNow = datetime.datetime.now()
    year = '{:02d}'.format(timeNow.year)
    month = '{:02d}'.format(timeNow.month)
    day = '{:02d}'.format(timeNow.day)
    hour = '{:02d}'.format(timeNow.hour)
    minute = '{:02d}'.format(timeNow.minute)
    second = '{:02d}'.format(timeNow.second)

    currentTime = '{}-{}-{} {}:{}:{}'.format(day, month, year, hour, minute, second)
    if PHOTORESISTOR208 == 1:
	r208=inforRoom("208",timeNow)
	list.append(r208)
	msg = "208 have gone out"
	sendEmail(msg)

    if PHOTORESISTOR308 == 1:
	r308=inforRoom("308",timeNow)
        list.append(r308)
	msg = "308 have gone out" 
	sendEmail(msg)

def sendEmail(msg):
    subject = "ROOM HAVE MISTAKE AFTER 10 pm"
    server=smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    server.login("thao.ngopn@gmail.com","thao180899")
    server.sendmail("thao.ngopn@gmail.com","thao.ngopn@gmail.com",msg,subject)
    server.quit()

def exit():
	sys.exit()

def destroy():
    GPIO.cleanup()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        destroy()

