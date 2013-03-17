import smtplib

sender = 'agarwalpranaya@gmail.com'
receivers = ['agarwalpranaya@gmail.com']

message = """From: From Person <agarwalpranaya@gmail.com>
To: To Person <agarwalpranaya@gmail.com>
Subject: SMTP e-mail test

This is a test e-mail message.
"""

try:
       smtpObj = smtplib.SMTP('smtp.gmail.com',587)
       smtpObj.sendmail(sender, receivers, message)         
       print "Successfully sent email"
except:
       print "Error: unable to send email"

