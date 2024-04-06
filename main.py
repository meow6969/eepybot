import importlib
import json
import os

import git
import discord
from discord.ext import commands

from utils import classes


with open("config.json") as meowf:
    meow = json.load(meowf)
    prefix = meow["prefix"]
    timeout_time = meow["timeout-time"]
    eepy_server = meow["eepy-server"]
    eepy_role = meow["eepy-role"]
    mins_to_eep = meow["mins-to-eep"]
    welcome_channel = meow["welcome-channel"]
    debug = meow["debug"]
    debug_prefix = meow["debug-prefix"]
    owners = meow["owner-ids"]


bot_intents = discord.Intents.default()
bot_intents.members = True
bot_intents.message_content = True

if debug:
    prefix = debug_prefix

client = commands.Bot(command_prefix=prefix, intents=bot_intents, fetch_offline_members=True, case_insensitive=True)
client.timeout_time = timeout_time
client.eepy_server = eepy_server
client.eepy_role = eepy_role
client.mins_to_eep = mins_to_eep
client.welcome_channel = welcome_channel
client.debug = debug
client.owners = owners


@client.event
async def on_ready():
    # cogs
    cogs = os.listdir('./cogs/')
    for cog in cogs:
        cog_list = cog.split('.')
        if cog_list[len(cog_list) - 1] == 'py':
            await client.load_extension(f'cogs.{cog_list[0]}')

    print(f'{classes.bcolors.OKGREEN}Logged on as {client.user}!{classes.bcolors.ENDC}')

    if client.debug:
        print(f'{classes.bcolors.OKGREEN}loaded debug eepybot{classes.bcolors.ENDC}')
    else:
        print(f'{classes.bcolors.OKGREEN}loaded eepybot{classes.bcolors.ENDC}')


@client.command(hidden=True)
async def reload(ctx):
    with open('config.json') as file:
        client.owners = json.load(file)["owner-ids"]
    if ctx.author.id in owners:
        if not debug:
            try:
                g = git.cmd.Git(os.getcwd())
                g.pull()
            except Exception as e:
                await ctx.send(f"error in git pull:\n{e}")
        with open('config.json') as configf:
            config = json.load(configf)
            client.owners = config['owner-ids']

        try:
            importlib.reload(classes)
        except Exception as e:
            ctx.send(f"error in reloading main.py imports:\n{e}")

        try:
            cogs_ = os.listdir('./cogs/')
            for cog_ in cogs_:
                _cog_list = cog_.split('.')
                if _cog_list[len(_cog_list) - 1] == 'py':
                    await client.reload_extension(f'cogs.{_cog_list[0]}')
        except Exception as e:
            await ctx.send(f"error in reloading cogs:\n{e}")

        await ctx.send('reloaded')

with open("config.json") as meow:
    if client.debug:
        token = json.load(meow)["debug-token"]
    else:
        token = json.load(meow)["token"]

# client = MyClient()
client.run(token)
