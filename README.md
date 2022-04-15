# Discord Raidkit
A collection of tools designed for raiding discord servers and accounts. The project has two main goals: to make these tools freely available and useable to anyone, regardless of technical prowess, and to make these tools as unassuming and trojan-like as possible.

---

### Features
- A malicious bot designed to appear like a helpful moderation and anti-raiding bot.
- A malicious bot designed to appear like an NSFW bot, complete with 1323 links to images.
- Eight commands to manipulate servers, including an admin, nuke, and raid command.
- A malicious tool designed to use an account's Auth Token to your advantage.
- An information command that can display an accounts email, phone number, and 2FA status.
- An account nuke command that can send a settings patch to mess with an account, such as changing the account language to japaneese, or the theme to light mode.
- A login command that can allow you to log into an account easily, using a Selenium webdriver.
- Completely, 100% open-source and free.

---

### Installation
***Warning:** if cloning this repository, as opposed to using the releases page, there will be some files missing, as some files are big enough to immediately ruin the cloning limit placed on free GitHub accounts and are thus only included in the release file, not any branches. If you are cloning this repository, be sure to [download the browser folder here](https://drive.google.com/file/d/1gfym1W--XqBaZKHv5Bs0adK-aV5ekHLE/view?usp=sharing) and place the folder within the Discord Raidkit folder; this folder is not used for Anubis or Qetesh, but is essential for Osiris.*

The installation of Discord Raidkit v2.0.0+ is easy compared to previous versions.
1. Head over to the [releases page](https://github.com/the-cult-of-integral/discord-raidkit/releases/latest) and download the 7-zip file for the release you want to install.

2. Extract the 7-zip file and enter the Discord Raidkit folder.


3. Run the `install_requirements.bat` file to install the required dependencies. If you cannot run batch files, for any reason, run the following command in whichever console you use:
  `pip install bs4 colorama discord dhooks PyQt6 qasync requests selenium`

4. Finally, run the `Discord Raidkit.pyw` file. There may be a slight delay between running the file and you seeing the program.

It should be mentioned that this project is built with, and thus requires, Python. To install Python, go the [python page](https://python.org) then download and install the latest version of Python. 

**When installing Python, you must check the "Add to PATH" checkbox!**

---

### Usage
After running the program, you may see a pop-up notifying you of a new update. If accpeted, this pop-up will take you to the latest release of this program which you can then download and run.

The Discord Raidkit GUI has four main screens: the bot configuration screen, the Anubis screen, the Qetesh screen, and the Osiris screen.

![Discord Raidkit v2 0 0 Screen](https://user-images.githubusercontent.com/98130822/163580370-8d389e60-d225-4aa1-be39-fa411121a80c.png)

##### Bot Configuration
The Bot Configuration screen allows users to set a bot token and prefix to be used when running Anubis or Qetesh. It is imporant to note that these settings are saved upon clicking the "Configure Bots" button; just entering values into the text inputs will not save the changes.

There are also two other buttons on the Bot Configuration screen. The "View GitHub" button will take you to the main page of the Discord Raidkit repository, the same page you are more than likely reading this on. The "Clear Logs" button will clear any error logging files, and is especially useful when the errors.log file becomes filled with qasync errors, which can occasionally happen (these errors do not cause any visual effect to the program, they are just caught by the logger regardless).

##### Anubis & Qetesh
The Anubis and Qetesh screens start their own respective tools. It should be mentioned that, after clicking the start Anubis and Qetesh buttons, other buttons will immediately become enabled. However, you may notice that if you click them, nothing happens: this means that the bot is still starting behind the screens; the buttons will work once the bot is fully started. Furthermore, if starting Qetesh for the first time, the screen may become unresponsive for a short period of time: this is the Qetesh bot creating the `qetesh_db.db` file and inserting every link into the database — the process will finish after a few seconds.

After starting Anubis or Qetesh, the only screens the user may see is the screen of the bot they started, and the Osiris screen. The Bot Configuration screen, and the other bot screen, will not be viewable until the bot started has been ended. Ending a bot can be done with the end button which is next to the start button.

As a final note, when running the spam and raid commands, you may notice that the button to end the bot, not just the commands, is enabled as spamming starts. This is not done by the other commands. The reason for this little quirk is that any commands that involve spamming risk spamming indefinitely, including past the usage of the "Abort Cmds" button. This is rarely caused by an issue highlighted at the bottom of this README.md file. However, should such an issue occur, these buttons are enabled so that the bot can be ended, which will allow you to close the application as normal (if this quirk was not implemented, users would have to mess around in task manager to close the program, which completely goes against this project's first goal of making these tools freely available and useable to anyone, regardless of their technical prowess). I just thouoght I'd mention this quirk here before anyone gets confused as to why two out of eight commands randomly enable an unrelated button when the rest of the commands do not.

---

##### Osiris
The Osiris screen has three buttons, where each button will prompt the user to enter an Auth Token — this Auth Token is a user token, not a bot token. The "Find Info" button will display information regarding the account to the five, read-only text boxes at the bottom of the screen (these text boxes are also used to inform the user that an invalid auth token has been passed). The "Nuke Account" button will nuke an account, which involves creating a number of servers and patching the account settings of the targeted account, which will, among other things, change the account language to japaneese, the theme to light mode, and disable embeds. The nuking may also involve making the member leave any server they do not own, depending on the contents of the request feedback received when making a GET request to the target account. Finally, the "Log Into Account" button will allow the user to log into and have full access to the target account, in a chrome browser window: the login script is executed by Selenium's webdriver.

---

### Known Issues

- **Inconsistency:** for Anubis and Qetesh, sometimes commands will work perfectly fine, other times the entire thing will break. I'm going to assume that this is an issue with discord's API, as I see no other reason why the exact same code would perform well sometimes, and poorly othertimes. Unfortunately, I do not have the power to change discord's API. It may also be an issue caused by trying to control discord bots, which are asynchronous, within a PyQt6 GUI application, which runs its own event loop. This is counteracted by the use of qasync's asyncSlot decorator, but it might not be perfect; I suspect this as only Anubis and Qetesh are afflicted with this issue, whereas Osiris is fine. Then again, Osiris works using the requests module, where as Anubis and Qetesh work using the discord.py module, so perhaps that is the issue. In any case, this issue can usually be resolved just by closing and rerunning the application.

---

### Milestones

- 10 stars. ✅
- 50 stars. ✅
- 69 stars. ✅
- 100 stars. ✅
- 250 stars. ❌
- 420 stars. ❌
- 1000 stars. ❌

A huge thank you to everyone who has been willing to support the metrics of this repository! ❤️