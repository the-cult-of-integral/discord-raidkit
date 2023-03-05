"""
Discord Raidkit v2.3.4 — "The trojan horse of discord raiding"
Copyright © 2023 the-cult-of-integral

a collection of raiding tools, hacking tools, and a token grabber generator for discord; written in Python 3

This program is under the GNU General Public License v2.0.
https://github.com/the-cult-of-integral/discord-raidkit/blob/master/LICENSE

nsfw.py stores the NSFW commands for Qetesh.
nsfw.py was last updated on 05/03/23 at 20:50 UTC.
"""

import logging
import os
import sqlite3

import discord
from discord import app_commands
from discord.app_commands import Choice
from discord.ext import commands

from utils import init_logger, mkfile

init_logger()

DB_PATH = os.path.join('databases', 'qetesh.db')


class Nsfw(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

        if not os.path.exists(DB_PATH):
            logging.info(f'{DB_PATH} does not exist. Creating...')
            mkfile(DB_PATH)

        self.conn = sqlite3.connect(DB_PATH)
        self.c = self.conn.cursor()

        self.__exec_select(
            '''SELECT count(*) FROM sqlite_master WHERE type='table' AND name='Servers';''')

        if not self.c.fetchone()[0]:
            logging.info(
                'One or more tables do not exist. Creating tables...')
            if not self.__create_tables():
                logging.error('Failed to create tables.')
                return
            logging.info('Tables created.')

            logging.info('Inserting links...')
            print(
                '\nInserting NSFW links into the database; this may take a few minutes. . .')
            with open(os.path.join('cogs', 'qetesh', 'all_links.txt'), 'r') as f:
                for line in f:
                    url, cat = line.strip().split(',')
                    if not self.__insert_links(url, cat):
                        logging.error(
                            f'Failed to insert link|cat {url} | {cat}')
                        return
            logging.info('Inserted links.')

        else:
            logging.info('Tables already exist; database presumed ready.')

        return

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild) -> bool:
        if not self.__check_guild(guild.id):
            sql = 'INSERT INTO Servers(server_id) VALUES(?)'
            if not self.__exec_nonselect(sql, guild.id):
                logging.error(
                    'Error in nsfw.py - on_guild_join(): failed to insert server')
                return False
        return True

    @app_commands.command(
        name='toggle-cmd',
        description='Toggle whether a command is enabled on your server.')
    @app_commands.describe(
        command='The command in question.',
        state='Whether to allow the command in your server.')
    @app_commands.choices(
        command=[
            Choice(name='amateur', value='amateur'),
            Choice(name='anal', value='anal'),
            Choice(name='asian', value='asian'),
            Choice(name='ass', value='ass'),
            Choice(name='bondage', value='bondage'),
            Choice(name='bukkake', value='bukkake'),
            Choice(name='cock', value='cock'),
            Choice(name='cosplay', value='cosplay'),
            Choice(name='creampie', value='creampie'),
            Choice(name='dildo', value='dildo'),
            Choice(name='double penetration', value='double'),
            Choice(name='ebony', value='ebony'),
            Choice(name='gay', value='gay'),
            Choice(name='hentai', value='hentai'),
            Choice(name='lesbian', value='lesbian'),
            Choice(name='milf', value='milf'),
            Choice(name='neko', value='neko'),
            Choice(name='oral', value='oral'),
            Choice(name='pussy', value='pussy'),
            Choice(name='squirt', value='squirt'),
            Choice(name='teen', value='teen'),
            Choice(name='threesome', value='threesome'),
            Choice(name='tits', value='tits'),
            Choice(name='uniform', value='uniform'),
            Choice(name='vaginal', value='vagl')
        ],
        state=[
            Choice(name='Yes', value=1),
            Choice(name='No', value=0)
        ])
    async def toggle_cmd(self, interaction: discord.Interaction, command: str, state: int) -> bool:
        await interaction.response.defer(ephemeral=True)
        try:

            if not self.__check_guild(interaction.guild.id):
                sql = 'INSERT INTO Servers(server_id) VALUES(?)'
                if not self.__exec_nonselect(sql, interaction.guild.id):
                    logging.error(
                        'Error in nsfw.py - on_guild_join(): failed to insert server')
                    return False
                sql = 'INSERT INTO Nsfw(server_id) VALUES(?)'
                if not self.__exec_nonselect(sql, interaction.guild.id):
                    logging.error(
                        'Error in nsfw.py - on_guild_join(): failed to insert server')
                    return False
                sql = 'INSERT INTO PreviousLinks(server_id) VALUES(?)'
                if not self.__exec_nonselect(sql, interaction.guild.id):
                    logging.error(
                        'Error in nsfw.py - on_guild_join(): failed to insert server')
                    return False

            if interaction.user.guild_permissions.administrator:
                sql = f'UPDATE Nsfw SET do{command.title()} = (?) WHERE server_id = (?);'
                if self.__exec_nonselect(sql, state, interaction.guild.id):
                    embed = discord.Embed(
                        title='Toggle Command',
                        description=f'Set do{command.title()} to {"true" if state else "false"}',
                        color=discord.Color.blue())
                    await interaction.followup.send(embed=embed)
                else:
                    return False

            else:
                embed = discord.Embed(
                    title='Toggle Command',
                    description='You do not have permission to use this command.',
                    color=discord.Color.brand_red())
                await interaction.followup.send(embed=embed)

        except discord.errors.Forbidden:
            embed = discord.Embed(
                title='Toggle Command',
                description='I do not have permission to post embeds to channels.',
                color=discord.Color.brand_red())
            await interaction.followup.send(embed=embed)

        except Exception as e:
            logging.error(
                f'Error in nsfw.py - set_only_nsfw(): {e}')
            await interaction.followup.send(f'Error: {e}')

        return True

    @app_commands.command(
        name='toggle-only-nsfw',
        description='Toggle whether NSFW commands only work in NSFW channels.')
    @app_commands.describe(
        state='Whether to restrict NSFW commands to only NSFW channels.')
    @app_commands.choices(
        state=[
            Choice(name='Yes', value=1),
            Choice(name='No', value=0)
        ])
    async def toggle_only_nsfw(self, interaction: discord.Interaction, state: int) -> bool:
        await interaction.response.defer(ephemeral=True)
        try:

            if not self.__check_guild(interaction.guild.id):
                sql = 'INSERT INTO Servers(server_id) VALUES(?)'
                if not self.__exec_nonselect(sql, interaction.guild.id):
                    logging.error(
                        'Error in nsfw.py - on_guild_join(): failed to insert server')
                    return False
                sql = 'INSERT INTO Nsfw(server_id) VALUES(?)'
                if not self.__exec_nonselect(sql, interaction.guild.id):
                    logging.error(
                        'Error in nsfw.py - on_guild_join(): failed to insert server')
                    return False
                sql = 'INSERT INTO PreviousLinks(server_id) VALUES(?)'
                if not self.__exec_nonselect(sql, interaction.guild.id):
                    logging.error(
                        'Error in nsfw.py - on_guild_join(): failed to insert server')
                    return False

            if interaction.user.guild_permissions.manage_channels or interaction.user.guild_permissions.administrator:
                sql = 'UPDATE Nsfw SET onlyNsfwChannels = ? WHERE server_id = ?'
                if self.__exec_nonselect(sql, state, interaction.guild.id):
                    embed = discord.Embed(
                        title='Set Only NSFW',
                        description=f'Set onlyNsfwChannels to {"true" if state else "false"}',
                        color=discord.Color.blue())
                    await interaction.followup.send(embed=embed)
                else:
                    return False
            else:
                embed = discord.Embed(
                    title='Set Only NSFW',
                    description='You do not have permission to use this command.',
                    color=discord.Color.brand_red())
                await interaction.followup.send(embed=embed)

        except discord.errors.Forbidden:
            embed = discord.Embed(
                title='Set Only NSFW',
                description='I do not have permission to post embeds to channels.',
                color=discord.Color.brand_red())
            await interaction.followup.send(embed=embed)

        except Exception as e:
            logging.error(
                f'Error in nsfw.py - set_only_nsfw(): {e}')
            await interaction.followup.send(f'Error: {e}')

        return True

    @app_commands.command(
        name='see',
        description='See a random NSFW image, based on category.',
    )
    @app_commands.describe(
        category='The category of image you\'d like to see')
    @app_commands.choices(
        category=[
            Choice(name='amateur', value='amateur'),
            Choice(name='anal', value='anal'),
            Choice(name='asian', value='asian'),
            Choice(name='ass', value='ass'),
            Choice(name='bondage', value='bondage'),
            Choice(name='bukkake', value='bukkake'),
            Choice(name='cock', value='cock'),
            Choice(name='cosplay', value='cosplay'),
            Choice(name='creampie', value='creampie'),
            Choice(name='dildo', value='dildo'),
            Choice(name='double penetration', value='double'),
            Choice(name='ebony', value='ebony'),
            Choice(name='gay', value='gay'),
            Choice(name='hentai', value='hentai'),
            Choice(name='lesbian', value='lesbian'),
            Choice(name='milf', value='milf'),
            Choice(name='neko', value='neko'),
            Choice(name='oral', value='oral'),
            Choice(name='pussy', value='pussy'),
            Choice(name='squirt', value='squirt'),
            Choice(name='teen', value='teen'),
            Choice(name='threesome', value='threesome'),
            Choice(name='tits', value='tits'),
            Choice(name='uniform', value='uniform'),
            Choice(name='vaginal', value='vagl')
        ])
    async def see(self, interaction: discord.Interaction, category: str) -> bool:
        await interaction.response.defer(ephemeral=True)
        try:
            if not self.__check_guild(interaction.guild.id):
                sql = 'INSERT INTO Servers(server_id) VALUES(?)'
                if not self.__exec_nonselect(sql, interaction.guild.id):
                    logging.error(
                        'Error in nsfw.py - on_guild_join(): failed to insert server')
                    return False
                sql = 'INSERT INTO Nsfw(server_id) VALUES(?)'
                if not self.__exec_nonselect(sql, interaction.guild.id):
                    logging.error(
                        'Error in nsfw.py - on_guild_join(): failed to insert server')
                    return False
                sql = 'INSERT INTO PreviousLinks(server_id) VALUES(?)'
                if not self.__exec_nonselect(sql, interaction.guild.id):
                    logging.error(
                        'Error in nsfw.py - on_guild_join(): failed to insert server')
                    return False

            if self.__only_nsfw(interaction.guild.id) and not interaction.channel.is_nsfw():
                embed = discord.Embed(
                    title='NSFW Only',
                    description='This server has been set to only allow NSFW images in NSFW channels.',
                    color=discord.Color.orange())
                await interaction.followup.send(embed=embed)
                return True

            if not self.__do_cmd(category, interaction.guild.id):
                embed = discord.Embed(
                    title=f'{category.title()} Command Disabled',
                    description=f'This server has set the "{category.title()}" command to be disabled.',
                    color=discord.Color.orange())
                await interaction.followup.send(embed=embed)
                return True

            sql = 'SELECT link_url FROM Links WHERE link_category = ? ORDER BY RANDOM() LIMIT 1;'

            if self.__exec_select(sql, category):
                link = self.c.fetchone()[0]

                while not self.__check_link(link, category, interaction.guild.id):
                    sql = 'SELECT link_url FROM Links WHERE link_category = (?) ORDER BY RANDOM() LIMIT 1;'
                    if self.__exec_select(sql, category):
                        link = self.c.fetchone()[0]
                    else:
                        return False

                embed = discord.Embed(
                    title=f'{category.title()}',
                    color=discord.Color.blue())
                embed.set_image(url=link)

                sql = f'UPDATE PreviousLinks SET prev{category.title()} = (?) WHERE server_id = (?);'

                if not self.__exec_nonselect(sql, link, interaction.guild.id):
                    return False

                await interaction.followup.send(embed=embed)
            else:
                return False

        except discord.errors.Forbidden:
            embed = discord.Embed(
                title='See',
                description='I do not have permission to post embeds to channels with images.',
                color=discord.Color.brand_red())
            await interaction.followup.send(embed=embed)

        except Exception as e:
            logging.error(
                f'Error in nsfw.py - see(): {e}')
            await interaction.followup.send(f'Error: {e}')

        return True

    def __do_cmd(self, command: str, guild_id: int) -> bool:
        sql = f'SELECT do{command.title()} FROM Nsfw WHERE server_id = (?);'
        if not self.__exec_select(sql, guild_id):
            return True
        return bool(self.c.fetchone()[0])

    def __only_nsfw(self, guild_id: int) -> bool:
        sql = 'SELECT onlyNsfwChannels FROM Servers WHERE server_id = (?);'
        if not self.__exec_select(sql, guild_id):
            return True
        return bool(self.c.fetchone()[0])

    def __check_link(self, link: str, category: str, guild_id: int) -> bool:
        sql = f'SELECT prev{category.title()} FROM PreviousLinks WHERE server_id = (?);'
        self.__exec_select(sql, guild_id)
        prev_link = self.c.fetchone()[0]
        return not (link == prev_link)

    def __check_guild(self, guild_id: int) -> bool:
        sql = 'SELECT count(*) FROM Servers WHERE server_id=?'
        if not self.__exec_select(sql, guild_id):
            return False
        return bool(self.c.fetchone()[0])

    def __create_tables(self) -> bool:
        sql = '''CREATE TABLE IF NOT EXISTS Servers(
            server_id UNSIGNED BIG INT NOT NULL PRIMARY KEY
        );'''
        if not self.__exec_nonselect(sql):
            logging.error(
                'Error in nsfw.py - create_tables(): failed to create Servers table')
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
            logging.error(
                'Error in nsfw.py - create_tables(): failed to create Nsfw table')
            return False

        sql = '''CREATE TABLE IF NOT EXISTS Links(
            link_id INTEGER NOT NULL PRIMARY KEY,
            link_url TEXT NOT NULL,
            link_category TEXT NOT NULL
        );'''
        if not self.__exec_nonselect(sql):
            logging.error(
                'Error in nsfw.py - create_tables(): failed to create Links table')
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
            logging.error(
                'Error in nsfw.py - create_tables(): failed to create PreviousLinks table')
            return False

        return True

    def __insert_links(self, link: str, cat: str) -> bool:
        sql = 'INSERT INTO Links(link_url, link_category) VALUES(?, ?)'
        if not self.__exec_nonselect(sql, link, cat):
            logging.error(
                'Error in nsfw.py - insert_links(): failed to insert links')
            return False
        return True

    def __exec_select(self, query: str, *args) -> bool:
        try:
            self.c.execute(query, args)
            return True
        except Exception as e:
            logging.error(
                f'Error in nsfw.py - __exec_select(): {e}')
            return False

    def __exec_nonselect(self, query: str, *args) -> bool:
        try:
            self.c.execute(query, args)
            self.conn.commit()
            return True
        except Exception as e:
            logging.error(
                f'Error in nsfw.py - __exec_nonselect(): {e}')
            return False


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Nsfw(bot))
