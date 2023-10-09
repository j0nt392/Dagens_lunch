import discord
import responses
import os

async def send_message(message, user_message, is_private):
    try:
        response = responses.handle_response(user_message)
        print(f"Response: {response}")  # Add this line for debugging
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(f"error is {e}")


def run_discord_bot():
    TOKEN = 'MTE1OTQzMzAyOTA1NjQ3OTI1Mw.GkjguZ.z-ZHl-X4Jhm8My4wq54-HP9i0MAQSbIrGuQKiA'
    intents = discord.Intents.default()
    intents.message_content = True
    intents.messages = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f'{client.user} is now running')
    
    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        username = str(message.author)
        user_message = str(message.content)  # Convert to lowercase and remove leading/trailing spaces
        channel = str(message.channel)
        
        print(f"{username}said {user_message} in {channel}")
        
        # Check for the command prefix without the '?'
        if user_message[0] == "?":
            user_message = user_message[1:]        
            await send_message(message, user_message, is_private=True)
        else:
            await send_message(message, user_message, is_private=False)
        

    client.run(TOKEN)
