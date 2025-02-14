import smtplib

email=input("email: ")
receipient=input("receipient: ")

subject=input("Subject: ")
message=input("message: ")

text=f"Subject: {subject}\n\n{message}"

server=smtplib.SMTP("smtp.gmail.com", 587)

server.starttls()

server.login(email, 'fpfthcetaetnuexr')

server.sendmail(email, receipient, text)

print("Email  has been sent to: "+ receipient)
