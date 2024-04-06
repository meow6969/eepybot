import importlib

import discord
from discord.ext import commands

from utils import classes


class misc(commands.Cog):
    def __init__(self, client):
        self.client = client

        importlib.reload(classes)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content.strip() != '':
            print(f'{classes.bcolors.OKCYAN}Message from {message.author}: {message.content}{classes.bcolors.ENDC}')

    @commands.Cog.listener()
    async def on_member_join(self, member):
        chnl = self.client.get_channel(self.client.welcome_channel)
        if chnl.guild != self.client.get_guild(self.client.eepy_server):
            return
        await chnl.send(f"heloooooooooooooooooooooo <@{member.id}>")

    # @commands.command()
    # async def ping(self, ctx):
    #     await ctx.send(f"pong! `{round(self.client.latency * 1000)}ms`")


async def setup(client):
    await client.add_cog(misc(client))
