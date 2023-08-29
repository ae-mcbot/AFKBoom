from javascript import require, On, Once, console
import time
from cmd2 import Cmd
from lib.config import config
import discord
from discord.ext import commands
mineflayer = require("mineflayer", "latest")
lobby = 0
bot = mineflayer.createBot({
  "host": 'landania.net',
  "username": config()["BOT_USER"]["USERNAME"],
  "auth": 'microsoft',
  "version": "1.19.2",
  "hideErrors": 'False',
  "debug": 'True'
})
dc_bot = commands.Bot()
pathfinder = require('mineflayer-pathfinder').pathfinder
mcData = require('minecraft-data')(bot.version)
ChatMessage = require('prismarine-chat').mineflayer
Entity = require("prismarine-entity")(bot.version)
guild_ids=[1129058853703655474,930147010768678992]

@On(bot, 'resourcePack')
def handle(*args):
    print("resourcePack")
    time.sleep(5)
    bot.acceptResourcePack()
    return
@On(bot, 'spawn')
def handle(*args):
    global lobby
    if lobby == 1:
        print("I spawned!")
        time.sleep(5)
        bot.chat("/home Bot")
        print("Lade mich auf Discord ein:")
        print(f"https://discord.com/api/oauth2/authorize?client_id={dc_bot.application_id}&permissions=2112&scope=bot")
    lobby += 1
    return

@dc_bot.slash_command(name="help", description="Lists all commands of this Bot", guild_ids=guild_ids)
async def help(ctx):
    embed = discord.Embed(
        title="AFKBoom",
        description="Vollständige Liste an Commands",
        color=discord.Colour.blurple(),  # Pycord provides a class with default colors you can choose from
    )
    embed.add_field(name="**Nachrichten**",
                    value="""`msg` Sendet eine Nachricht an einen Spieler
                             `cc` Sendet eine Nachricht in den Clanchat *(wenn der Bot in einem Clan ist)*
                             `publicchat` Sendet eine Nachricht in den öffentlichen Chat *mit [BOT]*
                            """)
    embed.add_field(name="**Sonstiges**",
                    value="""`shutdown` Beendet den Bot
                             `restart` Startet den Bot neu
                             `update` Macht ein Update des Bot mit anschließendem Neustart
                             `payout` Zahlt Coins an einen User
                            """)


    embed.set_footer(text="Powered by AFKBoom", icon_url="https://raw.githubusercontent.com/ae-mcbot/AFKBoom/main/AFKBoomLogo.jpg")

    await ctx.respond("Here are the requested docs!", embed=embed)

@dc_bot.slash_command(name="nachrichtenversenden", description="Sends a private message to a user", guild_ids=guild_ids)
async def nachrichtenversenden(ctx, user: discord.Option(str), msg: discord.Option(str)):
    if await dc_bot.is_owner(ctx.author) and lobby >= 1:
        bot.chat(f"/msg {user} {msg}")
        await ctx.respond(f"Message successfully sent to {user}")
    elif not dc_bot.is_owner(ctx.author):
        await ctx.respond(f"You are not the owner of this Bot!")
    else:
        await ctx.respond(f"Internal Error, please restart the Bot")

@dc_bot.slash_command(description="Sends the bot's latency.", guild_ids=guild_ids)
async def ping(ctx):
    await ctx.respond(f"Pong! Latency is {dc_bot.latency}ms")

@dc_bot.slash_command(name="clanchat", description="Sends a message to the clanchat", guild_ids=guild_ids)
async def clanchat(ctx, msg: discord.Option(str)):
    if await dc_bot.is_owner(ctx.author) and lobby >= 1:
        bot.chat(f"/cc {msg}")
        await ctx.respond(f"Message successfully sent to clan chat")
    elif not dc_bot.is_owner(ctx.author):
        await ctx.respond(f"You are not the owner of this Bot!")
    else:
        await ctx.respond(f"Internal Error, please restart the Bot")
@dc_bot.slash_command(name="publicchat", description="Sends a message to the public minecraft chat", guild_ids=guild_ids)
async def publicchat(ctx, msg: discord.Option(str)):
    if await dc_bot.is_owner(ctx.author) and lobby >= 1:
        msg = "[BOT] " + msg
        bot.chat(f"/cc {msg}")
        await ctx.respond(f"Message successfully sent in public Chat")
    elif not dc_bot.is_owner(ctx.author):
        await ctx.respond(f"You are not the owner of this Bot!")
    else:
        await ctx.respond(f"Internal Error, please restart the Bot")
@dc_bot.slash_command(name="payout", description="Pays out coins to a minecraft player", guild_ids=guild_ids)
async def payout(ctx, user: discord.Option(str), amount: discord.Option(str)):
    if await dc_bot.is_owner(ctx.author) and lobby >= 1:
        bot.chat(f"/pay {user} {amount}")
        await ctx.respond(f"Coins successfully paid to {user}")
    elif not dc_bot.is_owner(ctx.author):
        await ctx.respond(f"You are not the owner of this Bot!")
    else:
        await ctx.respond(f"Internal Error, please restart the Bot")

dc_bot.run(config()["API"]["DISCORD"])