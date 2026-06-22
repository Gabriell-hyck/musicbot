import discord
from discord.ext import commands
import yt_dlp
import asyncio

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Queue system
music_queue = []

# FFmpeg options
FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
}

# yt-dlp options
YDL_OPTIONS = {
    'format': 'bestaudio/best',
    'quiet': True,
    'no_warnings': True,
    'default_search': 'ytsearch'
}

@bot.event
async def on_ready():
    print(f'{bot.user} udah online!')

@bot.command()
async def join(ctx):
    """Join voice channel"""
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()
        await ctx.send(f'Udah join ke {channel.name}')
    else:
        await ctx.send('Lo harus di voice channel dulu!')

@bot.command()
async def leave(ctx):
    """Leave voice channel"""
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send('Dah cabut!')

@bot.command()
async def play(ctx, *, query):
    """Play music dari YouTube"""
    voice_client = ctx.voice_client
    
    if not voice_client:
        if ctx.author.voice:
            channel = ctx.author.voice.channel
            voice_client = await channel.connect()
        else:
            await ctx.send('Join voice channel dulu!')
            return
    
    async with ctx.typing():
        with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(query, download=False)
            
            if 'entries' in info:
                # Playlist atau search result
                url = info['entries'][0]['url']
                title = info['entries'][0]['title']
            else:
                url = info['url']
                title = info['title']
            
            music_queue.append((url, title))
    
    await ctx.send(f'Ditambahin ke queue: **{title}**')
    
    if not voice_client.is_playing():
        await play_next(ctx)

async def play_next(ctx):
    """Play next song in queue"""
    voice_client = ctx.voice_client
    
    if music_queue:
        url, title = music_queue.pop(0)
        audio_source = discord.FFmpegPCMAudio(url, **FFMPEG_OPTIONS)
        
        voice_client.play(audio_source, after=lambda e: asyncio.run_coroutine_threadsafe(play_next(ctx), bot.loop))
        await ctx.send(f'Sekarang playing: **{title}**')
    else:
        await ctx.send('Queue kosong!')

@bot.command()
async def skip(ctx):
    """Skip current song"""
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.stop()
        await ctx.send('Di-skip!')
    else:
        await ctx.send('Gak ada lagu yang playing!')

@bot.command()
async def pause(ctx):
    """Pause music"""
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.pause()
        await ctx.send('Di-pause!')
    else:
        await ctx.send('Gak ada lagu yang playing!')

@bot.command()
async def resume(ctx):
    """Resume music"""
    if ctx.voice_client and ctx.voice_client.is_paused():
        ctx.voice_client.resume()
        await ctx.send('Di-resume!')
    else:
        await ctx.send('Gak ada lagu yang di-pause!')

@bot.command()
async def queue(ctx):
    """Show current queue"""
    if music_queue:
        queue_list = '\n'.join([f'{i+1}. {title}' for i, (_, title) in enumerate(music_queue)])
        await ctx.send(f'**Queue:**\n{queue_list}')
    else:
        await ctx.send('Queue kosong!')

@bot.command()
async def clear(ctx):
    """Clear the queue"""
    music_queue.clear()
    await ctx.send('Queue udah di-clear!')

# Replace with your bot token
bot.run('YOUR_BOT_TOKEN_HERE')
