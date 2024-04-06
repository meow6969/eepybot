import datetime
import importlib

import discord
from discord.ext import commands
from discord.ext import tasks

from utils import classes
from utils import funcs


class mytasks(commands.Cog):
    def __init__(self, client):
        self.client = client

        self.timeout_eepy.start()

        importlib.reload(classes)
        importlib.reload(funcs)

    async def cog_unload(self):
        self.timeout_eepy.stop()

    @tasks.loop(seconds=30)
    async def timeout_eepy(self):
        funcs.log_print(datetime.datetime.now().strftime('%H:%M'))
        if datetime.datetime.now().strftime('%H:%M') == self.client.timeout_time:
            server = self.client.get_guild(self.client.eepy_server)
            for m in server.members:
                for role in m.roles:
                    if role.id == self.client.eepy_role:
                        # if m.timed_out_until:  this code didnt work and i m too lazy to fix it
                        #     log_print(f"{m.name} is already muted")
                        #     continue

                        try:
                            await m.timeout(
                                datetime.timedelta(minutes=self.client.mins_to_eep),
                                reason="time for u to eep"
                            )
                        except discord.errors.Forbidden:
                            funcs.log_print(f"Unable to mute {m.name}")
                        funcs.log_print(f"muted {m.name}")


async def setup(client):
    await client.add_cog(mytasks(client))
