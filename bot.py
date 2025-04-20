import discord
from discord.ext import commands
import json, docker, random, string

# Load config
with open("config.json") as f:
    config = json.load(f)

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=config["prefix"], intents=intents)

client = docker.from_env()
vps_data = {}  # {userid: [ {vps details} ]}
port_list = []

def random_string(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

@bot.event
async def on_ready():
    print(f"Bot is online as {bot.user}")
    channel = discord.utils.get(bot.get_all_channels(), name="general")
    if channel:
        await channel.send("Bot is online! Type `/` to see available commands.")

@bot.command()
async def deployipv4(ctx, userid: int, ram: str, cpu: str, disk: str, password: str):
    username = "vpsuser"
    container = client.containers.run("ubuntu-vps", detach=True, ports={'22/tcp': None})
    ip = "127.0.0.1"
    vps_info = {
        "ip": ip, "user": username, "pass": password,
        "ram": ram, "cpu": cpu, "disk": disk, "version": "IPv4"
    }
    vps_data.setdefault(userid, []).append(vps_info)
    await ctx.send(f"IPv4 VPS for <@{userid}>:\nIP: `{ip}`\nUser: `{username}`\nPass: `{password}`")

@bot.command()
async def deployipv6(ctx, userid: int, ram: str, cpu: str, disk: str):
    username = "vpsuser"
    password = random_string()
    ip = "2001:0db8::" + random_string(4)
    vps_info = {
        "ip": ip, "user": username, "pass": password,
        "ram": ram, "cpu": cpu, "disk": disk, "version": "IPv6"
    }
    vps_data.setdefault(userid, []).append(vps_info)
    await ctx.send(f"IPv6 VPS for <@{userid}>:\nIP: `{ip}`\nUser: `{username}`\nPass: `{password}`")

@bot.command()
async def list(ctx):
    uid = ctx.author.id
    if uid in vps_data:
        msg = "\n".join([f"{v['version']} {v['ip']} {v['user']} {v['pass']}" for v in vps_data[uid]])
    else:
        msg = "No VPS found."
    await ctx.send(msg)

@bot.command()
async def portadd(ctx, *ports):
    global port_list
    port_list.extend(ports)
    await ctx.send(f"Ports added: {', '.join(ports)}")

@bot.command()
async def update(ctx):
    await ctx.send("Bot is up-to-date. Last update: v1.0 — IPv6, Port Management, Admin Tools.")

@bot.command()
async def botadmin(ctx):
    admins = ", ".join([f"<@{aid}>" for aid in config["admin_ids"]])
    await ctx.send(f"Bot Admins: {admins}")

@bot.command()
async def botinfo(ctx):
    dev = "<@1258646055860568094>"  # Replace with your ID
    await ctx.send(f"Bot Developer: {dev}\nDocker VPS Bot - v1.0\nIPv4 & IPv6, SSH, Port Control, Admin Panel.")

@bot.command()
async def delvps(ctx, userid: int):
    if ctx.author.id not in config["admin_ids"]:
        return await ctx.send("Unauthorized.")
    vps_data.pop(userid, None)
    await ctx.send(f"Deleted all VPS for user `{userid}`.")

# run the bot
bot.run(TOKEN)
