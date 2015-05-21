"""
marketbot.py: 

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
"""

import argparse
import json
import requests

# argparse
parser = argparse.ArgumentParser(description="Bot for the steam community marketplace.")
parser.add_argument("-k", "--key", type=str, required=True, help="weapon name")
parser.add_argument("-i", "--steamid", type=str, required=True, help="skin name")

# inventory API
INVENTORY_API_URL = "http://api.steampowered.com/IEconItems_730/GetPlayerItems/v0001/"


if __name__ == "__main__":

    args = parser.parse_args()

    # inventory URL
    url = INVENTORY_API_URL + "?key=" + args.key + "&SteamID=" + args.steamid

    data = {}
    while len(data) == 0:
        r = requests.get(url)
        data = json.loads(r.content)

    for item in data["result"]["items"]:
        print("\t{0}".format(item))