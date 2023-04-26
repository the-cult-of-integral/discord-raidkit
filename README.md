# Discord Raidkit

![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)
![forthebadge](http://forthebadge.com/images/badges/built-with-love.svg)

![GitHub contributors](https://img.shields.io/github/contributors/the-cult-of-integral/discord-raidkit)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=shields)](http://makeapullrequest.com)
![GitHub issues](https://img.shields.io/github/issues/the-cult-of-integral/discord-raidkit)
![GitHub pull requests](https://img.shields.io/github/issues-pr/9P9/Discord-QR-Token-Logger)
![Maintenance](https://img.shields.io/maintenance/yes/2023)
![GitHub commit activity](https://img.shields.io/github/commit-activity/m/the-cult-of-integral/discord-raidkit)

Discord Raidkit is an open-source, forever free tool that allows you to raid and destroy Discord servers via Discord bots, compromise Discord accounts, and generate Discord token grabbers.

![Discord Raidkit v2.4.0 Image](https://user-images.githubusercontent.com/98130822/234115079-195cbee2-2acf-4b86-9151-b715babad9e8.png)

## Why use Discord Raidkit over any other tool? Here's 5 reasons!

- **Developed for social engineering** - both bots have non-malicious slash commands, such as a moderation and NSFW suite (10000+ images!).

- **Asynchronous optimisation** - many tools work synchronously, one request at a time — we don't do things like that here.

- **Ease of use** - you can download this toolkit as a single executable, so there's no need to install Python or mess around with npm.

- **Maintained** - the first commit to this repository was made August 3rd, 2020, nearly three years ago. We evolve with discord.py, and Python. 

- **Professionally written** - this tool is written by a real software developer, and it's quite easy to tell!

## Installation

1. Head over to [the latest release](https://github.com/the-cult-of-integral/discord-raidkit/releases/latest).
2. Download the EXE zip.
3. Extract and run the executable in its directory.

---

## Tools summary

- **Anubis** is a Discord bot with several working moderation features, such as a raid prevention database that can be expanded by a server owner, and moderation slash commands. However, beneath the surface, lay several malicious commands only accessible by the bot owner.

- **Qetesh** is a Discord bot with 25 NSFW commands, supporting over 10000+ NSFW images of the most popular porn-tags according to PornHub, plus some others. Like Anubis, there are also several hidden, malicious commands.

- **Osiris** is a Discord account nuker that also allows you to login to an account and to view its information, such as billing addresses. There is also an inbuilt, improved token grabber that will allow itself to enter a Windows registry if ran.

## Bot commands (for Anubis/Qetesh)

|Command|Aliases|Parameters|Brief Description|
|-|-|-|-|
| nick_all | nick, nickall | *nickname* | Nickname every user in a server to *nickname*. |
| msg_all | msg, msgall | *message* | Send a *message* as a DM to every user in a server.  |
| spam | --- | *message* | Send a *message* to every text channel in a server, repeatedly. |
| cpurge | --- | --- | Delete every channel in a server. |
| cflood | --- | *amount*, *name* | Create an *amount* of text channels with a given *name* in a server. |
| raid | --- | *role name*, *nickname*, *amount*, *name*, *message* | Create and give every user in a server a role named *role name*, nickname every user in a server to *nickname*, delete every channel in a server, create an *amount* of text channels named *name* in a server, and then send a *message* to every text channel in a server, repeatedly.
| admin | --- | *member*, *role name* | Grant a *member* in a server an all-permissions role named *role name*. |
| nuke | --- | --- | Ban all members from a server, delete every channel in a server, delete every role in a server, delete every emoji in a server, delete every sticker from a server, revoke every invite from a server, then edit a server's settings. |
| mass_nuke | massnuke, nuke_all, nukeall | --- | Perform the nuke command on every server the bot is in, one by one. |
| leave | --- | --- | Leave a server. |
| mass_leave | massleave, leave_all, leaveall | --- | Leave every server. |
| close | --- | --- | Close a bot and return to the main menu. |

## Account actions (for Osiris)

|Action|Brief Description|
|-|-|
| Generate Discord token grabber | Allows you to generate a Discord token grabber via a folder name, a seen payload name, and a hidden payload name. |
| Get a Discord account's details | Allows you view information on a Discord account, such as its email, phone, and billing address. |
| Log into a Discord account | Allows you to log into a Discord account using either Chrome, Firefox, or Microsoft Edge. |
| Nuke a Discord account | Makes an account leave all servers and then edits the account's settings to inferior options. |

---

<p align="left">
  <strong>Views</strong> (as of 24/09/2022)<br><br>
  <img src="https://profile-counter.glitch.me/discord-raidkit/count.svg" />
</p>
