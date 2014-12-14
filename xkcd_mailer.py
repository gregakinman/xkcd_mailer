#!/usr/bin/env python

"""
A fun little script, designed to run in a cron job on Mondays, Wednesdays, and Fridays, to get xkcd automatically
delivered to your inbox.

According to xkcd.com, xkcd updates without fail every Monday, Wednesday, and Friday, so, theoretically, running a cron job each of those days will get the latest comic. Still need to find out at what time it gets updated, though. Exact timing is a work in progress. I reckon checking for an update is another possible workaround, but we'll try this method first.

There's probably already a solution out there to do this, and/or an easier way to do this. But I don't really care,
because this was fun to do.
"""

# Standard email, regex, and image scraping libraries.
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import re
import smtplib
from StringIO import StringIO

# Third-party web and image scraping libraries.
from bs4 import BeautifulSoup as BS
from PIL import Image
import requests

def main():

    """
    Main function. Pieces everything together.
    """

    # Grabs comic and metadata.
    comic_url, mouseover_text, comic_title, comic_number = comic_getter()

    # Saves comic image and mouseover text to current directory.
    comic = requests.get(comic_url)
    comic_id = "xkcd #" + comic_number + " - " + comic_title
    comic_filename = comic_id + ".png"
    if comic.status_code == 200:
        Image.open(StringIO(comic.content)).save("comics/" + comic_filename)
        with open("comics/" + comic_id + " - mouseover text.txt", "wb") as f:
            f.write(mouseover_text)

    # Sends email.
    email_sender(comic_filename, mouseover_text, comic_title, comic_number, comic_id)


def comic_getter():

    """
    Gets the URL of the comic, as well as metadata:

    Yeah, I know I didn't worry about the HTTP status code not being 200, but the world won't explode if it's not.

    :return comic_url:      The URL at which the image for the comic resides.
    :return mouseover_text: The mouseover text for the comic image.
    :return comic_title:    The title of the comic.
    :return comic_number:   The number of the comic.
    """

    # Pulls the source code into a DOM tree.
    page_request = requests.get("http://www.xkcd.com")
    soup = BS(page_request.text)

    # Gets the comic image and title and the mouseover text from the div in which the comic lives.
    img_div = soup.find_all(id="comic")[0].find("img")
    comic_url = img_div["src"]
    mouseover_text = img_div["title"]
    comic_title = img_div["alt"]

    # Extracts the comic number from the supplied permalink URL.
    text_with_number = unicode(soup.find_all(text=re.compile("Permanent link to this comic:"))[0]).encode("utf-8").lstrip()
    comic_number = re.findall("\d+", text_with_number)[0]

    return comic_url, mouseover_text, comic_title, comic_number


def email_sender(comic_filename, mouseover_text, comic_title, comic_number, comic_id):

    """
    Sends the email.

    :param comic_filename:  The name of the file in which the comic image resides.
    :param mouseover_text:  The mouseover text associated with the comic.
    :param comic_title:     The title of the comic.
    :param comic_number:    The number of the comic.
    :param comic_id:        A string that uniquely identifies this comic (combining the metadata).
    """

    send_from_and_to = "gregakinman@gmail.com"

    # Constructs the email message, including text, the image attachment, and metadata.
    msg = MIMEMultipart(
        From=send_from_and_to,
        To=send_from_and_to,
    )
    msg["Subject"] = comic_id
    msg.attach(MIMEText("Mouseover text: \"" + mouseover_text + "\""))
    with open("comics/" + comic_filename, "rb") as f:
        msg.attach(MIMEImage(f.read()))

    # Opens a Gmail SMTP server and sends the email.
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(send_from_and_to, "zimdbknowmporwhb")
    server.sendmail(send_from_and_to, send_from_and_to, msg.as_string())
    server.quit()


main()
