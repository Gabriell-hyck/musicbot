import os
import discord
from discord.ext import commands
import yt_dlp
import asyncio
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix="gaby!",
    intents=intents,
    help_command=None
)

music_queue = []

YDL_OPTIONS = {
    "format": "bestaudio/best",
    "default_search": "ytsearch",
    "noplaylist": True,
    "quiet": True
}

FFMPEG_OPTIONS = {
    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
    "options": "-vn"
}


async def play_next(ctx):
    if not music_queue:
        return

    query = music_queue.pop(0)

    try:
        with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(query, download=False)

            if "entries" in info:
                info = info["entries"][0]

            url = info["url"]
            title = info["title"]

        source = await discord.FFmpegOpusAudio.from_probe(
            url,
            **FFMPEG_OPTIONS
        )

        vc = ctx.voice_client

        vc.play(
            source,
            after=lambda e: asyncio.run_coroutine_threadsafe(
                play_next(ctx),
                bot.loop
            )
        )

        await ctx.send(f"🎵 Sedang memutar: **{title}**")

    except Exception as e:
        await ctx.send(f"❌ Error: {e}")


@bot.event
async def on_ready():
    print(f"✅ Login sebagai {bot.user}")

    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.listening,
            name="musik 24/7"
        )
    )


@bot.command()
async def join(ctx):
    if not ctx.author.voice:
        return await ctx.send(
            "❌ Masuk voice channel dulu bro."
        )

    channel = ctx.author.voice.channel

    if ctx.voice_client is None:
        await channel.connect()

    await ctx.send(
        f"✅ Bergabung ke **{channel.name}**"
    )


@bot.command()
async def leave(ctx):
    if ctx.voice_client:
        music_queue.clear()
        await ctx.voice_client.disconnect()
        await ctx.send("👋 Keluar dari voice channel")


@bot.command()
async def play(ctx, *, lagu):
    if not ctx.author.voice:
        return await ctx.send(
            "❌ Masuk voice channel dulu bro."
        )

    if ctx.voice_client is None:
        await ctx.author.voice.channel.connect()

    music_queue.append(lagu)

    await ctx.send(
        f"➕ Ditambahkan ke antrean: **{lagu}**"
    )

    if not ctx.voice_client.is_playing():
        await play_next(ctx)


@bot.command()
async def skip(ctx):
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.stop()
        await ctx.send("⏭️ Lagu dilewati")


@bot.command()
async def stop(ctx):
    music_queue.clear()

    if ctx.voice_client:
        ctx.voice_client.stop()

    await ctx.send("⏹️ Musik dihentikan")


@bot.command()
async def pause(ctx):
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.pause()
        await ctx.send("⏸️ Musik dijeda")


@bot.command()
async def resume(ctx):
    if ctx.voice_client:
        ctx.voice_client.resume()
        await ctx.send("▶️ Musik dilanjutkan")


@bot.command()
async def queue(ctx):
    if not music_queue:
        return await ctx.send(
            "📭 Antrean kosong"
        )

    daftar = "\n".join(
        f"{i+1}. {lagu}"
        for i, lagu in enumerate(music_queue)
    )

    await ctx.send(
        f"📜 Antrean:\n```{daftar}```"
    )


@bot.command()
async def now(ctx):
    if ctx.voice_client and ctx.voice_client.is_playing():
        await ctx.send(
            "🎶 Ada musik yang sedang diputar."
        )
    else:
        await ctx.send(
            "📭 Tidak ada musik yang diputar."
        )


@bot.command()
async def ping(ctx):
    await ctx.send(
        f"🏓 {round(bot.latency * 1000)}ms"
    )


@bot.command()
async def help(ctx):
    await ctx.send("""
🎵 hi aku gaby, bot music buatan @flyingdutchweirdman

gaby!join
gaby!leave
gaby!play <judul lagu>
gaby!skip
gaby!stop
gaby!pause
gaby!resume
gaby!queue
gaby!now
gaby!ping
""")

bot.run(TOKEN)
