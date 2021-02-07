import asyncio
import os
import time
from random import choice, randint
import bot_help
from ImageCollector import ImageCollector
import discord
import settings
import tinydb
from datetime import datetime
import re
import quotes
from discord.ext.commands import Bot

client = Bot(command_prefix=("?", "#", "!"))


@client.event
async def on_ready():
    client.loop.create_task(quote_queue())
    client.loop.create_task(playback_queue())
    print("Logged in as " + client.user.name)


@client.event
async def on_guild_join(guild):
    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            await channel.send(bot_help.help_text)
        break


@client.command(name='ronnie_add', pass_context=True)
async def add_voice_channel(context):
    try:
        voice_channel = context.author.voice.channel
        dm_channel = context.channel
        with tinydb.TinyDB(os.getenv('DB_PATH')) as db:
            if voice_channel.id not in list(map(lambda entry: entry['voice_channel'], db.table('channels').all())):
                db.table('channels').insert(
                    {
                        'voice_channel': voice_channel.id,
                        'dm_channel': dm_channel.id,
                        'interval': int(os.getenv('DEFAULT_INTERVAL')),
                        'quote_time': os.getenv('DEFAULT_QUOTE_TIME'),
                        'timestamp': int(time.time())
                    }
                )
                await context.send(f'Voice Channel "{voice_channel}" Added')
                await context.send(bot_help.help_text)
            else:
                await context.send(f'Voice Channel "{voice_channel}" Already Added')
    except AttributeError as error:
        print(error)
        print('User not in any Voice Channel')


@client.command(name='ronnie_remove', pass_context=True)
async def remove_voice_channel(context):
    try:
        voice_channel = context.author.voice.channel
        with tinydb.TinyDB(os.getenv('DB_PATH')) as db:
            if voice_channel.id in list(map(lambda entry: entry['voice_channel'], db.table('channels').all())):
                db.table('channels').remove(tinydb.Query().voice_channel == voice_channel.id)
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
            if voice_channel.id in list(map(lambda entry: entry['voice_channel'], db.table('channels').all())):
                if len(message := context.message.content.split()) != 2 or not message[1].isnumeric():
                    raise ValueError('Wrong command format, type "!ronnie" for help')
                db.table('channels').update(
                    {
                        'interval': int(message[1])
                    },
                    tinydb.Query().voice_channel == voice_channel.id
                )
                await context.send(f'Ronnie Interval for Channel "{voice_channel}" set to {message[1]} seconds.')
            else:
                await context.send(f'Voice Channel "{voice_channel}" Has Not Been Added Yet - type "!ronnie" for help')
    except AttributeError:
        print('User not in any Voice Channel')
    except ValueError as error:
        await context.send(error)


@client.command(name='ronnie_quote_time', pass_context=True)
async def set_channel_quote_time(context):
    try:
        dm_channel = context.channel
        with tinydb.TinyDB(os.getenv('DB_PATH')) as db:
            if dm_channel.id in list(map(lambda entry: entry['dm_channel'], db.table('channels').all())):
                if len(message := context.message.content.split()) != 2 or not re.match(r'^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$', message[1]):
                    raise ValueError('Wrong command format, type "!ronnie" for help')
                db.table('channels').update(
                    {
                        'quote_time': message[1]
                    },
                    tinydb.Query().dm_channel == dm_channel.id
                )
                await context.send(f'Ronnie Quote Time for Channel "{dm_channel}" set to {message[1]}.')
            else:
                await context.send(f'Text Channel "{dm_channel}" Has Not Been Added Yet - type "!ronnie" for help')
    except ValueError as error:
        await context.send(error)


@client.command(name='ronnie', pass_context=True)
async def ronnie_help(context):
    await context.send(bot_help.help_text)


@client.command(name='ronnie_sound', aliases=['lightweight', 'yeahbuddy', 'yeahbaby', 'chant'], pass_context=True)
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
        song = choice([f for f in os.listdir(os.getenv('SOUNDS_PATH')) if f.startswith(context.message.content[1:])])
        voice_channel_connection.play(discord.FFmpegPCMAudio(f'{os.getenv("SOUNDS_PATH")}/{song}'))
        while voice_channel_connection.is_playing():
            time.sleep(.1)
    await voice_channel_connection.disconnect()


@client.command(name='ronnie_vibe_check', pass_context=True)
async def vibe_check(context):
    await sound(context, loops=randint(5, 10))


@client.command(name='ronnie_quote', pass_context=True)
async def quote(context):
    await client.wait_until_ready()
    await send_quote(context.channel.id)


async def playback_queue():
    await client.wait_until_ready()
    while not client.is_closed():
        with tinydb.TinyDB(os.getenv('DB_PATH')) as db:
            for voice_channel_id in list(map(lambda entry: entry['voice_channel'], db.table('channels').all())):
                try:
                    if (voice_channel := client.get_channel(voice_channel_id)).voice_states:
                        channel_data = db.table('channels').search(tinydb.Query().voice_channel == voice_channel_id)[0]
                        if not int(channel_data['timestamp']) + int(channel_data['interval']) > int(time.time()):
                            db.table('channels').update(
                                {
                                    'timestamp': int(time.time())
                                },
                                tinydb.Query().voice_channel == voice_channel_id
                            )
                            await play(voice_channel)
                except AttributeError:
                    print(2)
                    db.table('channels').remove(tinydb.Query().voice_channel == voice_channel_id)
        await asyncio.sleep(5)


async def quote_queue():
    await client.wait_until_ready()
    while not client.is_closed():
        current_time = datetime.now().strftime("%H:%M")
        with tinydb.TinyDB(os.getenv('DB_PATH')) as db:
            for dm_channel_id in list(map(lambda entry: entry['dm_channel'], db.table('channels').all())):
                try:
                    channel_data = db.table('channels').search(tinydb.Query().dm_channel == dm_channel_id)[0]
                    if current_time == channel_data['quote_time']:
                        await send_quote(dm_channel_id)
                except AttributeError:
                    db.table('channels').remove(tinydb.Query().dm_channel == dm_channel_id)
        await asyncio.sleep(60)


async def send_quote(dm_channel_id):
    await client.get_channel(dm_channel_id).send(embed=discord.Embed.from_dict({
        "title": quotes.get_random_quote(),
        "type": "rich",
        "color": 12370112,
        "image": {"url": ImageCollector.get_random_ronnie_image_url()},
        "footer": {"text": "~ Ronnie Coleman"}
    }))


async def play(voice_channel):
    all_sounds = [file for file in os.listdir(os.getenv('SOUNDS_PATH'))]
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
