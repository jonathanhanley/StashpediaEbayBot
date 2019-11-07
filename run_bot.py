import re
import requests
import discord
from discord.ext import commands

TOKEN = 'TOKEN HERE'
description = ''''''
bot = commands.Bot(command_prefix='?', description=description)


def stash(name):
    name = name.replace(' ', '+')
    search_page = requests.get('https://stashpedia.com/search?terms=%s' % name)
    search_page = search_page.text
    link = re.findall('<a class="fill-height" href="(.*?)"', search_page)[0]
    link = 'https://stashpedia.com' + link
    main_page = requests.get(link)
    main_page = main_page.text
    number = '#'+str(re.findall('<H5>#(.*?)<', main_page)[0])
    stash_price = re.findall('<span class="gridValue">(.*?)<', search_page)[0]
    title = re.findall('<H4 class="toUpperCase">(.*?)<', search_page)[0]
    image_link = 'https://stashpedia.com'+re.findall('img-responsive gridImage" src="(.*?)"', search_page)[0]
    return stash_price, title, number, image_link, link


def ebay(search):
    link = 'https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2334524.m570.l1313.TR12.TRC2.A0.H0.XTEST.TRS0&_nkw=%s' \
           '&_sacat=0&LH_TitleDesc=0&_osacat=0&_odkw=%%23101' % search
    search_page = requests.get(link)
    search_page = search_page.text
    price = re.findall('<span class="s-item__price">(.*?)<', search_page)[0]
    return price


def main(name):
    stash_price, title, number, image_link, link = stash(name)
    ebay_search = (title+' '+number).replace(' ', '+').replace('#', '%23')
    ebay_price = ebay(ebay_search)

    embed = discord.Embed(title=title, url=link, description="", color=0x00ff00)
    embed.add_field(name="Ebay Price", value=ebay_price, inline=False)
    embed.add_field(name="Stashpedia Price", value=stash_price, inline=False)
    embed.set_image(url=image_link)

    return embed


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@bot.event
async def on_message(message):
    if message.content.startswith('!funko'):
        name = message.content.split(' ')[1:]
        name = ' '.join(name)
        embed = main(name)
        await bot.send_message(message.channel, embed=embed)


bot.run(TOKEN)
