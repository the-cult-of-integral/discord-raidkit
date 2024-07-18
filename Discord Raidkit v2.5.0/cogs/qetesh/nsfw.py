"""
nsfw.py

This namespace contains the Qetesh NSFW command cog,
which provides commands to see NSFW images from various categories.
A part of the genuine commands included in the Qetesh raider for social engineering.
"""

import os
import pathlib
import sqlite3
import typing

import discord
import discord.app_commands as app_commands
import discord.ext.commands as commands

import shared.utils.utils_io as iou
import shared.utils.utils_log as lu
import shared.utils.utils_runtime as rntu

DB_PATH = pathlib.Path(os.path.join('databases', 'qetesh.db'))


def all_links_path() -> pathlib.Path:
    """Returns the path to all_links.txt

    Returns:
        pathlib.Path: the path to all_links.txt
    """
    if rntu.is_running_as_executable():
        return pathlib.Path(os.path.join('_internal', 'cogs', 'qetesh', 'all_links.txt'))
    else:
        return pathlib.Path(os.path.join('cogs', 'qetesh', 'all_links.txt'))


class Nsfw(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        
        if not DB_PATH.exists():
            iou.mkfile(DB_PATH, None)

        self.conn = sqlite3.connect(DB_PATH)
        self.c = self.conn.cursor()
        
        if self.__exec_select_one('''
                    SELECT count(*) FROM sqlite_master 
                    WHERE type="table" AND name="Servers";''')[0]:
            lu.sinfo('Tables in the Qetesh database already exist; database is presumed ready.')
            return
        
        lu.sinfo('The Servers table is missing and thus the database is presumed not ready. \
            Creating tables...')
        
        if not self.create_tables():
            lu.scritical('Failed to create tables for Qetesh')
            raise SystemExit
        
        lu.sinfo('Tables created successfully. Inserting links...')
        with open(all_links_path(), 'r') as all_links:
            links = [(url, cat) for url, cat in (line.strip().split(',') for line in all_links)]
            chunk_size = 1000
            for i in range(0, len(links), chunk_size):
                chunk = links[i : i + chunk_size]
                if not self.insert_links(chunk):
                    lu.scritical(f'Failed to insert links chunk into the database at index {i}')
                    raise SystemExit
        lu.sinfo('Links inserted successfully.')

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        """Inserts a guild into the Qetesh database when the bot joins a guild
        if it is not already in the database

        Args:
            guild (discord.Guild): the guild the bot joined
        """
        self.insert_guild_if_not_present(guild.id)
    
    @app_commands.command(
        name='toggle-only-nsfw',
        description='Toggle whether NSFW commands only work in NSFW channels.')
    @app_commands.describe(
        state='Whether to restrict NSFW commands to only NSFW channels.')
    @app_commands.choices(
        state=[
            app_commands.Choice(name='Yes', value=1),
            app_commands.Choice(name='No', value=0)
        ])
    async def toggle_only_nsfw(self, interaction: discord.Interaction, state: int):
        await interaction.response.defer(ephemeral=True)

        if not self.insert_guild_if_not_present(interaction.guild.id):
            return False

        if not (interaction.user.guild_permissions.manage_channels or interaction.user.guild_permissions.administrator):
            embed = discord.Embed(
                title='Set Only NSFW',
                description='You do not have permission to use this command.',
                color=discord.Color.brand_red())
            await interaction.followup.send(embed=embed)
            return False

        try:
            sql = 'UPDATE Nsfw SET onlyNsfwChannels = ? WHERE server_id = ?'
            if self.__exec_nonselect(sql, state, interaction.guild.id):
                embed = discord.Embed(
                    title='Set Only NSFW',
                    description=f'Set onlyNsfwChannels to {"true" if state else "false"}',
                    color=discord.Color.blue())
                await interaction.followup.send(embed=embed)
                return True

        except discord.errors.Forbidden:
            embed = discord.Embed(
                title='Set Only NSFW',
                description='I do not have permission to post embeds to channels.',
                color=discord.Color.brand_red())
            await interaction.followup.send(embed=embed)

        except Exception as e:
            lu.swarning(f'Error when attempting to set onlyNsfwChannels to {state} for guild {interaction.guild.name}: {e}')
            await interaction.followup.send(f'Error: {e}')
    
    @app_commands.command(
        name='toggle-cmd',
        description='Toggle whether a command is enabled on your server.')
    @app_commands.describe(
        command='The command in question.',
        state='Whether to allow the command in your server.')
    @app_commands.choices(
        command=[
            app_commands.Choice(name='amateur', value='amateur'),
            app_commands.Choice(name='anal', value='anal'),
            app_commands.Choice(name='asian', value='asian'),
            app_commands.Choice(name='ass', value='ass'),
            app_commands.Choice(name='bondage', value='bondage'),
            app_commands.Choice(name='bukkake', value='bukkake'),
            app_commands.Choice(name='cock', value='cock'),
            app_commands.Choice(name='cosplay', value='cosplay'),
            app_commands.Choice(name='creampie', value='creampie'),
            app_commands.Choice(name='dildo', value='dildo'),
            app_commands.Choice(name='double penetration', value='double'),
            app_commands.Choice(name='ebony', value='ebony'),
            app_commands.Choice(name='gay', value='gay'),
            app_commands.Choice(name='hentai', value='hentai'),
            app_commands.Choice(name='lesbian', value='lesbian'),
            app_commands.Choice(name='milf', value='milf'),
            app_commands.Choice(name='neko', value='neko'),
            app_commands.Choice(name='oral', value='oral'),
            app_commands.Choice(name='pussy', value='pussy'),
            app_commands.Choice(name='squirt', value='squirt'),
            app_commands.Choice(name='teen', value='teen'),
            app_commands.Choice(name='threesome', value='threesome'),
            app_commands.Choice(name='tits', value='tits'),
            app_commands.Choice(name='uniform', value='uniform'),
            app_commands.Choice(name='vaginal', value='vagl')
        ],
        state=[
            app_commands.Choice(name='Yes', value=1),
            app_commands.Choice(name='No', value=0)
        ])
    async def toggle_cmd(self, interaction: discord.Interaction, command: str, state: int):
        """Toggle whether a command is enabled in the server or not

        Args:
            interaction (discord.Interaction): the interaction object
            command (str): the command to toggle on or off
            state (int): whether the command should be on or off
        """
        await interaction.response.defer(ephemeral=True)

        if not self.insert_guild_if_not_present(interaction.guild.id):
            return

        if not interaction.user.guild_permissions.administrator:
            embed = discord.Embed(
                title='Toggle Command',
                description='You do not have permission to use this command.',
                color=discord.Color.brand_red())
            return await interaction.followup.send(embed=embed)

        try:
            sql = f'UPDATE Nsfw SET do{command.title()} = ? WHERE server_id = ?;'
            if self.__exec_nonselect(sql, state, interaction.guild.id):
                embed = discord.Embed(
                    title='Toggle Command',
                    description=f'Set do{command.title()} to {"true" if state else "false"}',
                    color=discord.Color.blue())
                await interaction.followup.send(embed=embed)

        except discord.errors.Forbidden:
            embed = discord.Embed(
                title='Toggle Command',
                description='I do not have permission to post embeds to channels.',
                color=discord.Color.brand_red())
            await interaction.followup.send(embed=embed)

        except Exception as e:
            lu.swarning(f'Error when attempting to set do{command.title()} to {state}: {e}')
            await interaction.followup.send(f'Error: {e}')

    @app_commands.command(
        name='see',
        description='See a random NSFW image, based on category.',
    )
    @app_commands.describe(
        category='The category of image you\'d like to see')
    @app_commands.choices(
        category=[
            app_commands.Choice(name='amateur', value='amateur'),
            app_commands.Choice(name='anal', value='anal'),
            app_commands.Choice(name='asian', value='asian'),
            app_commands.Choice(name='ass', value='ass'),
            app_commands.Choice(name='bondage', value='bondage'),
            app_commands.Choice(name='bukkake', value='bukkake'),
            app_commands.Choice(name='cock', value='cock'),
            app_commands.Choice(name='cosplay', value='cosplay'),
            app_commands.Choice(name='creampie', value='creampie'),
            app_commands.Choice(name='dildo', value='dildo'),
            app_commands.Choice(name='double penetration', value='double'),
            app_commands.Choice(name='ebony', value='ebony'),
            app_commands.Choice(name='gay', value='gay'),
            app_commands.Choice(name='hentai', value='hentai'),
            app_commands.Choice(name='lesbian', value='lesbian'),
            app_commands.Choice(name='milf', value='milf'),
            app_commands.Choice(name='neko', value='neko'),
            app_commands.Choice(name='oral', value='oral'),
            app_commands.Choice(name='pussy', value='pussy'),
            app_commands.Choice(name='squirt', value='squirt'),
            app_commands.Choice(name='teen', value='teen'),
            app_commands.Choice(name='threesome', value='threesome'),
            app_commands.Choice(name='tits', value='tits'),
            app_commands.Choice(name='uniform', value='uniform'),
            app_commands.Choice(name='vaginal', value='vagl')
        ])
    async def see(self, interaction: discord.Interaction, category: str):
        """See a random image from a category and set the link to this image to the
        new previous link for this category

        Args:
            interaction (discord.Interaction): the interaction object
            category (str): the category of an image to see
        """
        await interaction.response.defer(ephemeral=True)

        if not self.insert_guild_if_not_present(interaction.guild.id):
            return False

        if self.is_only_nsfw(interaction.guild.id) and not interaction.channel.is_nsfw():
            embed = discord.Embed(
                title='NSFW Only',
                description='This server has been set to only allow NSFW images in NSFW channels.',
                color=discord.Color.orange())
            await interaction.followup.send(embed=embed)
            return False

        if not self.is_category_enabled(category, interaction.guild.id):
            embed = discord.Embed(
                title=f'{category.title()} Command Disabled',
                description=f'This server has set the "{category.title()}" command to be disabled.',
                color=discord.Color.orange())
            await interaction.followup.send(embed=embed)
            return False

        try:
            sql = 'SELECT link_url FROM Links WHERE link_category = ? ORDER BY RANDOM() LIMIT 1;'
            data = self.__exec_select_one(sql, category)

            while data and self.is_prev_link(data[0], category, interaction.guild.id):
                data = self.__exec_select_one(sql, category)

            if not data:
                return
            
            link = data[0]
            
            embed = discord.Embed(
                title=f'{category.title()}',
                color=discord.Color.blue())
            embed.set_image(url=link)
            await interaction.followup.send(embed=embed)
            
            sql = f'UPDATE PreviousLinks SET prev{category.title()} = ? WHERE server_id = ?;'
            
            self.__exec_nonselect(sql, link, interaction.guild.id)

        except discord.errors.Forbidden:
            embed = discord.Embed(
                title='See',
                description='I do not have permission to post embeds to channels with images.',
                color=discord.Color.brand_red())
            await interaction.followup.send(embed=embed)

        except Exception as e:
            lu.swarning(f'Error when attempting to see {category} for guild {interaction.guild.name}: {e}')
            await interaction.followup.send(f'Error: {e}')

    def insert_guild_if_not_present(self, guild_id: int) -> bool:
        """Inserts a guild into the database if it is not already in the database

        Args:
            guild_id (int): the id of the guild to insert

        Returns:
            bool: whether the guild was inserted. True if already present.
        """
        if not self.is_guild_in_db(guild_id):
            return self.insert_guild(guild_id)
        return True
    
    def is_category_enabled(self, category: str, guild_id: int) -> bool:
        """Checks whether a category is enabled for a guild

        Args:
            category (str): the category to check
            guild_id (int): the id of the guild to check

        Returns:
            bool: whether the category is enabled for the guild
        """
        sql = f'SELECT do{category.title()} FROM Nsfw WHERE server_id = ?;'
        data = self.__exec_select_one(sql, guild_id)
        if not data:
            return False
        return bool(data[0])

    def is_only_nsfw(self, guild_id: int) -> bool:
        """Checks whether a server only allows NSFW commands in NSFW channels

        Args:
            guild_id (int): the id of the guild to check

        Returns:
            bool: whether the server only allows NSFW commands in NSFW channels
        """
        sql = 'SELECT onlyNsfwChannels FROM Nsfw WHERE server_id = ?;'
        data = self.__exec_select_one(sql, guild_id)
        if not data:
            return True
        return bool(data[0])
    
    def is_prev_link(self, link: str, category: str, guild_id: int) -> bool:
        """Checks whether a link is the same as the previous link for a category

        Args:
            link (str): te link to check
            category (str): the category to check
            guild_id (int): the id of the guild to check

        Returns:
            bool: whether the link is the same as the previous link for the category
        """
        sql = f'SELECT prev{category.title()} FROM PreviousLinks WHERE server_id = ?;'
        data = self.__exec_select_one(sql, guild_id)
        if not data:
            return False
        return link == data[0]
    
    def is_guild_in_db(self, guild_id: int) -> bool:
        """Checks whether a guild is in the Qetesh database

        Args:
            guild_id (int): the id of the guild to check

        Returns:
            bool: whether the guild is in the Qetesh database
        """
        sql = 'SELECT count(*) FROM Servers WHERE server_id = ?;'
        data = self.__exec_select_one(sql, guild_id)
        if not data:
            return False
        return bool(data[0])
    
    def create_tables(self) -> bool:
        """Create tables for Qetesh if they do not exist

        Returns:
            bool: whether the non-select query executed without errors
        """
        sql = '''CREATE TABLE IF NOT EXISTS Servers(
            server_id UNSIGNED BIG INT NOT NULL PRIMARY KEY
        );'''
        if not self.__exec_nonselect(sql):
            return False
        
        sql = '''CREATE TABLE IF NOT EXISTS Nsfw(
            server_id UNSIGNED BIG INT NOT NULL PRIMARY KEY,
            doAmateur BOOLEAN NOT NULL DEFAULT 1,
            doAnal BOOLEAN NOT NULL DEFAULT 1,
            doAsian BOOLEAN NOT NULL DEFAULT 1,
            doAss BOOLEAN NOT NULL DEFAULT 1,
            doBondage BOOLEAN NOT NULL DEFAULT 1,
            doBukkake BOOLEAN NOT NULL DEFAULT 1,
            doCock BOOLEAN NOT NULL DEFAULT 1,
            doCosplay BOOLEAN NOT NULL DEFAULT 1,
            doCreampie BOOLEAN NOT NULL DEFAULT 1,
            doDildo BOOLEAN NOT NULL DEFAULT 1,
            doDouble BOOLEAN NOT NULL DEFAULT 1,
            doEbony BOOLEAN NOT NULL DEFAULT 1,
            doGay BOOLEAN NOT NULL DEFAULT 1,
            doHentai BOOLEAN NOT NULL DEFAULT 1,
            doLesbian BOOLEAN NOT NULL DEFAULT 1,
            doMilf BOOLEAN NOT NULL DEFAULT 1,
            doNeko BOOLEAN NOT NULL DEFAULT 1,
            doOral BOOLEAN NOT NULL DEFAULT 1,
            doPussy BOOLEAN NOT NULL DEFAULT 1,
            doSquirt BOOLEAN NOT NULL DEFAULT 1,
            doTeen BOOLEAN NOT NULL DEFAULT 1,
            doThreesome BOOLEAN NOT NULL DEFAULT 1,
            doTits BOOLEAN NOT NULL DEFAULT 1,
            doUniform BOOLEAN NOT NULL DEFAULT 1,
            doVagl BOOLEAN NOT NULL DEFAULT 1,
            onlyNsfwChannels BOOLEAN NOT NULL DEFAULT 1,
            FOREIGN KEY(server_id) 
                REFERENCES Servers(server_id)
        );'''
        if not self.__exec_nonselect(sql):
            return False
        
        sql = '''CREATE TABLE IF NOT EXISTS Links(
            link_id INTEGER NOT NULL PRIMARY KEY,
            link_url TEXT NOT NULL,
            link_category TEXT NOT NULL
        );'''
        if not self.__exec_nonselect(sql):
            return False
        
        sql = '''CREATE TABLE IF NOT EXISTS PreviousLinks(
            server_id UNSIGNED BIG INT NOT NULL PRIMARY KEY,
            prevAmateur TEXT NOT NULL DEFAULT '',
            prevAnal TEXT NOT NULL DEFAULT '',
            prevAsian TEXT NOT NULL DEFAULT '',
            prevAss TEXT NOT NULL DEFAULT '',
            prevBondage TEXT NOT NULL DEFAULT '',
            prevBukkake TEXT NOT NULL DEFAULT '',
            prevCock TEXT NOT NULL DEFAULT '',
            prevCosplay TEXT NOT NULL DEFAULT '',
            prevCreampie TEXT NOT NULL DEFAULT '',
            prevDildo TEXT NOT NULL DEFAULT '',
            prevDouble TEXT NOT NULL DEFAULT '',
            prevEbony TEXT NOT NULL DEFAULT '',
            prevGay TEXT NOT NULL DEFAULT '',
            prevHentai TEXT NOT NULL DEFAULT '',
            prevLesbian TEXT NOT NULL DEFAULT '',
            prevMilf TEXT NOT NULL DEFAULT '',
            prevNeko TEXT NOT NULL DEFAULT '',
            prevOral TEXT NOT NULL DEFAULT '',
            prevPussy TEXT NOT NULL DEFAULT '',
            prevSquirt TEXT NOT NULL DEFAULT '',
            prevTeen TEXT NOT NULL DEFAULT '',
            prevThreesome TEXT NOT NULL DEFAULT '',
            prevTits TEXT NOT NULL DEFAULT '',
            prevUniform TEXT NOT NULL DEFAULT '',
            prevVagl TEXT NOT NULL DEFAULT '',
            FOREIGN KEY(server_id)
                REFERENCES Servers(server_id)
        );'''
        if not self.__exec_nonselect(sql):
            return False
        
        return True
    
    def insert_guild(self, guild_id: int) -> bool:
        """Insert a guild into the database

        Args:
            guild_id (int): the id of the guild to insert

        Returns:
            bool: whether the non-select query executed without errors
        """
        sql = 'INSERT INTO Servers(server_id) VALUES (?);'
        if not self.__exec_nonselect(sql, guild_id):
            return False
        
        sql = 'INSERT INTO Nsfw(server_id) VALUES (?);'
        if not self.__exec_nonselect(sql, guild_id):
            return False

        sql = 'INSERT INTO PreviousLinks(server_id) VALUES (?);'
        if not self.__exec_nonselect(sql, guild_id):
            return False

        return True
    
    def insert_links(self, links: typing.List[typing.Tuple[str, str]]) -> bool:
        """Insert links into the database from all_links.txt

        Args:
            links (typing.List[typing.Tuple[str, str]]): the link,cat pairs to insert

        Returns:
            bool: whether the non-select query executed without errors
        """
        sql = 'INSERT INTO Links (link_url, link_category) VALUES (?, ?);'
        try:
            self.c.executemany(sql, links)
            self.conn.commit()
        except Exception as e:
            lu.serror(f'Failed to insert links into the database due to error: {e}')
            return False
        return True
    
    def __exec_select_one(self, query: str, *args: typing.Tuple[typing.Any, ...]) -> typing.Any:
        """Returns the first row of a query

        Args:
            query (str): the query to execute

        Returns:
            typing.Any: the first row of the query
        """
        try:
            self.c.execute(query, args)
            return self.c.fetchone()  
        except Exception as e:
            lu.serror(f'Failed to execute query: {query} with args: {args} due to error: {e}')
            return None
    
    def __exec_nonselect(self, query: str, *args: typing.Tuple[typing.Any, ...]) -> bool:
        """Returns the success of a non-select query

        Args:
            query (str): the query to execute

        Returns:
            bool: the success of the query
        """
        try:
            self.c.execute(query, args)
            self.conn.commit()
            return True
        except Exception as e:
            lu.serror(f'Failed to execute query: {query} with args: {args} due to error: {e}')
            return False
        

async def setup(bot):
    await bot.add_cog(Nsfw(bot))
