
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

def secsFormat(secs):
    time = ""
    suffix = ""
    seconds = secs
    decimals = seconds - seconds // 1
    seconds -= decimals

    days = seconds // (24*60*60)
    seconds -= days*24*60*60
    hours = seconds // (60*60)
    seconds -= hours*60*60
    minutes = seconds // 60
    seconds -= minutes*60
    #left with days hours minute seconds

    if days == 1: time += "1 day"
    elif days: time += f"{days} days"
    if days and (hours or minutes or seconds or decimals): 
        time += ", "

    if hours:#day and hour
        time += f"{hours}:"
        suffix = " hrs" if hours != 1 else " hr"
    
    if minutes:
        if not hours:
            time += f"{minutes}:"
            suffix = " min"
        else:
            time += f"{twoDigit(minutes)}:"
    elif hours and not minutes:
        time += "00:"

    if seconds:
        if not (hours or minutes): 
            time += str(seconds)
            suffix = " sec"
        else:
            time += f"{twoDigit(seconds)}"
    elif (hours or minutes) and not seconds:
        time += "00"
    #if float is inputted get rid of decimals
    time = time.replace('.0','')

    if decimals:
        time += '{:.3}'.format(decimals)[1:]
    elif not (hours or minutes or seconds) and decimals:
        time += '{:.3}'.format(decimals)
        suffix = " sec"
    #print(f"{days},{hours}:{minutes}:{seconds}")
    return (time + suffix) or 0

def decRound(num,n):
    return '%.0f'.replace("0",str(n))%(num)


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