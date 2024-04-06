import importlib
import contextlib
import io

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
        if member.guild != self.client.get_guild(self.client.eepy_server):
            return
        await chnl.send(f"heloooooooooooooooooooooo <@{member.id}>")

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f"pong! `{round(self.client.latency * 1000)}ms`")

    @commands.command(hidden=True)
    async def execute(self, ctx, *, code):
        if ctx.author.id not in self.client.owners:
            return
        if code.strip() == "":
            await ctx.send("there is no code")
            return
        ansi = ""
        nobacktick = False
        slice_num = 0
        if "return=" in code.split()[0]:
            slice_num += len(code.split()[0])
            args = code.split()[0].split("=")[1].split(",")
            for arg in args:
                if arg == "ansi":
                    ansi = "ansi"
                elif arg == "nobacktick":
                    nobacktick = True
        code = code[slice_num:]
        if code.strip().startswith("```"):
            code = code.strip()[3:]
            if code.startswith("py"):
                code = code[3:]
        if code[-3:] == "```":
            code = code[:-3]
        str_obj = io.StringIO()  # Retrieves a stream of data

        try:
            with contextlib.redirect_stdout(str_obj):
                exec(code, {'self': self})
        except Exception as e:
            return await ctx.send(f"```py\n{e.__class__.__name__}: {e}```")
        
        stdout = str_obj.getvalue()
        if stdout == "":
            await ctx.send("no stdout")
            return
        if nobacktick:
            stdout = stdout.replace("`", "'")
        if len(stdout) > 1990:
            msg = f"output is too long, truncating\n```{ansi}\n{stdout}"[:1990]
            msg += "```"
            await ctx.send(msg)
            return
        await ctx.send(f'```{ansi}\n{stdout}```')


async def setup(client):
    await client.add_cog(misc(client))
