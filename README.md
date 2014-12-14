xkcd "daemon"
===

Automatically delivers xkcd to your mailbox (via a `cron` job), every day the comic is updated (which is every Monday, Wednesday, and Friday)! Also records a local backup of the comic for those rainy days when the entire Internet goes out but you still want to read every xkcd released since you created the `cron` job. Never forget to read the funniest webcomic in the world again. Oh, and, of course I remembered to grab the mouseover text, too.

If you want to receive these updates yourself, set up your own `cron` job by copying what I do! Or, if you know me personally, let me know, and I can add you to my mailing list in a flash. That is, as long as I still have fewer than 500 people signed up, due to Gmail's `SMTP` limits.

Requirements/Dependencies:
---

- [BeautifulSoup 4.3.2](http://www.crummy.com/software/BeautifulSoup/) (`$ pip install beautifulsoup4`)
- [Python Imaging Library (PIL) 1.1.7](http://www.pythonware.com/products/pil/) (`$ pip install PIL`)
- [Requests 2.5.0](http://docs.python-requests.org/en/latest/) (`$ pip install requests`)
- a) A Unix-like system (so that you have `cron`) and knowledge of or ability to learn how to set up a `cron` job with a specific `crontab` file[^1] OR b) knowledge of how to run a `cron`-like process on your own system

Usage:
---

The skeleton of the code is general. Just change the member variables of the `XKCDMailer` class to their corresponding assignments in your system. Also, make sure the `PYTHONPATH` assignment in the `xkcd_crontab` file points to where your third-party library modules live. If you're wondering where they live, start up your Python shell, `import` your modules, and check their `__file__` attributes.

Once your `crontab` file is set up properly, your `cron` job is up and running, and your member variables are changed to whatever they need to be for your setup, you're good to go. Happy comic reading!

TODO:
---

- I might change this to have a `cron` job running every weekday to check for a new post, since I read somewhere that sometimes xkcd updates more often than its normal MWF.

[^1]:
In case you're wondering: [here]()'s how.
