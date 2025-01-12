import discord      # base discord module
import code         # code.interact
import os           # environment variables
import inspect      # call stack inspection
import random       # dumb random number generator
# Hello from signed land
from discord.ext import commands    # Bot class and utils
 
################################################################################
############################### HELPER FUNCTIONS ###############################
################################################################################
 
# log_msg - fancy print
#   @msg   : string to print
#   @level : log level from {'debug', 'info', 'warning', 'error'}
def log_msg(msg: str, level: str):
    # user selectable display config (prompt symbol, color)
    dsp_sel = {
        'debug'   : ('\033[34m', '-'),
        'info'    : ('\033[32m', '*'),
        'warning' : ('\033[33m', '?'),
        'error'   : ('\033[31m', '!'),
    }
 
    # internal ansi codes
    _extra_ansi = {
        'critical' : '\033[35m',
        'bold'     : '\033[1m',
        'unbold'   : '\033[2m',
        'clear'    : '\033[0m',
    }
 
    # get information about call site
    caller = inspect.stack()[1]
 
    # input sanity check
    if level not in dsp_sel:
        print('%s%s[@] %s:%d %sBad log level: "%s"%s' % \
            (_extra_ansi['critical'], _extra_ansi['bold'],
             caller.function, caller.lineno,
             _extra_ansi['unbold'], level, _extra_ansi['clear']))
        return
 
    # print the damn message already
    print('%s%s[%s] %s:%d %s%s%s' % \
        (_extra_ansi['bold'], *dsp_sel[level],
         caller.function, caller.lineno,
         _extra_ansi['unbold'], msg, _extra_ansi['clear']))
 
################################################################################
############################## BOT IMPLEMENTATION ##############################
################################################################################
 
# bot instantiation
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)
 
# on_ready - called after connection to server is established
@bot.event
async def on_ready():
    log_msg('logged on as <%s>' % bot.user, 'info')
 
# on_message - called when a new message is posted to the server
#   @msg : discord.message.Message
@bot.event
async def on_message(msg):
    # filter out our own messages
    if msg.author == bot.user:
        return
 
    log_msg('message from <%s>: "%s"' % (msg.author, msg.content), 'debug')
 
    # overriding the default on_message handler blocks commands from executing
    # manually call the bot's command processor on given message
    await bot.process_commands(msg)

@bot.event
async def on_voice_state_update(member, before, after):
    if not member.bot and bot.user.voice.channel != None and bot.user.
 
# roll - rng chat command
#   @ctx     : command invocation context
#   @max_val : upper bound for number generation (must be at least 1)
@bot.command(brief='Generate random number between 1 and <arg>')
async def roll(ctx, max_val: int):
    # argument sanity check
    if max_val < 1:
        raise Exception('argument <max_val> must be at least 1')
 
    await ctx.send(random.randint(1, max_val))

# roll_error - error handler for the <roll> command
#   @ctx     : command that crashed invocation context
#   @error   : ...
@roll.error
async def roll_error(ctx, error):
    await ctx.send(str(error))

@bot.command()
async def join(ctx):
    voice = ctx.message.author.voice

    if voice != None:
        await voice.channel.connect()
        await ctx.send(f"Connected and bound to {voice.channel.mention}!")
    else:
        await ctx.send(
            "You need to be connected to a voice channel to use this command!"
        )

@bot.command()
async def leave(ctx):
    voice = ctx.voice_client
    if voice != None:
        await voice.disconnect()
        await ctx.send(f"Left the VC!")
    else:
        await ctx.send("I am not connected to any voice channel!")

@bot.command(brief='Play music on message author channel')
async def play(ctx, name: str):
    voice_channel = ctx.author.voice.channel
    if voice_channel == None:
        await ctx.send("You need to be in a voice channel to use this command")
    elif name == '':
        source = discord.FFmpegPCMAudio('/home/luca/Music/Never gonna give u up.webm');
        ctx.voice_client.play(source)
    else:
        list = os.listdir("/home/luca/Music")
        for file in list:
            if ".mp3" in file and name in file:
                source = discord.FFmpegPCMAudio(f'/home/luca/Music/{file}')
                ctx.voice_client.play(source)

@bot.command(brief='List available tracks')
async def list(ctx):
    list = os.listdir("/home/luca/Music")
    file_list = ""
    for file in list:
        if ".mp3" in file:
            file_list += file + '\n'
    await ctx.send(file_list)

 
################################################################################
############################# PROGRAM ENTRY POINT ##############################
################################################################################
 
if __name__ == '__main__':
    # check that token exists in environment
    if 'BOT_TOKEN' not in os.environ:
        log_msg('save your token in the BOT_TOKEN env variable!', 'error')
        exit(-1)
 
    # launch bot (blocking operation)
    bot.run(os.environ['BOT_TOKEN'])
