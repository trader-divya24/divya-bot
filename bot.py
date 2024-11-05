import nextcord
from nextcord import Interaction
from nextcord.ext import commands, tasks
from datetime import datetime
import random
import os

testServerId = 1

intents = nextcord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix="dv ", intents=intents)


@bot.event
async def on_ready():
    """Event triggered when the bot is ready and connected"""
    print(f'{bot.user.name} has connected to Discord!')
    print('Connected to the following guilds:')
    for guild in bot.guilds:
        print(f'- {guild.name} (id: {guild.id})')


@bot.slash_command(name='test', guild_ids=[testServerId])
async def test(interaction: Interaction):
    await interaction.response.send_message("Hello, subscriber :)")


@bot.slash_command(name='echo', guild_ids=[testServerId])
async def echo(interaction: Interaction, *, message):
    """Repeats whatever the user says. Usage: !echo [message]"""
    await interaction.response.send_message(f'You said: {message}')


@bot.slash_command(name='basic_embed', guild_ids=[testServerId])
async def basic_embed(ctx):
    """Sends a basic embed message"""
    embed = nextcord.Embed(
        title="Basic Embed",
        description="This is a simple embed message",
        color=nextcord.Color.blue()
    )
    await ctx.send(embed=embed)


@bot.slash_command(name='full_embed', guild_ids=[testServerId])
async def full_embed(ctx):
    """Sends an embed with all common features"""
    embed = nextcord.Embed(
        title="📘 Complete Embed Example",
        description="This embed shows all common features",
        color=nextcord.Color.gold(),
        url="https://discord.com",
        timestamp=datetime.now()
    )

    print(ctx.user)
    print(type(ctx.user))
    print(dir(ctx.user))

    mem = ctx.user

    # Add author info
    embed.set_author(
        name=mem.name,
        icon_url=mem.avatar.url if mem.avatar else None
    )

    # Add fields
    embed.add_field(name="Regular Field", value="This is a regular field", inline=True)
    embed.add_field(name="Inline Field", value="This appears inline", inline=True)
    embed.add_field(name="Inline Field 2", value="This also appears inline", inline=True)
    embed.add_field(name="Non-inline Field", value="This appears on its own line", inline=False)

    # Add footer
    embed.set_footer(text=f"Requested by {mem.name}", icon_url=mem.avatar.url if mem.avatar else None)

    # Add thumbnail
    embed.set_thumbnail(url="https://satviknewz.com/wp-content/uploads/2024/08/fii-dii.jpg")

    # Add image
    embed.set_image(url="https://example.com/image.png")

    await ctx.send(embed=embed)


@bot.slash_command(name='profile_card', guild_ids=[testServerId])
async def profile_card(ctx, member: nextcord.Member = None):
    """Creates a profile card for a user"""
    member = member or ctx.user

    roles = [role.name for role in member.roles if role.name != "@everyone"]

    embed = nextcord.Embed(
        title=f"Profile Card - {member.name}",
        color=member.color,
        timestamp=datetime.now()
    )

    embed.set_thumbnail(url=member.avatar.url if member.avatar else None)

    embed.add_field(name="ID", value=member.id, inline=True)
    embed.add_field(name="Nickname", value=member.nick if member.nick else "None", inline=True)
    embed.add_field(name="Account Created", value=member.created_at.strftime("%Y-%m-%d"), inline=True)
    embed.add_field(name="Joined Server", value=member.joined_at.strftime("%Y-%m-%d"), inline=True)
    embed.add_field(name="Roles", value=", ".join(roles) if roles else "No roles", inline=False)

    await ctx.send(embed=embed)


@tasks.loop(minutes=1)
async def send_random_message():
    """Send a random message every hour"""
    try:
        channel = bot.get_channel(1294150994137059450)
        if channel:
            # Get time-appropriate messages and select one randomly
            current_messages = [
                "Remember to stay hydrated! 💧",
                "Time for a quick stretch break! 🧘‍♂️",
                "Don't forget to check your posture! 🪑",
                "Take a moment to rest your eyes! 👀",
                "Random fact: The shortest war in history lasted 38 minutes! 🎭",
                "Fun reminder: You're awesome! Keep it up! ⭐",
                "Time check! How's your day going? 🕒",
                "Remember to take deep breaths! 🌬️",
                "Pro tip: Back up your important files! 💾",
                "Random joke: Why don't programmers like nature? It has too many bugs! 🐛"
            ]
            message = random.choice(current_messages)

            # Add current time to the message
            current_time = datetime.now().strftime("%H:%M")
            formatted_message = f"🕒 **{current_time}**\n{message}"

            await channel.send(formatted_message)
    except Exception as e:
        print(f"Error sending message: {e}")


if __name__ == '__main__':
    # Run the bot with the token
    bot.run(os.environ["DISCORD_TOKEN"])
