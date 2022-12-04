import os 
import smtplib
from email.message import EmailMessage
import imghdr
import pdfkit 


#THIS IS ANOTHER WAY TO DO IT 
pdfkit.from_file('songs.html', 'results.pdf') 


# this gives the port needed for the gmail -- this is from the python article
port = 465

# this is from the video ???
port = 587 

EMAIL_ADDRESS = os.environ.get('EMAIL_USER')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASS')

msg = EmailMessage()
msg['Subject'] = 'Check out my results!'
msg['From'] = EMAIL_ADDRESS
msg['To'] = 'sc2830059@gmail.com' 
msg.set_content('How about dinner at 6pm this Saturday')

# lists for JPGs and PDFs
files = ['creators.jpg', 'city.jpg']
pdffiles = ['results.pdf']

# for loop for JPGs
for file in files:
    # adds an attachment of an image to the email
    with open(file, 'rb') as f: 
        file_data = f.read()
        file_type = imghdr.what(f.name)
        filename = f.name

# for loop for PDF 
for pdffile in pdffiles:
    # adds an attachment of an image to the email
    with open(pdffile, 'rb') as x: 
        pdffile_data = x.read()
        pdffilename = x.name


msg.add_attachment(file_data, maintype='image', subtype=file_type, filename=filename)
msg.add_attachment(pdffile_data, maintype='application', subtype="octet-stream", filename=pdffilename)

msg.add_alternative("""\ 
<! DOCTYPE html>
<html>
    <body>
        <h1 style="color: SlateGray;">This is an HTML Email!</h1>
    </body>
</html>
""", subtype='html')

with smtplib.SMTP('smtp.gmail.com', port) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()

        # send the email and the message
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)