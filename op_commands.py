
from interactions.models.internal.extension import Extension

from interactions import slash_command, SlashContext, slash_option

from interactions import is_owner
from interactions import Activity, ActivityType, Color
import nosync_tools as ns

class op_commands(Extension):
    @slash_command(name="bot_reload", description="reloads Bot instance", scopes=[])
    async def bot_reload(self, ctx:SlashContext):
        if is_owner():
            bot_info: dict = ns.open_json("Variables.json")
            await self.bot.change_presence(
                activity=Activity(name=bot_info["general_variables"]["startup_activity"], type=ActivityType.WATCHING))
            await ctx.send("Reload Completed, New Variables Fetched ✅", ephemeral=True)
        else:
            await ctx.send("You dont have Permission to do so!")

def setup(bot):
    op_commands(bot)