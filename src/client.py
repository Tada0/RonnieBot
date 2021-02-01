import asyncio
import os
import time
from random import choice, randint
import bot_help
import discord
import settings
import tinydb
from discord.ext.commands import Bot

client = Bot(command_prefix=("?", "#", "!"))


@client.command(name='ronnie_add', pass_context=True)
async def add_voice_channel(context):
    try:
        voice_channel = context.author.voice.channel
        with tinydb.TinyDB(os.getenv('DB_PATH')) as db:
            if voice_channel.id not in list(map(lambda entry: entry['channel'], db.table('channels').all())):
                db.table('channels').insert(
                    {'channel': voice_channel.id, 'interval': 300, 'timestamp': int(time.time())})
                await context.send(f'Voice Channel "{voice_channel}" Added')
            else:
                await context.send(f'Voice Channel "{voice_channel}" Already Added')
    except AttributeError:
        print('User not in any Voice Channel')


@client.command(name='ronnie_remove', pass_context=True)
async def remove_voice_channel(context):
    try:
        voice_channel = context.author.voice.channel
        with tinydb.TinyDB(os.getenv('DB_PATH')) as db:
            if voice_channel.id in list(map(lambda entry: entry['channel'], db.table('channels').all())):
                db.table('channels').remove(tinydb.Query().channel == voice_channel.id)
                await context.send(f'Voice Channel "{voice_channel}" Removed')
            else:
                await context.send(f'Voice Channel "{voice_channel}" Has Not Been Found')
    except AttributeError:
        print('User not in any Voice Channel')


@client.command(name='ronnie_interval', pass_context=True)
async def set_channel_interval(context):
    try:
        voice_channel = context.author.voice.channel
        with tinydb.TinyDB(os.getenv('DB_PATH')) as db:
            if voice_channel.id in list(map(lambda entry: entry['channel'], db.table('channels').all())):
                if len(message := context.message.content.split()) != 2 or not message[1].isnumeric():
                    raise ValueError('Wrong command format, type "?ronnie" for help')
                db.table('channels').update({'interval': int(message[1])}, tinydb.Query().channel == voice_channel.id)
                await context.send(f'Ronnie Interval for Channel "{voice_channel}" set to {message[1]} seconds.')
            else:
                await context.send(f'Voice Channel "{voice_channel}" Has Not Been Found')
    except AttributeError:
        print('User not in any Voice Channel')
    except ValueError as error:
        await context.send(error)


@client.command(name='ronnie', pass_context=True)
async def ronnie_help(context):
    await context.send(bot_help.help_text)


@client.command(name='ronnie_sound', aliases=['lightweight', 'ooo'], pass_context=True)
async def sound(context, loops=1):
    all_sounds = [file for file in os.listdir(os.getenv('SOUNDS_PATH'))]
    voice_channel = context.author.voice.channel
    voice_channel_connection = await voice_channel.connect()
    if context.message.content[1:] in ('ronnie_sound', 'ronnie_vibe_check'):
        for _ in range(loops):
            voice_channel_connection.play(discord.FFmpegPCMAudio(f'{os.getenv("SOUNDS_PATH")}/{choice(all_sounds)}'))
            while voice_channel_connection.is_playing():
                time.sleep(.1)
    else:
        pass
    await voice_channel_connection.disconnect()


@client.event
async def on_guild_join(guild):
    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            await channel.send(bot_help.help_text)
        break


@client.command(name='ronnie_vibe_check', pass_context=True)
async def vibe_check(context):
    await sound(context, loops=randint(5, 10))


async def playback_queue():
    await client.wait_until_ready()
    while not client.is_closed():
        with tinydb.TinyDB(os.getenv('DB_PATH')) as db:
            for voice_channel_id in list(map(lambda entry: entry['channel'], db.table('channels').all())):
                try:
                    if (voice_channel := client.get_channel(voice_channel_id)).voice_states:
                        channel_data = db.table('channels').search(tinydb.Query().channel == voice_channel_id)[0]
                        if not int(channel_data['timestamp']) + int(channel_data['interval']) > int(time.time()):
                            db.table('channels').update({'timestamp': int(time.time())},
                                                        tinydb.Query().channel == voice_channel_id)
                            await play(voice_channel)
                except AttributeError:
                    db.table('channels').remove(tinydb.Query().channel == voice_channel_id)
        await asyncio.sleep(5)


@client.event
async def on_ready():
    client.loop.create_task(playback_queue())
    print("Logged in as " + client.user.name)


async def play(voice_channel):
    all_sounds = [file for file in os.listdir(os.getenv('SOUNDS_PATH'))]
    voice_channel = voice_channel
    try:
        voice_channel_connection = await voice_channel.connect()
        voice_channel_connection.play(discord.FFmpegPCMAudio(f'{os.getenv("SOUNDS_PATH")}/{choice(all_sounds)}'))
        while voice_channel_connection.is_playing():
            time.sleep(.1)
        await voice_channel_connection.disconnect()
    except discord.errors.ClientException:
        print('RonnieBot already Connected')


if __name__ == '__main__':
    settings.initialize()
    client.run(os.getenv('TOKEN'))
