from discord.ext import commands
import discord
import dotenv
import os
from datetime import datetime, timedelta, timezone

dotenv.load_dotenv()
TOKEN = os.getenv("TOKEN", "TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.command()
async def rule(ctx: commands.Context, number):
    guild = ctx.guild
    if guild is None:
        return
    rules_channel = guild.rules_channel

    if rules_channel is None:
        rules_channel = discord.utils.get(guild.text_channels, name="rules")

    if not rules_channel:
        await ctx.send("Rules channel not found.")
        return

    async for message in rules_channel.history(limit=100):
        content = message.content.strip()

        if content.startswith(f"{number}.") or content.startswith(f"{number} "):
            await ctx.send(
                f"**Rule {number}:**\n`{content[len(f'{number}.') :].strip()}`"
            )
            return

        elif content.lower().startswith(f"rule {number}"):
            await ctx.send(
                f"**Rule {number}:**\n`{content[len(f'rule {number}') :].strip()}`"
            )
            return

    await ctx.send(f"Rule {number} was not found in {rules_channel.mention}.")


@bot.command()
async def rules(ctx: commands.Context):
    guild = ctx.guild
    if guild is None:
        return
    rules_channel = guild.rules_channel

    if rules_channel is None:
        rules_channel = discord.utils.get(guild.text_channels, name="rules")

    if not rules_channel:
        await ctx.send("Rules channel not found.")
        return

    rules_msg = "```json\n"
    async for message in rules_channel.history(limit=100, oldest_first=True):
        content = message.content.strip()
        rules_msg += content + "\n"
    rules_msg += "```"
    await ctx.send(rules_msg)


@bot.command()
async def ynot(ctx: commands.Context):
    async for msg in ctx.channel.history(limit=50):
        if msg.content.startswith("!ynot"):
            await msg.delete()
            await ctx.send("because why not?")
            return


@bot.command()
async def clean(ctx: commands.Context):
    async for msg in ctx.channel.history(limit=100):
        if msg.content.startswith("!") or msg.author.id == 1400924541663973386:
            await msg.delete()


@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx: commands.Context, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(
        f"{member} has been banned. Reason: {reason or 'No reason provided'}"
    )


@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx: commands.Context, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(
        f"{member} has been kicked. Reason: {reason or 'No reason provided'}"
    )


@bot.command()
@commands.has_permissions(moderate_members=True)
async def timeout(
    ctx: commands.Context, member: discord.Member, minutes: float, *, reason=None
):
    until = datetime.now(timezone.utc) + timedelta(minutes=minutes)
    await member.edit(timed_out_until=until, reason=reason)
    await ctx.send(
        f"{member} has been timed out for {minutes} minutes. Reason: {reason or 'No reason provided'}"
    )

@bot.command()
async def unban(ctx: commands.Context, *, member: discord.Member):
    banned_users: list[discord.guild.BanEntry] = await ctx.guild.bans()
    for ban_entry in banned_users:
        user = ban_entry.user
        if user.name.lower() == member.name.lower() or str(user) == member.name:
            await ctx.guild.unban(user)
            await ctx.send(f"{user} has been unbanned.")
            return
    await ctx.send("User not found in ban list.")


@bot.command()
async def untimeout(ctx: commands.Context, member: discord.Member):
    await member.edit(timed_out_until=None)
    await ctx.send(f"{member} is no longer timed out.")

@ban.error
@unban.error
@kick.error
@timeout.error
@untimeout.error
async def command_error(ctx: commands.Context, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You don’t have permission to do that!")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Invalid member or arguments.")
    else:
        raise error


bot.run(TOKEN)
