import ssl
import re
import requests
import urllib.request
import shutil
import os
import discord
from discord.ext import commands
import asyncio
from discord.utils import get
TOKEN = 'NDYwNDExNjUyODgyNDMyMDAw.DkjI0Q.7GxoJ_IDBXldPGdm8KXOKHFXJR8'

def stash(name):
    name=name.replace(' ','+')
    searchPage=requests.get('https://stashpedia.com/search?terms=%s'%(name))
    searchPage=searchPage.text
    link=re.findall('<a class="fill-height" href="(.*?)"', searchPage)[0]
    link='https://stashpedia.com'+link
    mainPage=requests.get(link)
    mainPage=mainPage.text
    number='#'+str(re.findall('<H5>#(.*?)<', mainPage)[0])
    stashPrice=re.findall('<span class="gridValue">(.*?)<', searchPage)[0]
    title=re.findall('<H4 class="toUpperCase">(.*?)<', searchPage)[0]
    imageLink='https://stashpedia.com'+re.findall('img-responsive gridImage" src="(.*?)"', searchPage)[0]
    return (stashPrice,title,number,imageLink,link)

def ebay(search):
    link='https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2334524.m570.l1313.TR12.TRC2.A0.H0.XTEST.TRS0&_nkw=%s&_sacat=0&LH_TitleDesc=0&_osacat=0&_odkw=%%23101'%(search)
    print(link)
    searchPage=requests.get(link)
    searchPage=searchPage.text
    title = re.findall('<h3 class="s-item__title" role="text">(.*?)<', searchPage)[0]
    price = re.findall('<span class="s-item__price">(.*?)<', searchPage)[0]
    return price
    pass

def main(name):
    stashPrice,title,number,imageLink,link=stash(name)
    ebaySearch=(title+' '+number).replace(' ','+').replace('#','%23')
    ebayPrice=ebay(ebaySearch)

    mess='''**%s**
*Ebay Price*
%s
*Stashpedia Price*
%s
*Link*
<%s>
'''%(title,ebayPrice,stashPrice,link)
    embed = discord.Embed(title=title, url=link,description="", color=0x00ff00)
    embed.add_field(name="Ebay Price", value=ebayPrice, inline=False)
    embed.add_field(name="Stashpedia Price", value=stashPrice, inline=False)
    embed.set_image(url=imageLink)

    return (embed)
'''
esl._create_default_https_context = ssl._create_unverified_context
fp = requests.get('https://twitter.com/BotBroker')
fp = fp.text
print(fp)
'''

description = ''''''
bot = commands.Bot(command_prefix='?', description=description)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.event
async def on_message(message):
   if message.content.startswith('!funko'):
       name=(message.content).split(' ')[1:]
       name=' '.join(name)
       embed=main(name)
       await bot.send_message(message.channel, embed=embed)


bot.run(TOKEN)