#!/usr/bin/env python

from PIL import Image

from StringIO import StringIO

import requests

# GET URL OF IMAGE

# DEFINE WHAT image_url IS
comic = requests.get(comic_url)
if comic.status_code == 200:
    Image.open(StringIO(comic.content)).save("comic.png")



#!/usr/bin/env python

import smtplib

import os
from os.path import basename

import urllib


from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate

# GET IMAGE FILE AND TEXT



# Open a plain text file for reading.  For this example, assume that
# the text file contains only ASCII characters.
fp = open(textfile, 'rb')
# Create a text/plain message
msg = MIMEText(fp.read())
fp.close()

# me == the sender's email address
# you == the recipient's email address
msg['Subject'] = 'The contents of %s' % textfile
msg['From'] = me
msg['To'] = you

# Send the message via our own SMTP server, but don't include the
# envelope header.
s = smtplib.SMTP('localhost')
s.sendmail(me, [you], msg.as_string())
s.quit()


"""
for f in files or []:
    with open(f, "rb") as fil:
        msg.attach(MIMEApplication(
            fil.read(),
            Content_Disposition='attachment; filename="%s"' % basename(f)
        ))
"""
