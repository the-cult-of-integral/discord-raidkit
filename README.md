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

![Discord Raidkit v2.4.4 Console](https://user-images.githubusercontent.com/98130822/235321378-f624a5ba-5ff6-4f80-b37e-8a1691724c53.png)

## Tools

- **Anubis** is a Discord bot with [nine malicious commands](#malicious-bot-commands). However, unlike other nuking tools, Anubis also has several non-malicious slash commands, including a moderation suite, to help you convince server administration to add the bot.

- **Qetesh** is a Discord bot with [nine malicious commands](#malicious-bot-commands). However, Qetesh also has 25 NSFW slash commands for the most popular pornographic kinks, at least according to PornHub. These commands should help take advantage of the degeneracy of Discord users.

- **Osiris** is the account manager of Discord Raidkit. Using Osiris, you can save the information of an account, login to an account using either Chrome, Firefox, or Microsoft Edge, or you can fully nuke an account, deleting channels, guilds, friends, and connections, deauthorizing applications, removing hype squad, and PATCHing various account settings. You can also generate Discord token grabbers within Windows Registry support. As of v2.4.2, Osiris has beta support for proxies.
 
Remember, if you need help setting these tools, you can always visit the [Discord Raidkit Wiki](https://github.com/the-cult-of-integral/discord-raidkit/wiki)!
 
## Installation

1. Head over to [the latest release](https://github.com/the-cult-of-integral/discord-raidkit/releases/latest).
2. Download the EXE zip.
3. Extract and run the executable in its directory.

**Notice:** Some anti-malware may flag this project as harmful — especially any files that relate to Osiris, as this tool generates token stealers. If you are having issues with anti-malware constantly getting in the way of using this tool, you can create a folder, add that folder to the anti-malwares list of excluded search/scan locations, then place the Discord Raidkit files in said folder. This should allow Discord Raidkit to function correctly without interferance. **Do not randomly exclude every location on your computer!**

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

<p align="left">
  <strong>Views</strong> (as of 24/09/2022)<br><br>
  <img src="https://profile-counter.glitch.me/discord-raidkit/count.svg" />
</p>

---

## v3.0.0 - November Preview

For those of you keeping up, you will be aware that I was working on converting this application to React.JS front-end. At the time, I was working with create-react-app, and the intention would be for the user to download the files, install node.js and run it locally. However, it quickly came to me that this idea was stupid. So, I then looked at using Electron with React.JS to distribute a desktop application, with a React.JS front-end. However, I'm not sure you would all appreciate a 250MB executable for a program that was previously 24KB.

So, I am now at plan three: a Tauri desktop application with a React.JS front-end. Now, the advantage of this is that the executable size shouldn't be ludicrous, and you'll all get prettier graphics that aren't a confusing terminal from the 90s. The disadvantage is that the backend is in Rust, and I've never used Rust. So, I suppose this will be an oppertunity for me to learn Rust. In the meantime, here's a screenshot of recent development. As you can see, as well as being a Desktop application now, there is also a dark mode! :)

![DR Tauri Preview](https://github.com/the-cult-of-integral/discord-raidkit/assets/98130822/efbfc892-8906-48cf-994d-03f21c3600c6)

