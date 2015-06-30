xkcd "daemon"
===

Every 5 minutes, polls to see if the latest xkcd hasn't been sent to you yet. Happens every 5 minutes because I want it
to be frequent enough that I receive every xkcd, since my personal laptop spends a lot of time closed while I'm working
a day job.

Dependencies:
---

- [BeautifulSoup 4.3.2](http://www.crummy.com/software/BeautifulSoup/) `$ pip install beautifulsoup4`
- [Python Imaging Library (PIL) 1.1.7](http://www.pythonware.com/products/pil/) `$ pip install PIL`
- [Requests 2.5.0](http://docs.python-requests.org/en/latest/) `$ pip install requests`
- [cron(8)](http://linux.die.net/man/8/cron) should be already installed on a \*nix system

Usage:
---

Takes a list of e-mail recipients defined in recipients.py, or can take a list of recipients from the command line.
