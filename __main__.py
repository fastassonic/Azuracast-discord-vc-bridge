import discord
import os 
import io
from discord.ext import commands, tasks
import aiohttp
from dotenv import load_dotenv
from difflib import get_close_matches
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
IP=os.getenv("IP")
STATION=os.getenv("STATION")
PREFIX = os.getenv("PREFIX")
API_KEY = os.getenv("API_KEY")
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=PREFIX, intents=intents)
client = None

requestWithApiKey = {"api_key": API_KEY}
@bot.command()
async def join(ctx):
    global client
    voicechannel = ctx.author.voice.channel
    if not client:
        client = await voicechannel.connect()
        print(f"http://{IP}/listen/{STATION}/radio.mp3")
        rawstream = discord.FFmpegPCMAudio(f"http://{IP}/listen/{STATION}/radio.mp3")
        volumecorrected =  discord.PCMVolumeTransformer(rawstream, volume=1)
        client.play(volumecorrected)
    else:
        await client.move_to(voicechannel)



@bot.command()
async def disconnect(ctx):
    global client
    if not client:
        await ctx.send("Hey uh... I'm nowhere to be seen dude")
    else:
        await client.disconnect()
        client = None

@bot.command()
async def upnext(ctx):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"http://{IP}/api/nowplaying/{STATION}") as response:
            if response.status == 200:
                data = await response.json()  
                songdict = data["playing_next"]["song"]
                temp_embed = discord.Embed(title=songdict["title"], description=f"By {songdict["artist"]} \nFrom the album {songdict["album"]}")
                #This hack brought to you by the fact that I didn't want to expose the album art to the internet
                async with session.get(songdict["art"]) as artresponse:
                    image = await artresponse.read()
                discordimage = discord.File(io.BytesIO(image),filename="albumart.png")
                temp_embed.set_image(url="attachment://albumart.png")
                await ctx.send(embed = temp_embed, file=discordimage)
            else:
                await ctx.send("Failed to fetch data from the API.")
@bot.command()
async def currentsong(ctx):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"http://{IP}/api/nowplaying/{STATION}") as response:
            if response.status == 200:
                data = await response.json()
                songdict = data["now_playing"]["song"]
                temp_embed = discord.Embed(title=songdict["title"], description=f"By {songdict["artist"]} \nFrom the album {songdict["album"]}")
                #This hack brought to you by the fact that I didn't want to expose the album art to the internet
                async with session.get(songdict["art"]) as artresponse:
                    image = await artresponse.read()
                discordimage = discord.File(io.BytesIO(image),filename="albumart.png")
                temp_embed.set_image(url="attachment://albumart.png")
                await ctx.send(embed = temp_embed, file=discordimage)
            else:
                await ctx.send("Failed to fetch data from the API.")

@bot.command()
async def request(ctx,*, arg):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"http://{IP}/api/station/{STATION}/requests") as response:
            if response.status == 200:
                data = await response.json()
                currentsongnamelist = []
                print(data)
                for y in data: #This is apperently automatically turned into a list instead of a dict?    
                        currentsongnamelist.append(y["song"]["title"])

                if arg in currentsongnamelist:
                    index = currentsongnamelist.index(arg)
                    putstring = f"http://{IP}/api/station/{STATION}/request/"+data[index]["request_id"]
                    print(putstring)

                    async with session.post(putstring) as response2:
                        if response2.status == 200:
                            await ctx.send("Successfully Requested!: " + arg)
                        else:
                            await ctx.send("Failed to send request! Response was " + str(response2.status))
                else:
                    matches = get_close_matches(arg, currentsongnamelist, cutoff=0.4)
                    #This check brought to you by Honey B. Lovely and the fact my copy of bee my honey contained japanese characters in the name.
                    for i in currentsongnamelist: 
                        if arg in i:
                            matches.insert(0,i)
                    tempstring = f"Heya! I can't find anything named {arg}, could you perhaps be looking for any of these?\n"
                    for i in matches:
                        tempstring= tempstring +"* " + i + "\n"
                    if len(tempstring) >= 4000:
                        await ctx.send("Holy cow, dude that uh brought up alot of stuff. More then I can fit in a single message. Can you be more specific?")
                    else:
                        await ctx.send(tempstring)
            
                
            else:
                await ctx.send("Failed to fetch data from the API.")
    
    

    
    

@bot.command()
async def currentqueue(ctx):
    async with aiohttp.ClientSession() as session:
            print(f"http://{IP}/api/station/{STATION}/queue")
            async with session.get(f"http://{IP}/api/station/{STATION}/queue",params=requestWithApiKey) as response:
                print(response.status)
                if response.status == 200:
                    data = await response.json()
                    tempstring = ""
                    
                    for i in range(len(data)):
                        songdata = data[i]["song"]
                        tempstring= tempstring + f"{i+1}. {songdata["title"]} by {songdata["artist"]} \n" 
                        
                    temp_embed = discord.Embed(title="Queue!", description=tempstring)
                    await ctx.send(embed=temp_embed)
                        
                else:
                    await ctx.send("Failed to fetch data from the API.")



bot.run(TOKEN)


