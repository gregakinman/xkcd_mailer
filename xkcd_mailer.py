#!/usr/bin/env python

"""
A fun little program, designed to run in a cron job on Mondays, Wednesdays, and Fridays, to get xkcd automatically
delivered to your inbox.

According to xkcd.com, xkcd updates without fail every Monday, Wednesday, and Friday, so, theoretically, running a cron
job each of those days will get the latest comic. Still need to find out at what time it gets updated, though. Exact
timing is a work in progress. I reckon checking for an update is another possible workaround, but we'll try this method
first.

There are definitely easier & non-programmatic ways to do this (e.g., ITTT), but this was more of a fun exercise for
learning cron jobs and helping myself to stop forgetting to read xkcd. Also, this has the added advantage of easily
adding new emails to the list, so it's a mailing list, of sorts.
"""

# Standard email, regex, and image scraping libraries.
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import re
import smtplib
from StringIO import StringIO
import sys

# Third-party web and image scraping libraries.
from bs4 import BeautifulSoup as BS
from PIL import Image
import requests

# Imports outsourced mailing list module.
from recipients import recipients as RECIPIENTS

def main(recipients):

    """
    Main function. Instantiates and runs the process.
    """

    mailer = XKCDMailer(recipients)
    mailer.run()


class XKCDMailer(object):

    """
    Wrapper class for xkcd-emailing metadata and functionality.
    """

    def __init__(self, recipients):

        """
        Constructs a new instance, initially with just to and from designations.

        :param self:    The current instance.
        """

        # This is a throwaway email address I made just for this instance. Please don't use it - make your own.
        # Also, that password doesn't go to anything else, and there's no sensitive information in that inbox.
        self.send_from = "xkcddaemon@gmail.com"
        # TODO: CHANGE BACK ZOMG
        self.send_to = recipients
        self.password = "TendeBeneAltaPete"
        self.dump_dir_path = "/Users/gregakinman/Google Drive/Work/Projects/scripts/xkcd_mailer/comics/"

    def run(self):

        """
        Main method. Pieces everything together.

        :param self:    The current instance.
        """

        # Saves comic image and mouseover text to current directory.
        self.__comic_getter()

        # Sends email.
        self.__email_sender()

    def __comic_getter(self):

        """
        Internal helper method. Gets the URL of the comic, as well as metadata:

        Yeah, I know I didn't worry about the HTTP status code not being 200, but the world won't explode if it's not.

        :param self:    The current instance.
        """

        # Pulls the source code into a DOM tree.
        page_request = requests.get("http://www.xkcd.com")
        soup = BS(page_request.text)

        # Gets the comic image and title and the mouseover text from the div in which the comic lives.
        img_div = soup.find_all(id="comic")[0].find("img")
        comic_url = img_div["src"]
        self.mouseover_text = img_div["title"]
        comic_title = img_div["alt"]

        # Extracts the comic number from the supplied permalink URL.
        text_with_number = (unicode(soup.find_all(text=re.compile("Permanent link to this comic:"))[0])
            .encode("utf-8").lstrip())
        comic_number = re.findall("\d+", text_with_number)[0]

        # Dumps the comic image and mouseover text to files in a subdirectory.
        comic = requests.get(comic_url)
        self.comic_id = "xkcd #" + comic_number + " - " + comic_title
        self.comic_filename = self.comic_id + ".jpg"
        if comic.status_code == 200:
            Image.open(StringIO(comic.content)).save(self.dump_dir_path + self.comic_filename)
            with open(self.dump_dir_path + self.comic_id + " - mouseover text.txt", "wb") as f:
                f.write(self.mouseover_text)

    def __email_sender(self):

        """
        Internal helper method. Sends the email.

        :param self:    The current instance.
        """

        # Constructs the email message, including text, the image attachment, and metadata.
        msg = MIMEMultipart(From=self.send_from, To=", ".join(self.send_to))
        msg["Subject"] = self.comic_id
        msg.attach(MIMEText("Today's xkcd - enjoy!\nMouseover text: \"" + self.mouseover_text + "\""))
        with open(self.dump_dir_path + self.comic_filename, "rb") as f:
            msg.attach(MIMEImage(f.read()))

        # Opens a Gmail SMTP server and sends the email.
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(self.send_from, self.password)
        server.sendmail(self.send_from, self.send_to, msg.as_string())
        server.quit()


if __name__ == "__main__":
    # Optional command-line args: any number of specific emails can be specified on the command-line.
    if len(sys.argv) > 1:
        main(sys.argv[1:])
    # If no specific emails are specified (as in the cron job), sends to all recipients on the mailing list.
    else:
        main(RECIPIENTS)
