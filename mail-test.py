import smtplib
from email.message import EmailMessage


# this gives the port needed for the gmail -- this is from the python article
port = 465

# this is from the video ???
port = 587 

EMAIL_ADDRESS = os.environ.get('EMAIL_USER')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASS')

msg = EmailMessage()
msg['Subject'] = 'Grab dinner this weekend?'
msg['From'] = EMAIL_ADDRESS
msg['To'] = 'sc2830059@gmail.com'
msg.set_content('How about dinner at 6pm this Saturday')


with smtplib.SMTP('smtp.gmail.com', port) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()

        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

        # Sender, Receiver, msg 
        smtp.send_message(msg)