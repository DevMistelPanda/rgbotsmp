import datetime


import interactions
from interactions.models.internal.extension import Extension
import requests
import asyncio
import warnings
import interactions
from interactions import slash_command, SlashContext, slash_option
from interactions import OptionType
from interactions import Permissions
from interactions import Activity, ActivityType, Color

import main
import nosync_tools as ns
from interactions import Embed



class general_commands(Extension):



#######################################################################################################################

    @slash_command(name='serverstatus', description='Retrieve website information')
    async def website_info(self, ctx):
        url = main.URL
        response = requests.get(url, verify=False)
        # Filter and ignore the InsecureRequestWarning
        warnings.filterwarnings("ignore", category=requests.packages.urllib3.exceptions.InsecureRequestWarning)
        if response.ok:
            html_content = response.text
            server1, server2 = ns.parse_server_info(html_content)
            embed = ns.create_embed(server1, server2)

            await ctx.send(embed=embed)
            #await main.send_website_info()
        else:
            await ctx.send(f'Failed to retrieve website information. Status code: {response.status_code}')

    @slash_command(name="smpsetup", description="get ready for our SMP")
    async def getready(self, ctx: SlashContext):
        if ctx.author.has_role(989915966299324457):
            await ctx.send("you are already set for our SMP!", ephemeral=True)
        else:
            await ctx.author.add_role(989915966299324457)
            await ctx.send("you got access to everything regarding our SMP! \nHave Fun Playing :)", ephemeral=True)

    @slash_command(name="purge", description="cleans up after someone did something dirty")
    @slash_option(name="messages", description="How many Messages do you want to delete?", required=True, opt_type=OptionType.INTEGER, min_value=1, max_value=50)
    async def purge(self, ctx: SlashContext, messages: int):
        if ctx.author.has_permission(Permissions.MANAGE_MESSAGES):
            await ctx.channel.purge(deletion_limit=messages)
            await ctx.send(f"Deleted {messages} successfully ✅")
        else:
            await ctx.send(content="you do not have the Permissions to do that!", color=Color.RED)

    @slash_command(name="ping", description="checks the ping of the bot")
    async def ping(self, ctx: SlashContext):
        response = await ctx.send("🏓 Calculating Pong...")

        async def get_average_ping():
            total_ping = 0
            count = 0
            for _ in range(10):
                total_ping += round(self.bot.latency * 1000)
                count += 1
                await  asyncio.sleep(0.2)

            return round(total_ping / count)

        average_ping = await get_average_ping()
        await response.edit(content=f"🏓 Average Ping: {average_ping} ms")

    @slash_command(name="whois", description="Get User Information")
    @slash_option(name="member", description="User to get Information for", opt_type=OptionType.USER)
    async def whois(self, ctx:SlashContext, member=None):
        member = member or ctx.author
        def get_user_roles(User):
            roles = ""
            for i in User.roles:
               roles = roles + f"{i.mention} "
            return roles


        if member.id == self.bot.user.id:
            botinfoembed = Embed()
            botinfoembed.set_author(name=f"{member.user}", icon_url=member.display_avatar.url)
            botinfoembed.description = member.user.mention + "(Bot)"
            botinfoembed.add_field("Joined", member.joined_at, inline=True)
            botinfoembed.add_field("Registered", member.created_at, inline=True)
            botinfoembed.add_field("Version", ns.open_json("Variables.json")["info"]["Version"])
            botinfoembed.add_field("Bot Status", ns.open_json("Variables.json")["info"]["Status"], inline=True)
            botinfoembed.add_field(f"Roles [{len(member.roles)}]", get_user_roles(member))
            botinfoembed.color = member.top_role.color
            botinfoembed.thumbnail = member.display_avatar.url
            botinfoembed.footer = f"ID: {member.id}"
            botinfoembed.timestamp = datetime.datetime.now()
            await ctx.send(embed=botinfoembed)
        else:
            simpembed = Embed()
            simpembed.set_author(name=f"{member}", icon_url=member.display_avatar.url)
            simpembed.description = member.user.mention
            if member.bot:
                simpembed.description = member.user.mention + " (Bot)"
            simpembed.add_field("Joined", member.joined_at, inline=True)
            simpembed.add_field("Registered", member.created_at, inline=True)
            simpembed.add_field(f"Roles [{len(member.roles)}]", get_user_roles(member))
            simpembed.color = member.top_role.color
            simpembed.thumbnail = member.display_avatar.url
            simpembed.footer = f"ID: {member.id}"
            simpembed.timestamp = datetime.datetime.now()
            await ctx.send(embed=simpembed)


def setup(bot):
    general_commands(bot)
