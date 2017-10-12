#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright © Odd Stråbø <oddstr13@openshell.no> 2017
# License: MIT - https://opensource.org/licenses/MIT
#

__doc__ = "A Discord bot for the Optimus 3D printer"
import logging

import requests

import discord

from gridrender import render

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


##################################

client = discord.Client()

@client.event
async def on_ready():
    print('Connected!')
    print('Username: ' + client.user.name)
    print('ID: ' + client.user.id)
    print('Add to server: https://discordapp.com/oauth2/authorize?client_id={id}&scope=bot&permissions=67488832'.format(id=client.user.id))

filelist = {}

@client.event
async def on_message(message):
    print(">>> {}: {}".format(message.author, message.content))
    print(message.embeds)
    print(message.attachments)
    for att in message.attachments:
        if att.get("filename") == "delta.grid":
            await client.send_typing(message.channel)

            with requests.get(att.get('url')) as rq:
                im = render(rq.content)

            filelist[message.id] = await client.send_file(message.channel, im, filename="delta.png")

@client.event
async def on_message_delete(message):
    print(message.id)
    print(message.embeds)
    print(message.attachments)
    if filelist.get(message.id):
        await client.delete_message(filelist.get(message.id))
        filelist.pop(message.id)

def main(args=[]):
    with open("TOKEN") as fh:
        client.run(fh.read().strip())

if __name__ == "__main__":
    import sys
    main(args=sys.argv[1:])
