"""
marketbot.py: Automated price checker for the Steam Community Marketplace.

author: Frank Liu - frank.zijie@gmail.com
last modified: 05/21/2015

Copyright (c) 2015, Frank Liu
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.
    * Neither the name of the Frank Liu (fzliu) nor the
      names of its contributors may be used to endorse or promote products
      derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL Frank Liu (fzliu) BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

TODOs:
  - automatically download and install dependencies
"""

import argparse
from email.mime.text import MIMEText
import os
import smtplib
import subprocess
import sys
import time

# argparse
parser = argparse.ArgumentParser(description="Bot for the steam community marketplace.")
parser.add_argument("-w", "--weapon", type=str, required=True, help="weapon name")
parser.add_argument("-s", "--skin", type=str, required=True, help="skin name")
parser.add_argument("-e", "--exterior", type=str, required=True, help="exterior wear")
parser.add_argument("-b", "--budget", type=float, required=True, help="threshold price")
parser.add_argument("-p", "--phone", type=long, required=True, help="phone number for notifications")

# addresses for email-to-sms
EMAIL_TO_SMS = [
    "txt.att.net",
    "tmomail.net",
    "vtext.com",
    "messaging.sprintpcs.com",
    "vmobl.com",
    "mmst5.tracfone.com",
    "mymetropcs.com",
    "myboostmobile.com",
    "sms.mycricket.com",
    "messaging.nextel.com",
    "message.alltel.com",
    "ptel.com",
    "tms.suncom.com",
    "qwestmp.com",
    "email.uscc.net"
]

# plain text authentication file
GMAIL_AUTH_FNAME = ".gmail_auth"
GMAIL_SMTP_SERVER = "smtp.gmail.com"
GMAIL_SMTP_PORT = 587

# temporary output filename from pricecheck script
PRICECHECK_OUT_FNAME = "price.tmp"

# milliseconds between requests
SLEEP_TIME = 200


def _checkdep(cmd):

    # OSError is raised upon failure
    try:
        with open(os.devnull, "w") as f:
            subprocess.check_call(cmd, std)
    except subprocess.CalledProcessError:
        return False

    return True


def setup():
    """
        Only checking for dependencies for now.
    """

    print("Verifying dependencies")
    
    # dependency check
    has_phantomjs = _checkdep(["phantomjs", "--version"])
    has_casperjs = _checkdep(["casperjs", "--version"])
    print("\thas phantomjs: {0}".format(has_phantomjs))
    print("\thas casperjs: {0}".format(has_casperjs))

    # quit if they are not available
    if not (has_phantomjs and has_casperjs):
        print("Both PhantomJS and CaasperJS must be installed.")
        print("Please make sure that they are available in your path.")
        sys.exit()


def sendsms(server, phone_num, body):
    """
        Send a text to the specified phone number.
    """

    # SMTP server
    msg = MIMEText(body)
    msg["To"] = phone_num
    msg["From"] = "marketbot"
    msg["Subject"] = "Marketplace notification"

    # loop through all possible addresses for the phone #
    addrs = [str(phone_num) + "@" + domain for domain in EMAIL_TO_SMS]
    try:
        server.sendmail("marketbot", addrs, msg.as_string())
    except:
        pass


if __name__ == "__main__":

    args = parser.parse_args()

    # start the bot
    print("marketbot:")
    print("    {0}".format(parser.description))
    print("-"*(4+len(parser.description)))
    setup()

    # get an SMTP server
    if os.path.isfile(GMAIL_AUTH_FNAME):
        with open(GMAIL_AUTH_FNAME, "r") as f:
            (user, passwd) = f.read().splitlines()
            server = smtplib.SMTP(GMAIL_SMTP_SERVER, GMAIL_SMTP_PORT)
            server.ehlo()
            server.starttls()
            server.login(user, passwd)
    # you'll need a local SMTP server running on port 2525
    # head over to github.com/fzliu/python-smtpsrv to grab one
    else:
        server = smtplib.SMTP("127.0.0.1", 2525)

    # set up the args for pricecheck
    weapon_arg = "--weapon=" + args.weapon
    skin_arg = "--skin" + args.skin
    wear_arg = "--wear" + args.exterior

    while(True):

        # grab the price
        cmd = ["casperjs", "pricecheck.js", weapon_arg, skin_arg, wear_arg]
        subprocess.call(cmd)

        # read in from the output file
        with open(PRICECHECK_OUT_FNAME, "r") as f:
            price = float(f.readline().strip())
            if price < args.budget:
                text = args.weapon + \
                    " | " + args.skin + \
                    " (" + args.exterior + ") " + \
                    "is now priced at {0}.".format(price)
                sendsms(server, args.phone, text)

        # sleep the thread
        time.sleep(SLEEP_TIME)

    server.quit()
