import discord
import responses

async def send_message(message, user_message, is_private):
    try:
        response = responses.handle_response(user_message)
        print(f"Response: {response}")  # Add this line for debugging
        if response:
            await message.author.send(response) if is_private else await message.channel.send(response)
            print("Message sent successfully")  # Add this line for debugging
    except Exception as e:
        print(e)


def run_discord_bot():
    TOKEN = 'MTE1OTE0MTg0Mjk0ODk4OTAzOA.GArfNk.rL3Bo5kR3CJELYyTwaHb51QUT6kTO9q4M_QnJ0'
    client = discord.Client(intents=discord.Intents.default())

    @client.event
    async def on_ready():
        print(f'{client.user} is now running')
    
    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        user_message = message.content.lower().strip()  # Convert to lowercase and remove leading/trailing spaces

        print(user_message)
        
        # Check for the command prefix without the '?'
        if user_message.startswith('dagenslunch'):
            response = responses.handle_response(user_message)
            if response:
                await send_message(message, response, is_private=True)
        elif user_message.startswith('?dagenslunch'):
            response = responses.handle_response(user_message)
            if response:
                await send_message(message, response, is_private=True)
        else:
            await send_message(message, user_message, is_private=False)

    client.run(TOKEN)
