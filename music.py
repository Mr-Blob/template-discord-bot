import discord
from discord.ext import commands
import youtube_dl
import asyncio

YT_DL_OPTS = {
	"format": 'mp3[abr>0]/bestaudio/best',
	"ignoreerrors": True,
	"default_search": "auto",
	"source_address": "0.0.0.0",
	'quiet': True
}


@commands.command(alias='connect')
	async def join(ctx):
        bot.voice = await ctx.author.voice.channel.connect(timeout=60.0, reconnect=False)
        if bot.voice.is_connected():
            await ctx.send(f'Joined {ctx.author.voice.channel.name}')

        else:
            await ctx.send('Connection unsuccessful')

        await ctx.message.delete()

	@commands.command(alias='disconnect')
	async def leave(ctx):
    bot.voice.disconnect()

    @commands.command()
    async def play(ctx, *, search):
        if bot.voice.is_connected():
            downloader = youtube_dl.YoutubeDL(YT_DL_OPTS)
            info = downloader.extract_info(search, download=False)

            if info.get('_type') == 'playlist':
                info = info['entries'][0]

            url = info['url']
            title = info.get('title')

            ffmpeg_player = discord.FFmpegPCMAudio(url)

            bot.voice.play(ffmpeg_player)
            await ctx.send(f'Now Playing {title}')


    @commands.command()
    async def pause(ctx):
		if not bot.voice.is_paused() and bot.voice.is_playing():
        	await bot.voice.pause()
		else:
			await ctx.send('I am already paused...')

	@commands.command()
	async def resume(ctx):
		if bot.voice.is_paused():
			await bot.voice.resume()
		else:
			await ctx.send('I am not paused...')
