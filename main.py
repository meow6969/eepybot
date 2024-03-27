import json
import datetime

import discord
from discord.ext import commands
from discord.ext import tasks


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


with open("config.json") as meowf:
    meow = json.load(meowf)
    prefix = meow["prefix"]
    timeout_time = meow["timeout-time"]
    eepy_server = meow["eepy-server"]
    eepy_role = meow["eepy-role"]
    mins_to_eep = meow["mins-to-eep"]


def log_print(text):
    with open("log.txt", "a+") as f:
        f.write(f"{text}\n")


bot_intents = discord.Intents.default()
bot_intents.members = True
bot_intents.message_content = True

client = commands.Bot(command_prefix=prefix, intents=bot_intents, fetch_offline_members=True, case_insensitive=True)
client.timeout_time = timeout_time
client.eepy_server = eepy_server
client.eepy_role = eepy_role
client.mins_to_eep = mins_to_eep


@client.event
async def on_ready():
    # cogs
    # cogs = os.listdir('./cogs/')
    # for cog in cogs:
    #     cog_list = cog.split('.')
    #     if cog_list[len(cog_list) - 1] == 'py':
    #         await client.load_extension(f'cogs.{cog_list[0]}')
    timeout_eepy.start()

    print(f'{bcolors.OKGREEN}Logged on as {client.user}!{bcolors.ENDC}')

    with open('config.json') as configf:
        config = json.load(configf)
        client.owners = config['owner-ids']

    print(f'{bcolors.OKGREEN}loaded eepybot{bcolors.ENDC}')


@client.listen('on_message')
async def on_message(message):
    if message.content.strip() != '':
        print(f'{bcolors.OKCYAN}Message from {message.author}: {message.content}{bcolors.ENDC}')


@client.command(hidden=True)
async def reload(ctx):
    with open('config.json') as file:
        owners = json.load(file)["owner-ids"]
    if ctx.author.id in owners:
        with open('config.json') as configf:
            config = json.load(configf)
            client.owners = config['owner-ids']

        # cogs_ = os.listdir('./cogs/')
        # for cog_ in cogs_:
        #     _cog_list = cog_.split('.')
        #     if _cog_list[len(_cog_list) - 1] == 'py':
        #         await client.reload_extension(f'cogs.{_cog_list[0]}')

        await ctx.send('reloaded')


@client.event
async def on_member_join(member):
    chnl = client.get_channel(825875712559808522)
    await chnl.send(f"heloooooooooooooooooooooo <@{member.id}>")


@tasks.loop(seconds=30)
async def timeout_eepy():
    log_print(datetime.datetime.now().strftime('%H:%M'))
    if datetime.datetime.now().strftime('%H:%M') == client.timeout_time:
        server = client.get_guild(client.eepy_server)
        for m in server.members:
            for role in m.roles:
                if role.id == client.eepy_role:
                    # if m.timed_out_until:  this code didnt work and i m too lazy to fix it
                    #     log_print(f"{m.name} is already muted")
                    #     continue

                    try:
                        await m.timeout(datetime.timedelta(minutes=client.mins_to_eep), reason="time for u to eep")
                    except discord.errors.Forbidden:
                        log_print(f"Unable to mute {m.name}")
                    log_print(f"muted {m.name}")


with open("config.json") as meow:
    token = json.load(meow)["token"]

# client = MyClient()
client.run(token)
