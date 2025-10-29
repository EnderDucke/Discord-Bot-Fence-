import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import webserver

load_dotenv()
token = os.getenv("DISCORD_TOKEN")

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

scav_role = "Scav"

@bot.event
async def on_ready():
    print(f'Welcome to the hideout {bot.user.name}.')

@bot.event
async def on_member_join(member):
    await member.send(f'Welcome to the hideout {member.name}.')

# Prevents people saying "awesomesauce"
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if "awesomesauce" in message.content.lower():
        await message.delete()
        await message.channel.send(f"{message.author.mention}, don't say that scav-y boy (or girl).")

    await bot.process_commands(message)

# !hello
@bot.command()
async def hello(ctx):
    await ctx.send(f"Hello {ctx.author.mention}! Nice to see a decent PMC.")

# Assigns user to Scav role
@bot.command()
async def assign(ctx):
    role = discord.utils.get(ctx.guild.roles, name=scav_role)
    if role:
        await ctx.author.add_roles(role)
        await ctx.send(f"{ctx.author.mention} is now a good {scav_role}.")
    else:
        await ctx.send(f"Role doesn't exist.")

@bot.command()
async def remove(ctx):
    role = discord.utils.get(ctx.guild.roles, name=scav_role)
    if role:
        await ctx.author.remove_roles(role)
        await ctx.send(f"{ctx.author.mention} is no longer a {scav_role}.")
    else:
        await ctx.send(f"Role doesn't exist.")

@bot.command()
@commands.has_role(scav_role)
async def secret(ctx):
    await ctx.send(f"You'll be a friend to all scavs {ctx.author.mention}.")

@secret.error
async def secret_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("I don't recognize you as a Scav.")

@bot.command()
async def dm(ctx, *, msg):
    await ctx.author.send(f"You said {msg}")

@bot.command()
async def reply(ctx):
    await ctx.reply("This is a reply to your message.")

@bot.command()
async def poll(ctx, *, question):
    embed = discord.Embed(title="New Poll", description=question)
    poll_message = await ctx.send(embed=embed)
    await poll_message.add_reaction("👍")
    await poll_message.add_reaction("👎")

webserver.keep_alive()
bot.run(token, log_handler=handler, log_level=logging.DEBUG)