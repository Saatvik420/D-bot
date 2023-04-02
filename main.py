import discord
import random
from discord.ext import commands, tasks
from itertools import cycle


status = cycle(['Status 1', 'Status 2'])

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

client = commands.Bot(command_prefix='!')

# Status of bot and bot ready


@client.event
async def on_ready():
    # await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='Spider-Man: No Way Home'))
    change_status.start()
    print("The bot is ready!")


@client.command()
async def ping(ctx):
    await ctx.send(f'Pong!\n **Shard**: {round(client.latency*1000)}ms')


@client.command(aliases=['8ball'])
async def _8ball(ctx, *, question):
    responses = ["As I see it, yes.", "Ask again later.", "Better not tell you now.", "Cannot predict now.", "Concentrate and ask again.", "Don’t count on it.", "It is certain.", "It is decidedly so.", "Most likely.",
                 "My reply is no.", "My sources say no.", "Outlook not so good.", "Outlook good.", "Reply hazy, try again.", "Signs point to yes.", "Very doubtful.", "Without a doubt.", "Yes.", "Yes – definitely.", "You may rely on it."]
    await ctx.send(f':8ball:| {random.choice(responses)}')


@client.command()
async def clear(ctx, amount=6):
    await ctx.channel.purge(limit=amount+1)


@client.command()
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'Kicked {member}!')


@client.command()
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'Banned {member}!')


@client.command()
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user
        if(user.name, user.discriminator == (member_name, member_discriminator)):
            await ctx.guild.unban(user)
            await ctx.send("Unbanned the User!")


@tasks.loop(seconds=10)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Invalid command used.")


client.run("OTM1NzMyOTM5ODM5Mzg5NzQ3.YfC7NQ.GxumNEIhSTDzSSvuEHyEW8PxPlw")