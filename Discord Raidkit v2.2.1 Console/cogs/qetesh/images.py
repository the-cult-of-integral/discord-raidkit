"""
Discord Raidkit v2.2.1 by the-cult-of-integral
"The trojan horse of discord raiding"
Last updated: 16/06/2022
"""

import random
import sqlite3

import discord
from discord.ext import commands

from colorama import *; init()

CONNECTION_STRING = "qetesh_db.db"


class Images(commands.Cog):
    def __init__(self, bot):
        self.conn = sqlite3.connect(CONNECTION_STRING)
        self.link = ""
        self.previous_link = ""
        self.start()  
        self.bot = bot   
    
    def execute(self, *args):
        try:
            self.c = self.conn.cursor()
            self.c.execute(*args)
            self.c.close()
        except Exception as Error:
            print(str(Error))

    def insert_link(self, link, category):
        print(f"Inserting into database: {category}, {link}")
        self.execute("INSERT OR IGNORE INTO links VALUES (?, ?)", (category, link))

    def create_links_table(self):
        print("Creating table")
        self.execute("""CREATE TABLE links (
                category TEXT,
                link TEXT,
                UNIQUE(category, link))""")

    def start(self):
        try:
            self.create_links_table()
        except sqlite3.Error as Error:
            print(Error)
        
        with open("cogs/qetesh/vagl/vagl_links.txt", "r") as file: 
            links = file.read().split("\n")
            [self.insert_link(link, "vagl") for link in links]
        
        with open("cogs/qetesh/oral/oral_links.txt", "r") as file: 
            links = file.read().split("\n")
            [self.insert_link(link, "oral") for link in links]
        
        with open("cogs/qetesh/anal/anal_links.txt", "r") as file: 
            links = file.read().split("\n")
            [self.insert_link(link, "anal") for link in links]

        with open("cogs/qetesh/lesbian/lesbian_links.txt", "r") as file: 
            links = file.read().split("\n")
            [self.insert_link(link, "lesbian") for link in links]

        with open("cogs/qetesh/gay/gay_links.txt", "r") as file: 
            links = file.read().split("\n")
            [self.insert_link(link, "gay") for link in links]
        
        with open("cogs/qetesh/tits/tits_links.txt", "r") as file: 
            links = file.read().split("\n")
            [self.insert_link(link, "tits") for link in links]
        
        with open("cogs/qetesh/ass/ass_links.txt", "r") as file: 
            links = file.read().split("\n")
            [self.insert_link(link, "ass") for link in links]
        
        with open("cogs/qetesh/pussy/pussy_links.txt", "r") as file: 
            links = file.read().split("\n")
            [self.insert_link(link, "pussy") for link in links]

        with open("cogs/qetesh/cock/cock_links.txt", "r") as file: 
            links = file.read().split("\n")
            [self.insert_link(link, "cock") for link in links]

        with open("cogs/qetesh/asian/asian_links.txt", "r") as file:
            links = file.read().split("\n")
            [self.insert_link(link, "asian") for link in links]

        with open("cogs/qetesh/amateur/amateur_links.txt", "r") as file:
            links = file.read().split("\n")
            [self.insert_link(link, "amateur") for link in links]

        with open("cogs/qetesh/hentai/hentai_links.txt", "r") as file:
            links = file.read().split("\n")
            [self.insert_link(link, "hentai") for link in links]

        with open("cogs/qetesh/milf/milf_links.txt", "r") as file:
            links = file.read().split("\n")
            [self.insert_link(link, "milf") for link in links]

        with open("cogs/qetesh/teen/teen_links.txt", "r") as file:
            links = file.read().split("\n")
            [self.insert_link(link, "teen") for link in links]

        with open("cogs/qetesh/ebony/ebony_links.txt", "r") as file:
            links = file.read().split("\n")
            [self.insert_link(link, "ebony") for link in links]

        with open("cogs/qetesh/threesome/threesome_links.txt", "r") as file:
            links = file.read().split("\n")
            [self.insert_link(link, "threesome") for link in links]

        with open("cogs/qetesh/cartoon/cartoon_links.txt", "r") as file:
            links = file.read().split("\n")
            [self.insert_link(link, "cartoon") for link in links]

        with open("cogs/qetesh/creampie/creampie_links.txt", "r") as file:
            links = file.read().split("\n")
            [self.insert_link(link, "creampie") for link in links]

        with open("cogs/qetesh/bondage/bondage_links.txt", "r") as file:
            links = file.read().split("\n")
            [self.insert_link(link, "bondage") for link in links]

        with open("cogs/qetesh/squirt/squirt_links.txt", "r") as file:
            links = file.read().split("\n")
            [self.insert_link(link, "squirt") for link in links]

        with open("cogs/qetesh/yiff/yiff_links.txt", "r") as file:
            links = file.read().split("\n")
            [self.insert_link(link, "yiff") for link in links]
        
        with open("cogs/qetesh/neko/neko_links.txt", "r") as file: 
            links = file.read().split("\n")
            [self.insert_link(link, "neko") for link in links]
    
    def get_link(self, cat):
        self.c = self.conn.cursor()
        self.c.execute('SELECT * FROM links WHERE category = ?;', (cat,))

        self.link = random.choice(self.c.fetchall())[1]
        if self.link == self.previous_link:
            self.get_link(cat)
        else:
            self.previous_link = self.link
        self.c.close()

    @commands.command()
    @commands.is_nsfw()
    async def vagl(self, ctx):
        self.get_link('vagl')
        embed = discord.Embed()
        embed.set_image(url=self.link)
        await ctx.message.channel.send(embed=embed)

    @commands.command()
    @commands.is_nsfw()
    async def oral(self, ctx):
        self.get_link('oral')
        embed = discord.Embed()
        embed.set_image(url=self.link)
        await ctx.message.channel.send(embed=embed)
    
    @commands.command()
    @commands.is_nsfw()
    async def anal(self, ctx):
        self.get_link('anal')
        embed = discord.Embed()
        embed.set_image(url=self.link)
        await ctx.message.channel.send(embed=embed)

    @commands.command()
    @commands.is_nsfw()
    async def les(self, ctx):
        self.get_link('lesbian')
        embed = discord.Embed()
        embed.set_image(url=self.link)
        await ctx.message.channel.send(embed=embed)

    @commands.command()
    @commands.is_nsfw()
    async def gay(self, ctx):
        self.get_link('gay')
        embed = discord.Embed()
        embed.set_image(url=self.link)
        await ctx.message.channel.send(embed=embed)
    
    @commands.command()
    @commands.is_nsfw()
    async def tits(self, ctx):
        self.get_link('tits')
        embed = discord.Embed()
        embed.set_image(url=self.link)
        await ctx.message.channel.send(embed=embed)
    
    @commands.command()
    @commands.is_nsfw()
    async def ass(self, ctx):
        self.get_link('ass')
        embed = discord.Embed()
        embed.set_image(url=self.link)
        await ctx.message.channel.send(embed=embed)
    
    @commands.command()
    @commands.is_nsfw()
    async def pussy(self, ctx):
        self.get_link('pussy')
        embed = discord.Embed()
        embed.set_image(url=self.link)
        await ctx.message.channel.send(embed=embed)
    
    @commands.command()
    @commands.is_nsfw()
    async def cock(self, ctx):
        self.get_link('cock')
        embed = discord.Embed()
        embed.set_image(url=self.link)
        await ctx.message.channel.send(embed=embed)

    @commands.command()
    @commands.is_nsfw()
    async def asian(self, ctx):
        self.get_link('asian')
        embed = discord.Embed()
        embed.set_image(url=self.link)
        await ctx.message.channel.send(embed=embed)

    @commands.command()
    @commands.is_nsfw()
    async def amateur(self, ctx):
        self.get_link('amateur')
        embed = discord.Embed()
        embed.set_image(url=self.link)
        await ctx.message.channel.send(embed=embed)

    @commands.command()
    @commands.is_nsfw()
    async def hentai(self, ctx):
        self.get_link('hentai')
        embed = discord.Embed()
        embed.set_image(url=self.link)
        await ctx.message.channel.send(embed=embed)

    @commands.command()
    @commands.is_nsfw()
    async def milf(self, ctx):
        self.get_link('milf')
        embed = discord.Embed()
        embed.set_image(url=self.link)
        await ctx.message.channel.send(embed=embed)

    @commands.command()
    @commands.is_nsfw()
    async def teen(self, ctx):
        self.get_link('teen')
        embed = discord.Embed()
        embed.set_image(url=self.link)
        await ctx.message.channel.send(embed=embed)

    @commands.command()
    @commands.is_nsfw()
    async def ebony(self, ctx):
        self.get_link('ebony')
        embed = discord.Embed()
        embed.set_image(url=self.link)
        await ctx.message.channel.send(embed=embed)

    @commands.command()
    @commands.is_nsfw()
    async def threesome(self, ctx):
        self.get_link('threesome')
        embed = discord.Embed()
        embed.set_image(url=self.link)
        await ctx.message.channel.send(embed=embed)

    @commands.command()
    @commands.is_nsfw()
    async def cartoon(self, ctx):
        self.get_link('cartoon')
        embed = discord.Embed()
        embed.set_image(url=self.link)
        await ctx.message.channel.send(embed=embed)

    @commands.command()
    @commands.is_nsfw()
    async def creampie(self, ctx):
        self.get_link('creampie')
        embed = discord.Embed()
        embed.set_image(url=self.link)
        await ctx.message.channel.send(embed=embed)

    @commands.command()
    @commands.is_nsfw()
    async def bondage(self, ctx):
        self.get_link('bondage')
        embed = discord.Embed()
        embed.set_image(url=self.link)
        await ctx.message.channel.send(embed=embed)

    @commands.command()
    @commands.is_nsfw()
    async def squirt(self, ctx):
        self.get_link('squirt')
        embed = discord.Embed()
        embed.set_image(url=self.link)
        await ctx.message.channel.send(embed=embed)

    @commands.command()
    @commands.is_nsfw()
    async def yiff(self, ctx):
        self.get_link('yiff')
        embed = discord.Embed()
        embed.set_image(url=self.link)
        await ctx.message.channel.send(embed=embed)

    @commands.command()
    @commands.is_nsfw()
    async def neko(self, ctx):
        self.get_link('neko')
        embed = discord.Embed()
        embed.set_image(url=self.link)
        await ctx.message.channel.send(embed=embed)

