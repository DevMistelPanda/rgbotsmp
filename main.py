import aiohttp
import asyncio
import interactions
from interactions import listen
from interactions import Activity, ActivityType
from interactions.ext import prefixed_commands
from interactions import Intents, is_owner
import nosync_tools as ns
from interactions import slash_command, SlashContext, slash_option, OptionType, check, Status




#opens General Variables.json in a dict file to access important information
bot_info: dict = ns.open_json("Variables.json")

#innitializes the bot
bot = interactions.Client(token=bot_info["general_variables"]["TOKEN"], intents = Intents.DEFAULT | Intents.MESSAGE_CONTENT) #implements the bot

#innitializing required Variables from Variables.json

CHANNEL_ID = bot_info["smp_infos"]["server_info_channel"] #Channel ID to send smp information
URL = bot_info["smp_infos"]["server_info_url"] #Website to gain smp information

#sets default prefix
prefixed_commands.setup(bot, default_prefix='+')

# Store the message object
message = None

#Store Genereal Information from Variables.json



@listen()
async def on_ready():
    global bot_info
    print(f'Logged in as {bot.user.username} ({bot.user.id})')
    ns.logthis("info", f"Logged in as {bot.user.username} ({bot.user.id})")
    await bot.change_presence(activity=Activity(name=bot_info["general_variables"]["startup_activity"], type=ActivityType.WATCHING))
    print("cleaning up channel...")
    ns.logthis("info", "Cleanup Completed... Running Bot Routine")
    channel = bot.get_channel(CHANNEL_ID)
    await channel.purge(deletion_limit=50)
    print("catching Server Information...")
    await send_website_info(channel)


async def send_website_info(channel):
    global message  # Use the global message variable


    async with aiohttp.ClientSession() as session:
        async with session.get(URL, ssl=False) as response:
            if response.status == 200:
                html_content = await response.text()
                server1, server2 = ns.parse_server_info(html_content)
                modified_content = html_content.replace("<br/>", "\n")
                if message is None:
                    #cleans the channel before sending the new message
                    await bot.get_channel(CHANNEL_ID).purge(deletion_limit=50)
                    # If the message is not set, send a new message
                    message = await channel.send(modified_content)
                else:
                    # If the message is already set, edit it with the new content
                    await message.edit(content=modified_content)
            else:
                await channel.send(f'Failed to retrieve website information. Status code: {response.status}')

    # Schedule the next update after 30 seconds
    await asyncio.sleep(30)
    await send_website_info(channel)

@slash_command(name="reload_server_info", description="Relaods SMP Information on WeLikeMoreRGBEEE")
async def reload_server_info(ctx: SlashContext):
    global message
    message = None
    await ctx.send("Reload Command completed ✅", ephemeral=True)
    await send_website_info(channel=bot.get_channel(CHANNEL_ID))


########################################################################################################################




bot.load_extension("general_commands")
bot.load_extension("op_commands")
bot.load_extension("maintain_bugs")
bot.load_extension("listeners")



bot.start()
