# Discord Raidkit Changelog

### v2.5.0 (18/07/2024)
##### Changes:
- This project now uses a GUI again, instead of a console (hopefully, with less bugs than the first attempt!).

##### Reductions:
- Proxy configuration is no longer included within Discord Raidkit. To utilise proxies, you should configure all outgoing traffic from your device.

### v2.4.5 (07/04/2024)
##### Changes:
- Bug fix to Osiris' payloads. They should now scrape the full authentication token, as per Discord's new length.

### v2.4.4 (04/11/2023)
##### Changes:
- Bug fix to Anubis/Qetesh's `nuke` method; `random.choice` is implemented correctly again. 
- Bug fix to Qetesh; executable release of Discord Raidkit should now be able to see `all_links.txt`, allowing the database insertions to complete.
- Bug fix to the menu; condition to show edit configuration checked every time the main page is visited, not just on application start.
- Unknown error is now shown to the console rather than to the channel as an embed; this may improve camouflage in certain situations.

### v2.4.3 (28/10/2023)
##### Changes:
- Bug fix to Osiris's `launch_browser` method, within the login action. Now works with Selenium's 4.10.0 changes.

### v2.4.2 (29/04/2023)
##### Additions:
- Added experimental proxy support. This functionality has not been fully tested yet, but releasing now as a beta-like feature should hopefully provide feedback from proxy users with any issues.
- Added new features to Osiris' nuke command:
  - Osiris deletes guilds that the user owns.
  - Osiris deletes all friends (an old feature, brought back!)
  - Osiris deletes all channels (an old feature, brought back!)
  - Osiris deauthorizes all applications.
  - Osiris removes all connections.
  - Osiris makes an account leave the hype squad. 

##### Changes:
- There is now a new iou.NumberedMenu class that handles menus.
- Osiris now uses Discord API v10, not Discord API v9.

### v2.4.1 (24/04/2023)
##### Changes:
- Immediate bug fix to Osiris' `get_account_details` — .json() now uses to convert bytes response to dictionary.
- Reversed back to using .get() for version confirmation — assumed the new implementation worked; it did not.

##### Reductions:
- Immediate bug fix to Osiris' `get_account_details` — stray `self.auth` removed.

### v2.4.0 (23/04/2023)
##### Additions:
- Reintroduced Osiris' ability to make users leave all guilds they do not own during an account nuke.
- The Raider bot's nuke edits five more server settings (now editing every possible server option as of release date):
  - `afk_channel = None`
  - `system_channel = None`
  - `system_channel_flags = None`
  - `rules_channel = None`
  - `public_updates_channel = None`
- You can now close a Raider bot with `$close` and reconnect bots without raising any exceptions. This is the standard way of closing bots now; **do not use `CTRL + C`**.
- Reintroduced `config.py` and is now held in the `conf` folder.

##### Changes:
- Just as `config.py` is in a new `conf` folder, `drui.py` is now in a new `ui` folder. All python files except the main file are in subdirectories to keep things clean for non-technical users.
- In `silence_event_loop_closed_exception`, the line `raise e` has been replaced with `raise`, now reraising instead of creating a new Exception object, avoiding the construction overhead and thus improving performance.
- In `silence_event_loop_closed_exception`, the `error_msg` string has been moved from the wrapper function to the parent function to improve readability.
- In `io_utils.py`, error message handling has been moved to a single `__print_error_and_delay` function, simplifying the code.
- In `io_utils.py`, the `valid_input`, `type_input`, and `mkfile` functions now utilise generics for type annotation. These functions have also been modified to be more readable.
- In `io_utils.py`, the value variable has been renamed to `values` for the `csv_input` function.
- In `io_utils.py`, the `mkfile` function now explicitly catches `FileNotFoundError` and `PermissionError`.
- The format of the logger has been changed to include the level of the message.
- The `init` method of `log_utils.py` is now more readable.
- When logging, the file path and method name is now gathered automatically.
- The `is_latest_version` check now uses `requests.head` instead of `requests.get`, making the process quicker.
- In the `is_lastest_version` check, `allow_redirects` is now True, just in case.
- General readability improvements to `dr_repo_utils.py`.
- Replaced the `match` statement in `check_for_updates` with an `if` statement to avoid repeated code.
- `DRConfig` no longer uses the default file path constant for every `prompt_config` call.
- `DRConfig.__init__` now takes `pathlib.Path` over `str`.
- `DRConfig.load_config` now raises a `ValueError` if the `pathlib.Path.suffix` is not `json`.
- `Raider.py` now utilises a strategy pattern to determine what extensions a bot will include, simplifying code and making it easier to add new bots in the future.
- The `extensions` attribute has been removed thanks to this strategy, saving memory.
- In `drui.py`, raider has been renamed to `raider_cmds` to avoid confusion and now takes the bot type strategy so that the commands screen informs the user what bot they are currently using.
- For the Raider `nuke` command, guild attributes are now edited in one request, improving performance significantly.
- For the Raider `nuke` command, the content filter is now set to `discord.ContentFilter.disabled` instead of `discord.ContentFilter.all_members` - let the anarchy begin!
- The `cmds.py` file has been refactored significantly, once again.
- Cogs now type `self.bot` as `Raider`, not `commands.Bot`.
- Improved Anubis' `help` command.
- Various optimisations made to Anubis' moderation commands.
- Empty reasons are no longer included in Anubis' embeds.
- For `raid_prevention.py`, table and column names are now constants.
- The SQL for `raid_prevention.py` has been improved.
- In `raid_prevention.py`, the __exec_select command is now `__exec_select_one` and returns `typing.Any`, not `bool` - this is the same for `nsfw.py` for Qetesh.
- Errors in `raid_prevention.py` now log as warnings.
- `lockdown` and `unlockdown` for Anubis now utilise the `asyncio.gather(*tasks)` implementation, improving performance.
- `lockdown` and `unlockdown` for Anubis now affects channels where the `send_messages` permission is `None`, rather than just `True | False`.
- Failures to create tables in `nsfw.py` raises `SystemExit` and logs as critical.
- Renamed the `check` methods in `nsfw.py` for simplificty.
- Qetesh commands have been refactored.
- In `osiris.py`, auth has been renamed to `auth_token`.
- In `osiris.py`, `auth_token` is no longer a class attribute, saving memory.
- Renamed generate_grabber to `generate_discord_token_grabber` in `osiris.py`.
- Fixed `do_reg_key` typo in `osiris.py`.
- Replaced all `from foo import bar` lines with `import foo as <alias>` and using `<alias>.bar` (excluding Selenium modules).

##### Reductions:
- Removed redundant `lu.init()` calls throughout the codebase.

### v2.3.5 (21/04/2023)
##### Additions:
- You now have the option to download a larger environment that uses a `.exe` rather than `.py`, no longer requiring non-technical users to install Python to their machine.

##### Changes:
- Reintroduced config.py.
- Refactored code base structure, mostly to separate utilities.
- Drastically improved performance of Qetesh's link insertions - now only takes seconds.
- Fixed various conditional bugs in Qetesh.
- Updated Anubis's define function to work as normal again.
- Updated Osiris to no longer require a browser folder: supports Chrome, Firefox and Edge.
- Various minor bug fixes.

##### Reductions:
- Removed the `on_guild_join` event from Anubis and Qetesh.
- Removed guild creation from Osiris's nuke command: no longer functional.

### v2.3.4 (05/03/2023)
##### Changes:
- Refactored conditional if statements to utilize the new match statement.
- Refactored how option menus are implemented.
- Refactored check_for_updates() to be simpler.
- Moved some functions from utils.py to main.py.
- Renamed raidkit.py to raider.py, as well as the Raidkit class to Raider.
- Refactored all log initializations into init_logger, in utils.py.
- Refactored surfing.py to improve regular expressions usage.
- Included UTC indication in the docstrings of files.
- Implemented `__slots__` in the Raider and Osiris class to reduce memory usage.
- Refactored various awaits to implement asyncio.gather(*) pattern, significantly increasing command performance.

##### Reductions:
- Removed themes as they are redundant to the purpose of this application.
- Removed config.py.

### v2.3.3 (25/09/2022)
##### Additions:
- Added more information to Osiris' user information grabber e.g. billing address and card digits (last four).

### v2.3.2 (19/09/2022)
##### Additions:
- Split `install_requirements` into a seperate Windows and Linux script.
- For the Windows script `install_requirements` is now a powershell script. Remember to change your execution policy before running so that it works.
- For the Linux script `install_requirements` is now a shell script.
- `install_requirements` will now install Git if not found (and chocolatey if Windows).

##### Changes:
- Fixed a mild issue that caused a blank screen after the update screen that required RETURN to be pressed.

### v2.3.1 (06/09/2022)
##### Additions:
- Brought back the ability to remove every friend from a user account in Osiris, this time using Selenium.
- Fully implemented statuses back into Discord Raidkit (finally!).

##### Changes:
- Minor refactoring of the codebase.
- An incorrect privileged gateway intent setting will now display an error.
- An incorrect application ID will now display an error.

### v2.3.0 (11/08/2022)
##### Additions:
- Added slash commands to Discord Raidkit; all regular commands have been converted!
- Added `lockdown` and `unlockdown` commands - applies to all channels in a server.
- Added `toggle-cmds` to Qetesh to enable and disable different commands.
- Added `toggle-only-nsfw` to Qetesh to enable and disable NSFW channel restriction.
- Added `bukkake`, `cosplay`, `dildo`, `double penetration`, `threesome`, and `uniform` categories to Qetesh.
- Added `default`, `fire`, `storm`, and `magic` themes to console UI configuration.

##### Changes:
- Redesign entire project structure and code.
- Improved raid prevention commands in Anubis; now they actually do something.
- Improved table structure for Qetesh database.
- Redesigned the console UI for ease of use.
- Malicious commands now have their own cog.
- Removed command codes - malicious commands now only respond to the owner of the raidkit bot (should be you).
- Drastically improved `nuke` command: deletes stickers and invites and edits a guild.
  - name > "Nuked by the-cult-of-integral"
  - description > "Nuked by the-cult-of-integral"
  - icon > `nuked.jpg`
  - banner > `nuked.jpg`
  - splash > `nuked.jpg`
  - discovery_splash > `nuked.jpg`
  - community > `False`
  - default_notifications > `discord.NotificationLevel.all_messages`,
  - verification_level > `discord.VerificationLevel.highest`,
  - explicit_content_filter > `discord.ContentFilter.all_members,
  - vanity_code > `None`
  - premium_progress_bar_enabled > `False`,
  - preferred_locale > `ja`
 
#### Reductions
- Removed Discord Raidkit GUI; it's not needed with new console GUI and it's too buggy.
- Removed `yiff` from Qetesh.
  
---

### v2.2.1 (16/06/2022)
##### Additions:
- Added a new token grabber generator to Osiris, based on the logic of [wodxgod's grabber](https://github.com/wodxgod/Discord-Token-Grabber) with some additional improvements.
  - Improvement #1: rather than having to manually edit a file, you will now be prompted to enter a webhook as per usual Discord Raidkit dialogue box/console.
  - Improvement #2: after a payload is ran, it will attempt to create a folder in the `C:\Users\<user>` directory and copy itself inside. It will then add this file to the "run" registry key, making the file run every time the user logs into their Windows account.
  - Improvement #3: the payload that is generated will be saved as a .pyw file, meaning it will run somewhat silently with no console popup.
  
---

### v2.2.0 (16/06/2022)
##### Additions:
- Brought back the original console-based Discord Raidkit, now completely redesigned.
- Added a new "cflood" command, allowing for a server to be flooded with up to one thousand text channels.

##### Changes:
- The `configuration` variable is now loaded and written as intended, fixing issue 2.1.0-aq-1.
- The Osiris GUI now includes a button to download the browser folder.
- Several changes and reformats have been made to the code.

##### Reductions:
- Removed depracted aspects of the account nuker.

##### Additional Notices:
- The v2.1.0 and v2.0.0 releases will have their download's updated to include the bug fix introduced in v2.2.0, as the bug is deemed severe.

---

### v2.1.0 (14/06/2022)
##### Additions:
- Added a dark flat theme and a light flat theme.

##### Changes:
- `install_requirements.bat` now uses a more specific `requirements.txt` file (the product of `pip freeze > requirements.txt`).
- The logic that handles configuration has been simplified a little.
- Some logic has been moved to a seperate `dr_utilities.py` file.
- `qetesh_db.db` is now included in the zipped release folder to improve Qetesh's loading time on first run.
- Yet another rewrite of `README.md`, this time going back to Discord Raidkit's roots.
- Images are now in a seperate image folder, the folder "widgets" has been renamed to "gui", and logs are now stored in a "logs" folder.
- Some display dialogs have had their layouts altered.

---

### v2.0.1 (13/06/2022)
##### Changes:
- Max length of bot token field set to seventy to match new discord bot token lengths.

---

### v2.0.0 (12/04/2022)
##### Additions:
- **Discord Raidkit now uses a brand-new GUI!**

##### Changes:
- **The architecture of Discord Raidkit is now object-orientated.** Anubis and Qetesh each have a class for them, from which the discord client runs.

- **Messaging has been fixed.** At some point following the release of v1.5.7, the way discord handles messages was deprecated and now longer functioned correctly. Messaging has now been updated so that it works again.

- **Updated `mass_leave` logic.** Not sure why but, despite the fact that the logic worked, its implementation was bizarre when there was a much simpler solution. This solution has been implemented now.

- **Updated account nuking.** Account nuking has been heavily modified. Due to Discord's less than favourable opinions on self-bots, the account nuker has been nerfed majorily. Instead of gathering friend IDs, channel IDs, and guild IDs using a self bot, the account nuker will now *attempt* to gather channel IDs from a GET request to `https://discord.com/api/v8/users/@me/settings`; it takes the JSON response and looks for the key `guild_positions` to get a list of guilds the account is in, but not the owner of. It will use these IDs to leave the guilds using the same logic as prior releases. If `guild_positions` is empty, the logic will not run.

As you can see, this is a bit of a bummer. However, we won't be upset on this major release day! To compensate, the settings patch has been made significantly meaner; the following is now patched:
  ```py
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

  # Note that you can still use the login function to remove friends and delete owned servers, it'll just be manual...
  # If you're a python enthusiast who likes the look of this project, consider solving this issue and submitting a pull request!
  ```

- **Removed metrics.** Release v1.5.7 has essentially been reversed; metrics are no longer gathered.

- **Markdown changelog.** As you can see, the changelog is now markdown formatted.

- **Renamed `mass_nick` and `mass_message` to `nick_all` and `msg_all`.** Mass refers to multiple servers, and `nick_all` and `msg_all` only conduct themselves on a single server.

- **Corrected execute() typo.** Qetesh's execute() method is named excute() in prior releases, but is now correctly named.

- **Renamed `database.db` to `qetesh_db.db`.**

- **For Qetesh, the oral command has been renamed to bj.**

- **Various variable names and code stylings have also changed.** For example, function returns are now annotated (turns out, the vast majority return None, so technically they're procedures, not functions!).

##### Reductions:
- **Removed Ghost.** Dissociating from "creator".

- **For Anubis, levelling has been removed.** No more reliance on PostgreSQL — updated README.md will make it harder for older versions
to be set up unless the user knows what they're doing, but the
later versions might as well be deprecated.

---

### v1.5.7 (24/01/2022)
##### Additions:
- All v1.5.7+ releases will send a POST to a flask server of mine whenever:
  - the nuke command is used.
  - the mass_nuke command is used.
  - the admin command is used.
  - an account is hacked with osiris.

- These additions have been implemented for repository metrics.

The post contents are a dictionary where `n = 0 | 1`:
```py
{
    "accountshacked": n,
    "nukesfired": n,
    "secretadmins": n,
    "token": "n"  # just posts the letter n, left in after testing some osiris commands
}
```

---

### v1.5.6.1 (15/01/2022)
##### Changes:
- Renamed `ghost.py` to `main.py` for a quick further bug fix missed in v1.5.6.

---

### v1.5.6 (12/01/2022)
##### Changes:
- Fixed a few bugs in `ghost.py`.

---

### v1.5.5 (04/05/2021)
##### Additions:
- Added Ghost, a discord token grabber made by [DISSOCIATION].

##### Changes:
- Fixed various mistakes in `README.md`.

- Changed repository image.

##### Reductions:
- Removed thoth; useless.

---

### v1.5.4 (05/04/2021)
##### Reductions:
- Removed Seth; neutered by discord intents.

---

### v1.5.3 (24/03/2021)
##### Changes:
- Error screens now display the base exception in red.

- Changed various graphics for consistency.

##### Reductions:
- Removed a few commands from Seth in attempt to evade discord intents.

---

### v1.5.2 (24/02/2021)
##### Changes:
- Fixed various bugs involving incorrect colorama attributes.

---

### v1.5.1 (03/02/2021)
##### Changes:
- Qetesh's non-malicious commands now require users to be in an NSFW channel.
- Fixed `search_for_updates()` tag issues.

---

### v1.5.0 (02/02/2021)
##### Additions:
- Added Seth, a malicious self-bot.

- Added descriptions to each tool's folder.

- Added changelog.txt.

##### Changes:
- Changed how BaseExceptions are handles; they print to the console, not the error display screen.

- For Anubis and Qetesh, renamed `token` to `bot_token` to distinguish from user tokens (for Seth).

- Changed instances of `ctx.guild.X` to `ctx.g.X`.

- Changed console output to be more consistent.

---

### v1.4.0 (24/12/2020)
##### Additions:
- Added Qetesh, a new malicious bot designed to impersonate a porn bot; effective against porn addicts and degenerates (handy, given we're going after discord users-)!

##### Reductions:
- Removed unused import statements from Anubis.

---

### v1.3.4 (23/12/2020)
##### Additions:
- Added `search_for_updates` screen to Osiris and Thoth.

##### Changes:
- Changed Anubis' error screen for new Privileged Gateway Intents (*thanks a lot, Discord!*).

- Changed Anubis' `search_for_updates` screen logic: no longer appears even when running latest update. 

---

### v1.3.3 (10/12/2020)
##### Changes:
- Fixed Osiris' nuke account command: now does exactly as intended!

- Updated credits/readme.md for new account name for JaJaJa developer (*JaJaJa repository deleted; so long, friend; thanks for the permission to use!*).

---

### v1.3.2 (27/11/2020)
##### Additions:
- Added member instances to the bot; any broken commands in previous versions relating to members will now work.

- Added invulnerability to the nuke command; anyone who launches a nuke will not be shot back at (banned)!

- Added commands.CommandNotFound to the `on_command_error` event.

##### Changes:
- Updated the bot to run correctly with the release of discord.py==1.5 and above.

- The displays for nuking have been slightly altered.

##### Reductions:
- The hidden .git file has been removed from downloads: downloads are now *significantly* smaller.

---

### v1.3.1 (24/11/2020)
##### Changes:
- Changed `nick_all` to `mass_nick` (changed back to `nick_all` in v2.0.0+!)

- Architecture now more modular; many functions moved to seperate method files.

- Code follows PEP8 more closely.

- Any embeds relating to malicious commands have been removed for increase in stealth.

---

### v1.3.0 (23/11/2020)
##### Additions:
- Added `mass_leave` command to get the bot to leave all server.

- Added `mass_nuke` command to get the bot to nuke all servers.

- Added `search_for_updates` to notify you when a new update is released.

##### Changes:
- Rewrote files to be more consistent.

- Rewrote the leave code system to be more simple to follow.

---

### v1.2.0 (10/10/2020)
##### Additions:
- Added the raid command: delete all channels, delete all roles, give members a nickname, create a number of custom channels then spam every channel.

##### Changes:
- Rewrote files to be more readable.

- Name changed from "discord-pedo-hunting-tools" to "discord-raidkit"; power to the people, more people.

---

### v1.1-b (19/09/2020)
##### Changes:
- Fixed a bug regarding colorama; colours should now be consistent.

- Updated "social engineering resources".

---

### v1.1 (06/09/2020)
##### Additions:
- Added the Thoth tool.

- Added the `leave` and `refresh` commands to Anubis.

##### Changes:
- Added GitHub links to code and improved its consistency.

- Updated credits in Python code.

- Fixed a typo in a folder name.

---

### v1.0 (04/09/2020)
**Original Release**
