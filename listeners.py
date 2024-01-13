import interactions
from interactions import Extension
from interactions import listen
from interactions import events, Embed


class listeners(Extension):
    @listen()
    async def on_message_delete(self, event: events.MessageDelete):
        guild = await self.bot.fetch_guild(889967115380080641)
        channel = await guild.fetch_channel(1095757994211426416)
        embed = Embed(f"Message Deleted!")
        embed.add_field("User", event.message.author)
        if event.message.content != "":
            embed.add_field("Message Content", event.message.content)
            embed.add_field("Channel", event.message.channel.name)
            embed.set_footer("Powered by RGB-Networking", icon_url=self.bot.user.avatar.url)
           # embed.color = event.message.author.user.accent_color
            await channel.send(embed=embed)
        else:
            await channel.send("Embed Deleted:")


def setup(bot):
    listeners(bot)