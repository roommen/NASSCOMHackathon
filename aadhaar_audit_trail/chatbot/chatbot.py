import urllib
import json
import os
import time
import hashlib
import pandas as pd
from flask import Flask 
from flask import request
from flask import make_response
import psycopg2
conn = psycopg2.connect("dbname=uidai_repo user=dbadmin password=admin1234 host=uidairepo.clpayxv3izmg.ap-south-1.rds.amazonaws.com port=5432")

app = Flask(__name__)

def check_num_string(msg):
	"""This function check if a 12 digit number string is given as user message, with/without strings"""
	try:
		num = msg.replace(' ','')
		int(num)
		if len(num)==10:
			return True
		else:
			return False
	except:
		return False

@app.route("/webhook", methods = ["POST"])
def webhook():
	req = request.get_json(silent = True, force = True)
	print ("Request:")
	print (json.dumps(req, indent = 4))
	res = makeWebhookResult(req)
	res = json.dumps(res, indent = 4)
	print (res)
	r = make_response(res)
	r.headers['Content-Type'] = 'application/json'
	return r
	
	
def makeWebhookResult(req):
	speech = ''
	if req.get("result").get("action")!= "input.unknown":
		return {}
	user_msg = req.get("result").get("resolvedQuery")

	if user_msg.lower() in ['hi','hello','hey']:
		print('Greeting detected')
		speech = 'Hi! Please enter your Aadhaar Number'

	elif check_num_string(user_msg):
		print('Checking for Aadhaar Number')
		try:
			final_data = ''
			cur = conn.cursor()
			query = "select * from aadhaar_info where aadhaar_number=" + str(user_msg)
			cur.execute(query)
			for i in cur.fetchall():
				final_data = str(i[0]) + ' ' + str(i[1]) + ' ' + str(i[4]) + ', ' + str(i[5])
			print(final_data)
			with open('tempdata.txt', 'w') as myfile:
				myfile.write(str(final_data))
		except:
			print("exception")
			speech = 'Enter the correct aadhar number'
		#Making a json file to store the aadhaar number sent by the user
		if final_data:
			cur1 = conn.cursor()
			query = "insert into aadhaar_authentication_hist values(default," + str(user_msg) + ",'OTP',current_timestamp,'Aadhaar BOT');"
			print(query)
			cur1.execute(query)
			conn.commit()

			speech = 'Enter the OTP sent to your registered mobile number to authenticate'
		else:
			speech = 'Enter the correct aadhar number'

	elif len(user_msg) == 6:
		print('OTP Correct')
		with open('tempdata.txt', 'r') as myfile:
			data = myfile.read()
		speech = data
		# # Since the access of aadhaar details of this user was detected, an entry to the blockchain stream is generated
		# os.system("multichain-cli aadhaar publish demo '{\"app\": \"Skype AadhaarBot\",\"date\": \""+str(cur_date)+"\",\"time\": \""+str(cur_time)+"\",\"ip_addr\": \"103.203.139.3\",\"auth_type\": \"otp\"}' "+m1)
	print ("Responses:")
	print (speech)
	return{
		"speech": speech,
		"displayText": speech,
		"source": "Aadhaar_ChatBot"
		}
 
if __name__ == '__main__':
	port= int(os.getenv('PORT',8080))
	app.run(debug=True, port=port, host='0.0.0.0')
