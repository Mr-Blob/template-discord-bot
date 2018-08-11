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


class Music:
    def __init__(self, bot):
        self.bot = bot
		self._queue = []
		self._start_next_track_event = asyncio.Event()

	@commands.command(alias='connect')
	async def join(self, ctx):
        self.bot.voice = await ctx.author.voice.channel.connect(timeout=60.0, reconnect=False
		self._start_next_track_event.clear()
        if self.bot.voice.is_connected():
            await ctx.send(f'Joined {ctx.author.voice.channel.name}')

        else:
            await ctx.send('Connection unsuccessful')

        await ctx.message.delete()

	@commands.command(alias='disconnect')
	async def leave(self, ctx):
		self.bot.voice.disconnect()
		self.queue = []

    @commands.command()
    async def play(self, ctx, *, search):
        self.queue.append(search)
		self._start_next_track_event.clear()
		await self._play()
		await self._start_next_track_event.wait()

	async def _play(self, ctx):
        if self.bot.voice.is_connected():
            downloader = youtube_dl.YoutubeDL(YT_DL_OPTS)
            info = downloader.extract_info(self.queue.pop(0), download=False)

            if info.get('_type') == 'playlist':
                info = info['entries'][0]

            url = info['url']
            title = info.get('title')

            ffmpeg_player = discord.FFmpegPCMAudio(url)

            self.bot.voice.play(ffmpeg_player, after=lambda error: self._start_next_track_event.set())
            await ctx.send(f'Now Playing {title}')


    @commands.command()
    async def pause(self, ctx):
		if not self.bot.voice.is_paused() and self.bot.voice.is_playing():
        	await self.bot.voice.pause()
		else:
			await ctx.send('I am already paused...')

	@commands.command()
	async def resume(self, ctx):
		if self.bot.voice.is_paused():
			await self.bot.voice.resume()
		else:
			await ctx.send('I am not paused...')

	@commands.command()
	async def stop(self, ctx):
		if self.bot.voice.is_playing() and or self.bot.voice.is_paused():
			await self.bot.voice.stop()
			self.queue = []

	@commands.command(alias='list')
	async def queue(self, ctx):
		em = discord.Embed(name='Queue', colour)
		for i in self.queue:
			em.add_field(name=self.queue.index(i), value=i)

	@commands.command()
	async def skip(self, ctx):
		self._start_next_track_event.set()

def setup(bot):
    bot.add_cog(Music(bot))
