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
		
	if message.content.startswith("https://discord.com/channels/900302240559018015/") == True:
		try:
			response = "-**---** **Content** **in** **the** **link** **above** **---**- \n\n"
			link = message.content.split('/')
			sourceServer = client.get_guild(int(link[4]))
			sourceChannel = sourceServer.get_channel(int(link[5]))
			sourceMessage = await sourceChannel.fetch_message(int(link[6]))
			await message.channel.send(response + sourceMessage.content)
		except:
			await message.channel.send("-**Cannot** **preview**-\n-**I** **have** **no** **access** **to** **this** **channel.**-")

	
	
	
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
