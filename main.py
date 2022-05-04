from functools import partial
from flask import Flask
import threading
import BotFuncs
import discord
import os
import datetime

#----------------------------# Flask bot heartbeat. Keep Zorak alive.
client = discord.Client() 
app = Flask(__name__)
@app.route('/')
def index():
	return "Wow, such bot, so up."
partial_run = partial(app.run, host="0.0.0.0", port=80, debug=False, use_reloader=False)

#----------------------------# Discord Bot main function. 
@client.event
async def on_ready():
	await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="you..."))
	print('{0.user}, ready to conquer the world.'.format(client))


#-----------------------------#  Administrator Bot commands.
@client.event
async def on_message(message):
	if message.content.startswith('!echo') == True:
		if message.author.guild_permissions.administrator == True:
			text = message.content.replace('!echo','')
			await message.channel.send(text)
			await message.delete()
		else:
			await message.channel.send('You are not my master.', reference=message)

	if message.content == ('!dailychallenge'):
		if message.author.guild_permissions.administrator == True:
			await message.channel.send(BotFuncs.DailyChallenge())
			BotFuncs.increaseDay()
		else:
			await message.channel.send('You are not my master.', reference=message)
	
	
#-----------------------------#  User Commands	
	if message.content == ('!hello'):
		await message.channel.send('Dont talk to me, Im being developed.', reference=message)

	if message.content == ('!catfact'):
		await message.channel.send(BotFuncs.catfact(),reference=message)
		
	if message.content == ('!dogfact'):
		await message.channel.send(BotFuncs.dogfact(),reference=message)
		
	if message.content == ('!quote'):
		await message.channel.send(BotFuncs.quote(),reference=message)
		   
	if message.content == ('!joke'):
		await message.channel.send(BotFuncs.joke(),reference=message)

	if message.content.startswith('!google') == True:
		MsgString = str(message.content)
		msg = 'Here, allow me to gooogle that one for you:\nhttps://letmegooglethat.com/?q=' + str(MsgString[8:].strip().replace(" ","+"))
		await message.channel.send(msg, reference=message)
		
	if message.content.startswith('!8ball') == True:
		await message.channel.send('🎱 - ' + BotFuncs.magik(),reference=message)
		
	if message.content == ('!fakeperson'):
		await message.channel.send(BotFuncs.fakePerson(),reference=message)
		
  if "https://discord.com/channels" in message.content:
    text = message.content
    l = text.replace(", ", " ").split(" ")
    key = "https://discord.com/channels/"
    for item in l:
        if key in item:
            try:
                lilink = l[l.index(item)]
                response = "-**---** **Content** **in** **the** **link** **above** **---**- \n\n"
                link = lilink.replace("https://discord.com/channels/", "").split("/")
                sourceServer = client.get_guild(int(link[0]))
                sourceChannel = sourceServer.get_channel(int(link[1]))
                sourceMessage = await sourceChannel.fetch_message(int(link[2]))

                if len(sourceMessage.content) <= 1000:
                    embed = discord.Embed(title=response, description="", timestamp=datetime.datetime.utcnow())
                    embed.add_field(name=f"Length: {len(sourceMessage.content)}", value=sourceMessage.content)
                    embed.set_footer(text=sourceMessage.author, icon_url=sourceMessage.author.avatar_url)
                    await message.channel.send(embed=embed)

                if len(sourceMessage.content) > 1000:
                    contents = sourceMessage.content
                    con2 = []
                    splitstr = math.ceil(len(contents) / 1000)
                    embed1 = discord.Embed(title=response, description="", timestamp=datetime.datetime.utcnow())
                    while contents:
                        con2.append(contents[:900])
                        contents = contents[900:]
                    for feilds in range(0, splitstr):
                        embed1.add_field(name="**---CUT---HERE---**", value=f"```py\n{con2[feilds]}\n```",
                                         inline=False)
                    embed1.set_footer(text=sourceMessage.author, icon_url=sourceMessage.author.avatar_url)
                    await message.channel.send(embed=embed1)

            except:

                await message.channel.send(f"         -**Cannot** **preview**-\n-"
                                           f"**Make sure message is in this server,"
                                           f" and not a text file or image**-")

	
	
	
	if message.content.startswith('!embed') == True:
		text = message.content
		text = text.replace('!embed', '').replace("title= ", '').replace("message= ", '')
		u_m = text.split(", ")
		embed = discord.Embed(title=u_m[0], description="", timestamp=datetime.datetime.utcnow())
		embed.add_field(name=u_m[1], value=":slight_smile:")
		await message.channel.send(embed=embed)
		await message.delete()

	if message.content == "dm":
		await message.channel.send("Dming user")
		dm = await message.author.create_dm()  # Creates a dm channel with the user
		await dm.send("What you want to send")




if __name__ == "__main__":
	t1 = threading.Thread(target=partial_run)
	t1.start()
	client.run(os.environ['TOKEN'])
