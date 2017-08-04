import psycopg2
import random
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from requests.exceptions import ConnectionError
import app
import datetime

# class DBOperations:

conn_str = "host='localhost' dbname='user_communication' password='postgres' user='postgres'"
conn = psycopg2.connect(conn_str)
cursor =conn.cursor()

def allData():
	cursor.execute("SELECT * FROM users")
	records = cursor.fetchall()
	return records

def getUserData(user_id):
	cursor.execute("SELECT * FROM users where user_id=%s", (user_id))
	record = cursor.fetchone()
	return record

def generateRandomOTP():
	otp = random.randint(100000,999999)
	return otp

def sendSMS(to_number,body,user_id,name,otp):
	account_sid = app.Config.constants.get('TWILIO_ACCOUNT_SID')
	auth_token = app.Config.constants.get('TWILIO_AUTH_TOKEN')
	twilio_number = app.Config.constants.get('TWILIO_NUMBER')
	client = Client(account_sid, auth_token)
	time = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
	try:
		response = client.api.messages.create(to_number,
                           from_=twilio_number,
                           body=body)
	except ConnectionError:
		return {'error': 'Something went wrong with the network.Try after sometime.'}
	
	except TwilioRestException:
		return {'error' : 'Invalid Phone Number. Should be registered with the Twilio account.'}
	
	if to_number[0:3] == '+91':
		to_number = to_number[3:]
	cursor.execute("INSERT INTO communication_history (user_id,name,phone_number,sent_at,otp) VALUES (%s, %s, %s, %s, %s)", 
					(user_id,name,to_number,time,otp))
	return {'response':response, 'time':time}

def getHistory():
	cursor.execute("SELECT * from communication_history order by sent_at desc")
	records = cursor.fetchall()
	return records