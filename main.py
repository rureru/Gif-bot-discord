import discord
from discord.ext import commands
import random
import requests
from translate import Translator

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)
GIPHY_API_KEY = 'YOUR_GIPHY_APİ'  # Replace with Giphy API key


@bot.event
async def on_ready():
    print(f"{bot.user.name} opened now...")


@bot.command(name='gif')
async def gif(ctx, *args):
    member = ctx.author.name
    search_query = ' '.join(args) if args else 'trending'

    try:
        translator = Translator.translate(to_lang="en")
        en_searchq = translator.translate(search_query)  # Translate the written word in "en" format

        # Offset is used to get a different result in each call
        offset = random.randint(0, 100)  # Choose a random offset value

        endpoint = f'https://api.giphy.com/v1/gifs/search?api_key={GIPHY_API_KEY}&q={en_searchq}&limit=1&offset={offset}'
        response = requests.get(endpoint)
        data = response.json()

        if 'data' not in data or not data['data']:
            await ctx.send(
                f"{member} sorry but '{search_query.capitalize()}' not found")
            return

        gif_url = data['data'][0]['images']['original']['url']

        embed = discord.Embed(title=f"{member}, this is it {en_searchq}", color=0x00ff00)
        embed.set_image(url=gif_url)

        await ctx.send(embed=embed)
    # generate error code for any error
    except Exception as e:
        print(f'Error: {e}')


bot.run('YOUR_BOT_TOKEN')  # exchange with your bot token
