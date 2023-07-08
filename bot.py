import datetime
import asyncio
import time

import discord
from discord.ext import commands

# { "user" :  elapsed_time}
times = {

}


class Timer:
    def __init__(self, user):
        self.user = user
        ct = datetime.datetime.now()
        self.start = ct.timestamp()

    def end_timer(self):
        ct = datetime.datetime.now()
        end = ct.timestamp()

        timer_elapsed = end - self.start

        m, s = divmod(timer_elapsed, 60)
        h, m = divmod(m, 60)

        return f"{int(h):02}:{int(m):02}:{int(s):02}"


YES = "✅"
NO = "❌"

bot = commands.Bot(command_prefix=".", intents=discord.Intents.all())
token = "MTExODkwOTE5MDUyMjU1NjQxNg.G0R6gU.rkBeN3ZSo54aKun1jEP6tUubppfIdjRF_cQGLU"
study_channel_id = 1127141283463450645

platinum = 1127150943239151636
gold = 1127151589149388870
bronze = 1127151723224502292
# { "user" :  Timer() }
timers = {

}


def bold(qry):
    return "**" + qry + "**"


def italics(qry):
    return "_" + qry + "_"


def underline(qry):
    return "__" + qry + "__"


def h(size, qry):
    h_ = "".join(["#" for _ in range(size)])
    return h_ + qry


async def send(qry, ctx):
    await ctx.send(f"{qry}")


# @bot.command(pass_context=True)
# @commands.has_role("Admin") # This must be exactly the name of the appropriate role
# async def addrole(ctx):
#     member = ctx.message.author
#     role = get(member.server.roles, name="Test")
#     await bot.add_roles(member, role)

@bot.event
async def on_ready():
    print("Hello, Study bot is ready")
    channel = bot.get_channel(study_channel_id)
    await channel.send("Hello, Study bot is ready")


@bot.command(name="start")
async def start_timer(ctx):
    ctx: commands.Context

    if timers.get(ctx.author) is not None:
        msg = await ctx.send(
                f"You already have a timer running in background.\n{bold('Do you want to restart the timer?')}")
        msg: ctx.message

        for r in [YES, NO]:
            await msg.add_reaction(r)

        # def check(*args):
        #     print (args)
        # channel = message.channel

        reaction, user = await bot.wait_for('reaction_add', check=lambda message, sender: sender == ctx.author)
        reaction: discord.reaction.Reaction
        user: discord.member.Member

        # reaction.emoji.pri
        print(reaction, type(reaction), user, ctx.author, type(user))
        # print(reaction in YES, str(reaction).lower() == str(YES).lower(), NO)
        if YES in reaction.emoji and user == ctx.author:
            await msg.delete()
            await ctx.send("Restarting the timer")
            new_timer_obj = Timer(ctx.author)

            timers[ctx.author] = new_timer_obj
        elif NO in reaction.emoji and user == ctx.author:
            await msg.delete()
            await ctx.send("Canceling the request")
        # await ctx.send(f'```{user}``` reacted with {reaction} reaction')

        # reaction, user = await ctx.wait_for('reaction_add', timeout=60.0, check=check)
    else:
        new_timer_obj = Timer(ctx.author)

        timers[ctx.author] = new_timer_obj

        await ctx.send(bold(f"Starting Study session for {ctx.author}"))

    # print(ctx.author)
    # print(datetime.datetime.now())


@bot.command(name="end")
async def end_timer(ctx):
    ctx: commands.Context
    timer = timers[ctx.author]
    # await send(, ctx)
    ct = datetime.datetime.now()
    end = ct.timestamp()

    et = end - timer.start
    h = round(((et / 60) / 60))
    if h >= 15:
        role = discord.utils.get(ctx.guild.roles, id=platinum)
        await ctx.author.add_roles(role)
    elif h >= 10:
        role = discord.utils.get(ctx.guild.roles, id=gold)
        await ctx.author.add_roles(role)
    elif h >= 5:
        role = discord.utils.get(ctx.guild.roles, id=bronze)
        await ctx.author.add_roles(role)

    await ctx.send(bold(f"Deleting the timer, {underline(f'Elapsed time {timer.end_timer()}')}."))
    timers.pop(ctx.author)


@bot.command(name="get_time")
async def get_timer(ctx):
    ctx: commands.Context
    timer = timers[ctx.author]
    await send(f"Time Elapsed {timer.end_timer()}", ctx)


@bot.command()
async def add(ctx, *args):
    res = 0
    for r in args: res += int(r)
    await ctx.send(f"Hello! ans is {res}")


bot.run(token)
