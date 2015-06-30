#!/usr/bin/env python

from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import re
import smtplib
from StringIO import StringIO
import sys

from bs4 import BeautifulSoup as BS
from PIL import Image
import requests

from recipients import recipients as RECIPIENTS

def main(recipients):

    mailer = XKCDMailer(recipients)
    mailer.run()


class XKCDMailer(object):

    def __init__(self, recipients):

        # Throwaway email address I made just for this instance. Please don't use it - make your own.
        # Also, that password doesn't go to anything else, and there's no sensitive information in that inbox.
        self.send_from = "xkcddaemon@gmail.com"
        self.send_to = recipients
        self.password = "TendeBeneAltaPete"
        self.dump_dir_path = "/Users/gregakinman/google_drive/Work/Projects/scripts/xkcd_mailer/comics/"

    def run(self):

        self.__get_comic()
        self.__send_mail()

    def __get_comic(self):

        # Pulls the source code into a DOM tree.
        page_request = requests.get("http://www.xkcd.com")
        soup = BS(page_request.text)

        # Gets the comic image and title and the mouseover text from the div in which the comic lives.
        img_div = soup.find_all(id="comic")[0].find("img")
        comic_url = "http:" + img_div["src"]
        self.mouseover_text = img_div["title"]
        comic_title = img_div["alt"]

        # Extracts the comic number from the supplied permalink URL.
        text_with_number = (unicode(soup.find_all(text=re.compile("Permanent link to this comic:"))[0]).encode("utf-8")
                .lstrip())
        comic_number = re.findall("\d+", text_with_number)[0]

        # Dumps the comic image and mouseover text to files in a subdirectory.
        comic = requests.get(comic_url)
        self.comic_id = "xkcd #" + comic_number + " - " + comic_title
        self.comic_filename = self.comic_id + ".jpg"
        if comic.status_code == 200:
            Image.open(StringIO(comic.content)).save(self.dump_dir_path + self.comic_filename)
            with open(self.dump_dir_path + self.comic_id + " - mouseover text.txt", "wb") as f:
                f.write(self.mouseover_text)

    def __send_mail(self):

        # Constructs the email message, including text, the image attachment, and metadata.
        msg = MIMEMultipart(From=self.send_from, To=", ".join(self.send_to))
        msg["Subject"] = self.comic_id
        msg.attach(MIMEText("Today's xkcd - enjoy!\n\nMouseover text: \"" + self.mouseover_text + "\""))
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
