from discord.ext import commands
import discord
import dotenv
import os

dotenv.load_dotenv()
TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.command()
async def rule(ctx: commands.Context, number):
    guild = ctx.guild
    rules_channel = guild.rules_channel

    if rules_channel is None:
        rules_channel = discord.utils.get(guild.text_channels, name="rules")

    if not rules_channel:
        await ctx.send("Rules channel not found.")
        return

    async for message in rules_channel.history(limit=100):
        content = message.content.strip()
        
        if content.startswith(f"{number}.") or content.startswith(f"{number} "):
            await ctx.send(f"**Rule {number}:**\n`{content[len(f"{number}."):].strip()}`")
            return

        elif content.lower().startswith(f"rule {number}"):
            await ctx.send(f"**Rule {number}:**\n`{content[len(f"rule {number}"):].strip()}`")
            return

    await ctx.send(f"Rule {number} was not found in {rules_channel.mention}.")

@bot.command()
async def rules(ctx: commands.Context):
    guild = ctx.guild
    rules_channel = guild.rules_channel

    if rules_channel is None:
        rules_channel = discord.utils.get(guild.text_channels, name="rules")

    if not rules_channel:
        await ctx.send("Rules channel not found.")
        return

    rules_msg = '```json\n'
    async for message in rules_channel.history(limit=100, oldest_first=True):
        content = message.content.strip()
        rules_msg += content + '\n'
    rules_msg += '```'
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

bot.run(TOKEN)
