import aiohttp.web as web
import aiohttp
from redbot.core import commands

class MusicCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession(loop=bot.loop)
        self.queue = []
        self.current_song = None
        
    async def create_webpage(self):
        async def handle(request):
            current_song = self.current_song
            queue = "\n".join(self.queue)
            html = f"<html><body>Current Song: {current_song} <br>Queue: {queue}</body></html>"
            return web.Response(text=html, content_type="text/html")
            
    @commands.command()
    async def play(self, ctx, song_name: str):
        self.current_song = song_name
        await ctx.send(f"Now Playing: {song_name}")
    
    @commands.command()
    async def queue(self, ctx, song_name: str):
        self.queue.append(song_name)
        await ctx.send(f"{song_name} added to the queue")
        
    @commands.command()
    async def webpage(self, ctx):
        app = web.Application()
        app.router.add_get("/", handle)
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, "localhost", 8080)
        await site.start()
        await ctx.send("Webpage running on localhost:8080")

    def cog_unload(self):
        self.session.close()
