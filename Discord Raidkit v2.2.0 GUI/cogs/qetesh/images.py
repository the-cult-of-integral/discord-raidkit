"""
Discord Raidkit v2.2.0 by the-cult-of-integral
"The trojan horse of discord raiding"
Last updated: 16/06/2022
"""

import os
import random
import sqlite3

import discord
from discord.ext import commands

CON_LOG_PATH = r"logs\con_log.txt"


class Images(commands.Cog, name='Images module'):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.conn_string = "qetesh_db.db"
        if not os.path.isfile(CON_LOG_PATH):
            open(CON_LOG_PATH, "w").close()
        self.start()
        self.conn = sqlite3.connect(self.conn_string)
        self.c = self.conn.cursor()
        self.link = ""
        self.previous_link = ""
    
    def execute(self, *args) -> None:
        try:
            with sqlite3.connect(self.conn_string) as con:
                c = con.cursor()
                c.execute(*args)
                c.close()
        except Exception as e:
            with open(CON_LOG_PATH, "a") as f:
                f.writelines(f"execute() err: {e}\n")
    
    def create_links_table(self) -> None:
        try:
            self.execute("""CREATE TABLE links (
                category TEXT,
                link TEXT,
                UNIQUE(category, link))""")
        except Exception as e:
            with open(CON_LOG_PATH, "a") as f:
                f.writelines(f"execute() err: {e}\n")
    
    def insert_link(self, link, category) -> None:
        try:
            self.execute("INSERT OR IGNORE INTO links VALUES (?, ?)", (category, link))
        except Exception as e:
            with open(CON_LOG_PATH, "a") as f:
                f.writelines(f"execute() err: {e}\n")
    
    def start(self) -> None:
        try:
            if not os.path.isfile("qetesh_db.db"):
                self.create_links_table()
        except Exception as e:
            with open(CON_LOG_PATH, "a") as f:
                f.writelines(f"create_links_table() err: {e}")
        
        with open("cogs/qetesh/vagl/vagl_links.txt", "r") as file: 
            try:
                links = file.read().split("\n")
                [self.insert_link(link, "vagl") for link in links]
            except Exception as e:
                with open(CON_LOG_PATH, "a") as f:
                    f.writelines(f"insert_links() err: {e}")

        with open("cogs/qetesh/bj/bj_links.txt", "r") as file: 
            try:
                links = file.read().split("\n")
                [self.insert_link(link, "bj") for link in links]
            except Exception as e:
                with open(CON_LOG_PATH, "a") as f:
                    f.writelines(f"insert_links() err: {e}") 

        with open("cogs/qetesh/anal/anal_links.txt", "r") as file: 
            try:
                links = file.read().split("\n")
                [self.insert_link(link, "anal") for link in links]
            except Exception as e:
                with open(CON_LOG_PATH, "a") as f:
                    f.writelines(f"insert_links() err: {e}")

        with open("cogs/qetesh/lesbian/lesbian_links.txt", "r") as file: 
            try:
                links = file.read().split("\n")
                [self.insert_link(link, "lesbian") for link in links]
            except Exception as e:
                with open(CON_LOG_PATH, "a") as f:
                    f.writelines(f"insert_links() err: {e}")

        with open("cogs/qetesh/gay/gay_links.txt", "r") as file: 
            try:
                links = file.read().split("\n")
                [self.insert_link(link, "gay") for link in links]
            except Exception as e:
                with open(CON_LOG_PATH, "a") as f:
                    f.writelines(f"insert_links() err: {e}")

        with open("cogs/qetesh/tits/tits_links.txt", "r") as file: 
            try:
                links = file.read().split("\n")
                [self.insert_link(link, "tits") for link in links]
            except Exception as e:
                with open(CON_LOG_PATH, "a") as f:
                    f.writelines(f"insert_links() err: {e}")

        with open("cogs/qetesh/ass/ass_links.txt", "r") as file: 
            try:
                links = file.read().split("\n")
                [self.insert_link(link, "ass") for link in links]
            except Exception as e:
                with open(CON_LOG_PATH, "a") as f:
                    f.writelines(f"insert_links() err: {e}")

        with open("cogs/qetesh/pussy/pussy_links.txt", "r") as file: 
            try:
                links = file.read().split("\n")
                [self.insert_link(link, "pussy") for link in links]
            except Exception as e:
                with open(CON_LOG_PATH, "a") as f:
                    f.writelines(f"insert_links() err: {e}")

        with open("cogs/qetesh/cock/cock_links.txt", "r") as file: 
            try:
                links = file.read().split("\n")
                [self.insert_link(link, "cock") for link in links]
            except Exception as e:
                with open(CON_LOG_PATH, "a") as f:
                    f.writelines(f"insert_links() err: {e}")

        with open("cogs/qetesh/asian/asian_links.txt", "r") as file:
            try:
                links = file.read().split("\n")
                [self.insert_link(link, "asian") for link in links]
            except Exception as e:
                with open(CON_LOG_PATH, "a") as f:
                    f.writelines(f"insert_links() err: {e}")

        with open("cogs/qetesh/amateur/amateur_links.txt", "r") as file:
            try:
                links = file.read().split("\n")
                [self.insert_link(link, "amateur") for link in links]
            except Exception as e:
                with open(CON_LOG_PATH, "a") as f:
                    f.writelines(f"insert_links() err: {e}")

        with open("cogs/qetesh/hentai/hentai_links.txt", "r") as file:
            try:
                links = file.read().split("\n")
                [self.insert_link(link, "hentai") for link in links]
            except Exception as e:
                with open(CON_LOG_PATH, "a") as f:
                    f.writelines(f"insert_links() err: {e}")

        with open("cogs/qetesh/milf/milf_links.txt", "r") as file:
            try:
                links = file.read().split("\n")
                [self.insert_link(link, "milf") for link in links]
            except Exception as e:
                with open(CON_LOG_PATH, "a") as f:
                    f.writelines(f"insert_links() err: {e}")

        with open("cogs/qetesh/teen/teen_links.txt", "r") as file:
            try:
                links = file.read().split("\n")
                [self.insert_link(link, "teen") for link in links]
            except Exception as e:
                with open(CON_LOG_PATH, "a") as f:
                    f.writelines(f"insert_links() err: {e}")

        with open("cogs/qetesh/ebony/ebony_links.txt", "r") as file:
            try:
                links = file.read().split("\n")
                [self.insert_link(link, "ebony") for link in links]
            except Exception as e:
                with open(CON_LOG_PATH, "a") as f:
                    f.writelines(f"insert_links() err: {e}")

        with open("cogs/qetesh/threesome/threesome_links.txt", "r") as file:
            try:
                links = file.read().split("\n")
                [self.insert_link(link, "threesome") for link in links]
            except Exception as e:
                with open(CON_LOG_PATH, "a") as f:
                    f.writelines(f"insert_links() err: {e}")

        with open("cogs/qetesh/cartoon/cartoon_links.txt", "r") as file:
            try:
                links = file.read().split("\n")
                [self.insert_link(link, "cartoon") for link in links]
            except Exception as e:
                with open(CON_LOG_PATH, "a") as f:
                    f.writelines(f"insert_links() err: {e}")

        with open("cogs/qetesh/creampie/creampie_links.txt", "r") as file:
            try:
                links = file.read().split("\n")
                [self.insert_link(link, "creampie") for link in links]
            except Exception as e:
                with open(CON_LOG_PATH, "a") as f:
                    f.writelines(f"insert_links() err: {e}")

        with open("cogs/qetesh/bondage/bondage_links.txt", "r") as file:
            try:
                links = file.read().split("\n")
                [self.insert_link(link, "bondage") for link in links]
            except Exception as e:
                with open(CON_LOG_PATH, "a") as f:
                    f.writelines(f"insert_links() err: {e}")

        with open("cogs/qetesh/squirt/squirt_links.txt", "r") as file:
            try:
                links = file.read().split("\n")
                [self.insert_link(link, "squirt") for link in links]
            except Exception as e:
                with open(CON_LOG_PATH, "a") as f:
                    f.writelines(f"insert_links() err: {e}")

        with open("cogs/qetesh/yiff/yiff_links.txt", "r") as file:
            try:
                links = file.read().split("\n")
                [self.insert_link(link, "yiff") for link in links]
            except Exception as e:
                with open(CON_LOG_PATH, "a") as f:
                    f.writelines(f"insert_links() err: {e}")

        with open("cogs/qetesh/neko/neko_links.txt", "r") as file: 
            try:
                links = file.read().split("\n")
                [self.insert_link(link, "neko") for link in links]    
            except Exception as e:
                with open(CON_LOG_PATH, "a") as f:
                    f.writelines(f"insert_links() err: {e}")
    
    def get_link(self, cat) -> None:
        try:
            self.c.execute("SELECT * FROM links WHERE category = ?;", (cat,))
            self.link = random.choice(self.c.fetchall())[1]
        except Exception as e:
            with open(CON_LOG_PATH, "a") as f:
                f.writelines(f"insert_links() err: {e}")  
        try:        
            if self.link == self.previous_link:
                self.get_link(cat)
            else:
                self.previous_link = self.link
        except Exception as e:
            with open(CON_LOG_PATH, "a") as f:
                f.writelines(f"get_link() err: {e}\n")

    @commands.command(name="vagl")
    async def vagl(self, ctx) -> None:
        """Display an image of vaginal sex in the text channel.
        """
        if not ctx.message.channel.nsfw:
            embed = discord.Embed(
                title="Error",
                description="This is an NSFW channel only bot.",
                colour=discord.Colour.orange()
            )
            await ctx.message.channel.send(embed=embed)
            return
        try:
            self.get_link("vagl")
        except discord.errors.HTTPException as e:
            embed = discord.Embed(
                title="Error",
                description=f"HTTP Exception: {e}",
                colour=discord.Colour.orange()
            )
            return
        embed = discord.Embed()
        embed.set_image(url=self.link)
        await ctx.message.channel.send(embed=embed)

    @commands.command(name="bj")
    async def bj(self, ctx) -> None:
        """Display an image of bj sex in the text channel.
        """
        if not ctx.message.channel.nsfw:
            embed = discord.Embed(
                title="Error",
                description="This is an NSFW channel only bot.",
                colour=discord.Colour.orange()
            )
            await ctx.message.channel.send(embed=embed)
            return
        try:
            self.get_link("bj")
        except discord.errors.HTTPException as e:
            embed = discord.Embed(
                title="Error",
                description=f"HTTP Exception: {e}",
                colour=discord.Colour.orange()
            )
            return
        embed = discord.Embed()
        embed.set_image(url=self.link)
        await ctx.message.channel.send(embed=embed)
    
    @commands.command(name="anal")
    async def anal(self, ctx) -> None:
        """Display an image of anal sex in the text channel.
        """
        if not ctx.message.channel.nsfw:
            embed = discord.Embed(
                title="Error",
                description="This is an NSFW channel only bot.",
                colour=discord.Colour.orange()
            )
            await ctx.message.channel.send(embed=embed)
            return
        try:
            self.get_link("anal")
        except discord.errors.HTTPException as e:
            embed = discord.Embed(
                title="Error",
                description=f"HTTP Exception: {e}",
                colour=discord.Colour.orange()
            )
            return
        embed = discord.Embed()
        embed.set_image(url=self.link)
        await ctx.message.channel.send(embed=embed)

    @commands.command(name="les")
    async def les(self, ctx) -> None:
        """Display an image of lesbian sex in the text channel.
        """
        if not ctx.message.channel.nsfw:
            embed = discord.Embed(
                title="Error",
                description="This is an NSFW channel only bot.",
                colour=discord.Colour.orange()
            )
            await ctx.message.channel.send(embed=embed)
            return
        try:
            self.get_link("lesbian")
        except discord.errors.HTTPException as e:
            embed = discord.Embed(
                title="Error",
                description=f"HTTP Exception: {e}",
                colour=discord.Colour.orange()
            )
            return
        embed = discord.Embed()
        embed.set_image(url=self.link)
        await ctx.message.channel.send(embed=embed)

    @commands.command(name="gay")
    async def gay(self, ctx) -> None:
        """Display an image of gay sex in the text channel.
        """
        if not ctx.message.channel.nsfw:
            embed = discord.Embed(
                title="Error",
                description="This is an NSFW channel only bot.",
                colour=discord.Colour.orange()
            )
            await ctx.message.channel.send(embed=embed)
            return
        try:
            self.get_link("gay")
        except discord.errors.HTTPException as e:
            embed = discord.Embed(
                title="Error",
                description=f"HTTP Exception: {e}",
                colour=discord.Colour.orange()
            )
            return
        embed = discord.Embed()
        embed.set_image(url=self.link)
        await ctx.message.channel.send(embed=embed)
    
    @commands.command(name="tits")
    async def tits(self, ctx) -> None:
        """Display an image of tits in the text channel.
        """
        if not ctx.message.channel.nsfw:
            embed = discord.Embed(
                title="Error",
                description="This is an NSFW channel only bot.",
                colour=discord.Colour.orange()
            )
            await ctx.message.channel.send(embed=embed)
            return
        try:
            self.get_link("tits")
        except discord.errors.HTTPException as e:
            embed = discord.Embed(
                title="Error",
                description=f"HTTP Exception: {e}",
                colour=discord.Colour.orange()
            )
            return
        embed = discord.Embed()
        embed.set_image(url=self.link)
        await ctx.message.channel.send(embed=embed)
    
    @commands.command(name="ass")
    async def ass(self, ctx) -> None:
        """Display an image of ass in the text channel.
        """
        if not ctx.message.channel.nsfw:
            embed = discord.Embed(
                title="Error",
                description="This is an NSFW channel only bot.",
                colour=discord.Colour.orange()
            )
            await ctx.message.channel.send(embed=embed)
            return
        try:
            self.get_link("ass")
        except discord.errors.HTTPException as e:
            embed = discord.Embed(
                title="Error",
                description=f"HTTP Exception: {e}",
                colour=discord.Colour.orange()
            )
            return
        embed = discord.Embed()
        embed.set_image(url=self.link)
        await ctx.message.channel.send(embed=embed)
    
    @commands.command(name="pussy")
    async def pussy(self, ctx) -> None:
        """Display an image of pussy in the text channel.
        """
        if not ctx.message.channel.nsfw:
            embed = discord.Embed(
                title="Error",
                description="This is an NSFW channel only bot.",
                colour=discord.Colour.orange()
            )
            await ctx.message.channel.send(embed=embed)
            return
        try:
            self.get_link("pussy")
        except discord.errors.HTTPException as e:
            embed = discord.Embed(
                title="Error",
                description=f"HTTP Exception: {e}",
                colour=discord.Colour.orange()
            )
            return
        embed = discord.Embed()
        embed.set_image(url=self.link)
        await ctx.message.channel.send(embed=embed)
    
    @commands.command(name="cock")
    async def cock(self, ctx) -> None:
        """Display an image of cock in the text channel.
        """
        if not ctx.message.channel.nsfw:
            embed = discord.Embed(
                title="Error",
                description="This is an NSFW channel only bot.",
                colour=discord.Colour.orange()
            )
            await ctx.message.channel.send(embed=embed)
            return
        try:
            self.get_link("cock")
        except discord.errors.HTTPException as e:
            embed = discord.Embed(
                title="Error",
                description=f"HTTP Exception: {e}",
                colour=discord.Colour.orange()
            )
            return
        embed = discord.Embed()
        embed.set_image(url=self.link)
        await ctx.message.channel.send(embed=embed)

    @commands.command(name="asian")
    async def asian(self, ctx) -> None:
        """Display an image of a woman of asian ethnicity in the text channel.
        """
        if not ctx.message.channel.nsfw:
            embed = discord.Embed(
                title="Error",
                description="This is an NSFW channel only bot.",
                colour=discord.Colour.orange()
            )
            await ctx.message.channel.send(embed=embed)
            return
        try:
            self.get_link("asian")
        except discord.errors.HTTPException as e:
            embed = discord.Embed(
                title="Error",
                description=f"HTTP Exception: {e}",
                colour=discord.Colour.orange()
            )
            return
        embed = discord.Embed()
        embed.set_image(url=self.link)
        await ctx.message.channel.send(embed=embed)

    @commands.command(name="amateur")
    async def amateur(self, ctx) -> None:
        """Display an image of amateur porn in the text channel.
        """
        if not ctx.message.channel.nsfw:
            embed = discord.Embed(
                title="Error",
                description="This is an NSFW channel only bot.",
                colour=discord.Colour.orange()
            )
            await ctx.message.channel.send(embed=embed)
            return
        try:
            self.get_link("amateur")
        except discord.errors.HTTPException as e:
            embed = discord.Embed(
                title="Error",
                description=f"HTTP Exception: {e}",
                colour=discord.Colour.orange()
            )
            return
        embed = discord.Embed()
        embed.set_image(url=self.link)
        await ctx.message.channel.send(embed=embed)

    @commands.command(name="hentai")
    async def hentai(self, ctx) -> None:
        """Display an image of hentai in the text channel.
        """
        if not ctx.message.channel.nsfw:
            embed = discord.Embed(
                title="Error",
                description="This is an NSFW channel only bot.",
                colour=discord.Colour.orange()
            )
            await ctx.message.channel.send(embed=embed)
            return
        try:
            self.get_link("hentai")
        except discord.errors.HTTPException as e:
            embed = discord.Embed(
                title="Error",
                description=f"HTTP Exception: {e}",
                colour=discord.Colour.orange()
            )
            return
        embed = discord.Embed()
        embed.set_image(url=self.link)
        await ctx.message.channel.send(embed=embed)

    @commands.command(name="milf")
    async def milf(self, ctx) -> None:
        """Display an image of milf porn in the text channel._
        """
        if not ctx.message.channel.nsfw:
            embed = discord.Embed(
                title="Error",
                description="This is an NSFW channel only bot.",
                colour=discord.Colour.orange()
            )
            await ctx.message.channel.send(embed=embed)
            return
        try:
            self.get_link("milf")
        except discord.errors.HTTPException as e:
            embed = discord.Embed(
                title="Error",
                description=f"HTTP Exception: {e}",
                colour=discord.Colour.orange()
            )
            return
        embed = discord.Embed()
        embed.set_image(url=self.link)
        await ctx.message.channel.send(embed=embed)

    @commands.command(name="teen")
    async def teen(self, ctx) -> None:
        """Display an image of teen (age: 18-19) porn in the text channel.
        """
        if not ctx.message.channel.nsfw:
            embed = discord.Embed(
                title="Error",
                description="This is an NSFW channel only bot.",
                colour=discord.Colour.orange()
            )
            await ctx.message.channel.send(embed=embed)
            return
        try:
            self.get_link("teen")
        except discord.errors.HTTPException as e:
            embed = discord.Embed(
                title="Error",
                description=f"HTTP Exception: {e}",
                colour=discord.Colour.orange()
            )
            return
        embed = discord.Embed()
        embed.set_image(url=self.link)
        await ctx.message.channel.send(embed=embed)

    @commands.command(name="ebony")
    async def ebony(self, ctx) -> None:
        """Display an image of a woman of ebony ethnicity in the text channel.
        """
        if not ctx.message.channel.nsfw:
            embed = discord.Embed(
                title="Error",
                description="This is an NSFW channel only bot.",
                colour=discord.Colour.orange()
            )
            await ctx.message.channel.send(embed=embed)
            return
        try:
            self.get_link("ebony")
        except discord.errors.HTTPException as e:
            embed = discord.Embed(
                title="Error",
                description=f"HTTP Exception: {e}",
                colour=discord.Colour.orange()
            )
            return
        embed = discord.Embed()
        embed.set_image(url=self.link)
        await ctx.message.channel.send(embed=embed)

    @commands.command(name="threesome")
    async def threesome(self, ctx) -> None:
        """Display an image of a threesome in the text channel.
        """
        if not ctx.message.channel.nsfw:
            embed = discord.Embed(
                title="Error",
                description="This is an NSFW channel only bot.",
                colour=discord.Colour.orange()
            )
            await ctx.message.channel.send(embed=embed)
            return
        try:
            self.get_link("threesome")
        except discord.errors.HTTPException as e:
            embed = discord.Embed(
                title="Error",
                description=f"HTTP Exception: {e}",
                colour=discord.Colour.orange()
            )
            return
        embed = discord.Embed()
        embed.set_image(url=self.link)
        await ctx.message.channel.send(embed=embed)

    @commands.command(name="cartoon")
    async def cartoon(self, ctx) -> None:
        """Display an image of cartoon/sketched porn in the text channel.
        """
        if not ctx.message.channel.nsfw:
            embed = discord.Embed(
                title="Error",
                description="This is an NSFW channel only bot.",
                colour=discord.Colour.orange()
            )
            await ctx.message.channel.send(embed=embed)
            return
        try:
            self.get_link("cartoon")
        except discord.errors.HTTPException as e:
            embed = discord.Embed(
                title="Error",
                description=f"HTTP Exception: {e}",
                colour=discord.Colour.orange()
            )
            return
        embed = discord.Embed()
        embed.set_image(url=self.link)
        await ctx.message.channel.send(embed=embed)

    @commands.command(name="creampie")
    async def creampie(self, ctx) -> None:
        """Display an image of a creampie (the sexual kind) in the text channel.
        """
        if not ctx.message.channel.nsfw:
            embed = discord.Embed(
                title="Error",
                description="This is an NSFW channel only bot.",
                colour=discord.Colour.orange()
            )
            await ctx.message.channel.send(embed=embed)
            return
        try:
            self.get_link("creampie")
        except discord.errors.HTTPException as e:
            embed = discord.Embed(
                title="Error",
                description=f"HTTP Exception: {e}",
                colour=discord.Colour.orange()
            )
            return
        embed = discord.Embed()
        embed.set_image(url=self.link)
        await ctx.message.channel.send(embed=embed)

    @commands.command(name="bondage")
    async def bondage(self, ctx) -> None:
        """Display an image of bondage in the text channel.
        """
        if not ctx.message.channel.nsfw:
            embed = discord.Embed(
                title="Error",
                description="This is an NSFW channel only bot.",
                colour=discord.Colour.orange()
            )
            await ctx.message.channel.send(embed=embed)
            return
        try:
            self.get_link("bondage")
        except discord.errors.HTTPException as e:
            embed = discord.Embed(
                title="Error",
                description=f"HTTP Exception: {e}",
                colour=discord.Colour.orange()
            )
            return
        embed = discord.Embed()
        embed.set_image(url=self.link)
        await ctx.message.channel.send(embed=embed)

    @commands.command(name="squirt")
    async def squirt(self, ctx) -> None:
        """Display an image of a woman squirting in the text channel.
        """
        if not ctx.message.channel.nsfw:
            embed = discord.Embed(
                title="Error",
                description="This is an NSFW channel only bot.",
                colour=discord.Colour.orange()
            )
            await ctx.message.channel.send(embed=embed)
            return
        try:
            self.get_link("squirt")
        except discord.errors.HTTPException as e:
            embed = discord.Embed(
                title="Error",
                description=f"HTTP Exception: {e}",
                colour=discord.Colour.orange()
            )
            return
        embed = discord.Embed()
        embed.set_image(url=self.link)
        await ctx.message.channel.send(embed=embed)

    @commands.command(command="yiff")
    async def yiff(self, ctx) -> None:
        """Display an image of yiff in the text channel.
        """
        if not ctx.message.channel.nsfw:
            embed = discord.Embed(
                title="Error",
                description="This is an NSFW channel only bot.",
                colour=discord.Colour.orange()
            )
            await ctx.message.channel.send(embed=embed)
            return
        try:
            self.get_link("yiff")
        except discord.errors.HTTPException as e:
            embed = discord.Embed(
                title="Error",
                description=f"HTTP Exception: {e}",
                colour=discord.Colour.orange()
            )
            return
        embed = discord.Embed()
        embed.set_image(url=self.link)
        await ctx.message.channel.send(embed=embed)

    @commands.command(command="neko")
    async def neko(self, ctx) -> None:
        """Display an image of neko in the text channel.
        """
        if not ctx.message.channel.nsfw:
            embed = discord.Embed(
                title="Error",
                description="This is an NSFW channel only bot.",
                colour=discord.Colour.orange()
            )
            await ctx.message.channel.send(embed=embed)
            return
        try:
            self.get_link("neko")
        except discord.errors.HTTPException as e:
            embed = discord.Embed(
                title="Error",
                description=f"HTTP Exception: {e}",
                colour=discord.Colour.orange()
            )
            return
        embed = discord.Embed()
        embed.set_image(url=self.link)
        await ctx.message.channel.send(embed=embed)

