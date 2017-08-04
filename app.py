from flask import Flask, render_template, request, flash
import manager

app = Flask(__name__)
app.secret_key = 'random'

class Config:
	constants = {
		'TWILIO_ACCOUNT_SID' : 'AC97c45b70117319ef7aee95d51f0694ea',
		'TWILIO_AUTH_TOKEN' : '147e732fa8794aad59b31b7312e9bc72',
		'TWILIO_NUMBER' : '+16194734682'}

@app.route("/")
def main():
    return render_template('index.html')

@app.route('/showContacts', methods=['GET'])
def showContacts():
	contacts = manager.allData()
	return render_template('showContacts.html', params={'contacts':contacts})

@app.route('/selectContact', methods=['GET'])
def selectContact():
	user_id = request.args.get('user_id')
	user_details = manager.getUserData(user_id=user_id)
	otp = manager.generateRandomOTP()
	return render_template('selectContact.html', params={"user_id":user_id, "user_details":user_details, "otp":otp})

@app.route('/send', methods=['POST'])
def send():

	_otp = request.args.get('otp')
	_number = request.args.get('number')
	_user_id = request.args.get('user_id')
	_name = request.args.get('name')

	if _number[0:3] != '+91':
		_number = '+91'+_number
	result = manager.sendSMS(to_number=_number, body='Hi, Your OTP is: '+_otp, 
							user_id=_user_id, name=_name, otp=_otp)
	if result.get('error'):
		msg = result.get('error')
	else:
		msg = 'Message sent successfully to '+_number
	
	return render_template('displayResult.html', params={'msg':msg, 'number':_number, 'user_id':_user_id, 'name':_name})

@app.route('/showHistory', methods=['GET'])
def showHistory():

	details = manager.getHistory()
	return render_template('communicationHistory.html',params={'details':details})

if __name__ == "__main__":
    app.run()