import tinydb
import asyncio
from discord.ext.commands import Bot
import discord
import settings
import os
import time

client = Bot(command_prefix=("?", "#"))


@client.command(name='add_ronnie', pass_context=True)
async def add_voice_channel(context):
    voice_channel = context.author.voice.channel
    with tinydb.TinyDB('../Resources/DB/db.json') as db:
        if voice_channel.id not in list(map(lambda entry: entry['channel'], db.table('channels').all())):
            db.table('channels').insert({'channel': voice_channel.id})
            await context.send(f'Voice Channel "{voice_channel}" Added')
        else:
            await context.send(f'Voice Channel "{voice_channel}" Already Added')


@client.command(name='remove_ronnie', pass_context=True)
async def remove_voice_channel(context):
    voice_channel = context.author.voice.channel
    with tinydb.TinyDB('../Resources/DB/db.json') as db:
        if voice_channel.id in list(map(lambda entry: entry['channel'], db.table('channels').all())):
            db.table('channels').remove(tinydb.Query().channel == voice_channel.id)
            await context.send(f'Voice Channel "{voice_channel}" Removed')
        else:
            await context.send(f'Voice Channel "{voice_channel}" Has Not Been Found')


@client.command(
    name='ronnie',
    pass_context=True
)
async def ronnie(ctx):
    print(ctx)
    voice_channel = ctx.author.voice.channel
    channel = None
    if voice_channel is not None:
        channel = voice_channel.name
        vc = await voice_channel.connect()
        vc.play(discord.FFmpegPCMAudio('a.mp3'))
        while vc.is_playing():
            time.sleep(.1)
        await vc.disconnect()
    else:
        await ctx.send(str(ctx.author.name) + "is not in a channel.")
    await ctx.message.delete()


async def playback_queue():
    await client.wait_until_ready()
    while not client.is_closed():
        with tinydb.TinyDB('../Resources/DB/db.json') as db:
            for voice_channel_id in list(map(lambda entry: entry['channel'], db.table('channels').all())):
                if (voice_channel := client.get_channel(voice_channel_id)).voice_states:
                    await play(voice_channel)
        await asyncio.sleep(5)


@client.event
async def on_ready():
    client.loop.create_task(playback_queue())
    print("Logged in as " + client.user.name)


async def play(voice_channel):
    voice_channel = voice_channel
    voice_channel_connection = await voice_channel.connect()
    voice_channel_connection.play(discord.FFmpegPCMAudio('../Resources/Sounds/a.mp3'))
    while voice_channel_connection.is_playing():
        time.sleep(.1)
    await voice_channel_connection.disconnect()


if __name__ == '__main__':
    settings.initialize()
    client.run(os.getenv('TOKEN'))
