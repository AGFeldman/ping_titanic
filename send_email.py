# Based on http://dzone.com/snippets/send-email-attachments-python

import smtplib
import os
from email.mime.text import MIMEText
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email import Encoders


def send(from_address, to_address, subject, text, attachment=None):
    msg = MIMEMultipart()
    msg['From'] = from_address
    msg['To'] = to_address
    msg['Subject'] = subject
    msg.attach(MIMEText(text))

    if attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(open(attachment, 'rb').read())
        Encoders.encode_base64(part)
        part.add_header(
                'Content-Disposition',
                'attachment; filename="%s"' % os.path.basename(attachment))
        msg.attach(part)

    s = smtplib.SMTP('localhost')
    s.sendmail(from_address, to_address.split(', '), msg.as_string())
    s.quit()
