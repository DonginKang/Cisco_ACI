# -*- coding: utf8 -*-

import socket
import sys
import coolsms
import time
import smtplib

from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from sinchsms import SinchSMS
from datetime import datetime as dt

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login("ID@gmail.com", "PASSWORD")
Customer_Mails=["ID@naver.com","ID@lgnsys.com"] # 고객분들 메일 주소를 적어 주시면 됩니다.

option = raw_input("1 : Cs_SMS, 2 : Sinch_SMS")

if(option == "1"):  #Cs_SMS 함수 사용할 경우 1번, Sinch_SMS 함수 사용할경우 2번
	
	# Cs_SMS 함수 사용할 경우 
	cs = coolsms.sms(True)
	cs.appversion("TEST/1.0")
	cs.setuser("ID", "PASSWORD")  # coolsms 아이디와 비밀번호
	cs.charset("utf8")
	cs.setattachdir("")
	Customer_Numbers =["NUMBER","NUMBER"]  #EX) 01052520522

else:
	#Sinch_SMS 함수 사용할 경우 

	your_app_key ="key"         # Sinch_sms에서 받은 key 값 
	your_app_secret = "secret"  # Sinch_sms에서 받은 secret 값 

	Customer_Numbers =["+8210"] # 폰번호 

	
	
def Cs_SMS(Customer_Number):
	
	message = 'Storming Detection!!!'
	cs.addsms(Customer_Number,"PHONE NUMBER",message) # EX) 01052929292
	if cs.connect():
		nsent = cs.send()
	print("Sending '%s' to %s" % (message, Customer_Number))


def Sinch_SMS(Customer_Number):

	message = 'Storming Detection!!!'
	
	client = SinchSMS(your_app_key, your_app_secret)
	client.send_message(Customer_Number, message)
	
	print("Sending '%s' to %s" % (message, Customer_Number))

	


def Aci_Mail(data,address):

    fromaddr = "id@gmail.com"
    toaddr = address

    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Storming Detection!!!"   # 고객에게 보낼 메일 제목 입니다.
	#data = "메일 내용"  # 메일 내용을 변경 하시고 싶으실 경우에 앞에 #자를 없애주시고 사용하시면 됩니다. (Default : APIC에서 보낸 LOG 원본)
    msg.attach(MIMEText(data, 'plain'))
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    print " -- Mail Completion -- "
	

	
port = 514
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("", port))
print "waiting on port:", port
while 1:
	data, addr = s.recvfrom(1024)
	Date_Time = str(dt.now())
	pos = Date_Time.find(".")
	print "[%s]" %Date_Time[:pos+3],data
	if "disconnect" in data:  # log중에 "disconnect" 문구가 있으면 메일 보내기가 실행 됩니다 
		#for Customer_number in Customer_Numbers:
		#	Sinch_SMS(Customer_number)
		for Customer_Number in Customer_Numbers:
			Cs_SMS(Customer_Number)
		#for Customer_mail in Customer_Mails:
		#	Aci_Mail(data,Customer_mail)

			
			
			
