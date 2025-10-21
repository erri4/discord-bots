import discord
from discord.ext import commands

EMOJIS = {
    "yes": "✅",
    "no": "❌",
}
CYCLE = ['v', '<', '^', '>']
CHANNEL: str
TOKEN: str

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True

bot = commands.Bot(command_prefix="!", intents=intents)

curr = 0

@bot.event
async def on_message(message: discord.Message):
    global curr, CYCLE, EMOJIS
    if message.author == bot.user:
        return
    if message.channel.name != CHANNEL:
        return
    if message.content.lower() == CYCLE[curr]:
        await message.add_reaction(EMOJIS["yes"])
    else:
        curr = 0
        await message.add_reaction(EMOJIS["no"])
        await message.channel.send(f"{message.author.mention} broke it! start again from {CYCLE[curr]}")
    curr += 1

bot.run(TOKEN)
