
from datetime import datetime
from datetime import timezone
from datetime import timedelta

import discord
import requests

def get_time():
    return datetime.now(timezone.utc)

def compare_time(time1, time2, change):
    delta = time2 - time1
    
    if change == 0:
        return delta.total_seconds()
    
    if delta > change:
        return 0
    else:
        return delta.total_seconds()


pfp = "https://cdn.discordapp.com/emojis/729928591399321632.png"

def created_embed(
title = None, url = None,#title text and it's linked
colour = discord.Colour(0x7e8af7), #colour
description = None, #named links + discord md
timestamp = None, #datetime.datetime, probably won't ever use it
image = None, #full image
thumbnail = None, #top pic thingy
author = ("Witch", "", pfp), # (author text, linked url, pic url)
footer = ("Witch",pfp), # (footer text, pic url)
fields = None #expects (name, value, inline), value supports named links + discord md as well
):
    """Creates Embed

    Big Parameters
    -----------
    author: :class:`(str, str, str)`
        Author text, Url link, Author image url. 
    footer: :class:`(str,str)`
        Footer text, Icon url.
    fields: :class:`[(str,str,bool)]`
        Array of tuples`(Name, Value, Inline)`.
    """
    if url: embed = discord.Embed(url = url)
    else: embed = discord.Embed()
    if title: embed.title = title
    embed.colour = colour
    if timestamp: embed.timestamp = timestamp
    if description: embed.description = description

    if image: embed.set_image(url=image)
    if thumbnail: embed.set_thumbnail(url=thumbnail)
    embed.set_author(name=author[0], url=author[1], icon_url=author[2])
    embed.set_footer(text=footer[0], icon_url=footer[1])

    if fields:
        for field in fields:
            embed.add_field(name=field[0], value=field[1], inline=field[2])


    return embed

    def get_json(url, headers = {}):   
        r = requests.get(url, headers=headers)
        return r.json()

if __name__ == "__main__":
    pass