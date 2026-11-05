import os
import discord
from discord.ext import commands
from discord.ui import Select, View, Button
from flask import Flask
from threading import Thread

# 1. Setup Flask (24/7 Keep Alive)
app = Flask('')

@app.route('/')
def home():
    return "Bot is online and running 24/7!"

def run():
    app.run(host='0.0.0.0', port=8081)

def keep_alive():
    t = Thread(target=run)
    t.start()

# 2. Setup Discord Bot
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

SUPPORT_ROLE_ID = 123456789012345678  # ⚠️ Badalha b ID d Support f s-server dyalk
# 🚨 L-image l-jdida lli sifti duba
GIF_BANNER_URL = "https://i.postimg.cc/RZtGH1VG/Gemini-Generated-Image-admzaradmzaradmz.jpg"

class TicketSelect(Select):
    def __init__(self):
        options = [
            discord.SelectOption(
                label="Report Ticket", 
                description="For Reports Our B.T.D Members", 
                emoji="🚨", 
                value="report"
            ),
            discord.SelectOption(
                label="Help Ticket", 
                description="For Any Help Click Here", 
                emoji="🎫", 
                value="help"
            )
        ]
        super().__init__(placeholder="⚡ [B.T.D] Click Here To Open A Ticket", min_values=1, max_values=1, options=options, custom_id="ticket_select_menu")

    async def callback(self, interaction: discord.Interaction):
        guild = interaction.guild
        user = interaction.user
        ticket_type = self.values[0]

        channel_name = f"report-{user.name}" if ticket_type == "report" else f"help-{user.name}"

        existing_channel = discord.utils.get(guild.channels, name=channel_name.lower())
        if existing_channel:
            await interaction.response.send_message(f"❌ You already have an open ticket: {existing_channel.mention}", ephemeral=True)
            return

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            user: discord.PermissionOverwrite(read_messages=True, send_messages=True, attach_files=True),
            guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True, manage_channels=True)
        }

        support_role = guild.get_role(SUPPORT_ROLE_ID)
        if support_role:
            overwrites[support_role] = discord.PermissionOverwrite(read_messages=True, send_messages=True)

        channel = await guild.create_text_channel(
            name=channel_name,
            overwrites=overwrites,
            reason=f"Ticket ({ticket_type}) created by {user}"
        )

        embed = discord.Embed(
            title=f"🚨 [B.T.D] {ticket_type.capitalize()} Ticket - {user.name}",
            description="Welcome to B.T.D Support! Explain your issue clearly, and our crew will assist you shortly.",
            color=discord.Color.red() if ticket_type == "report" else discord.Color.green()
        )
        embed.set_thumbnail(url=user.display_avatar.url)

        await channel.send(content=f"{user.mention} | {support_role.mention if support_role else ''}", embed=embed, view=TicketControlView())
        await interaction.response.send_message(f"✅ Your ticket has been created: {channel.mention}", ephemeral=True)

class TicketView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(TicketSelect())

class TicketControlView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="🔒 Close Ticket", style=discord.ButtonStyle.danger, custom_id="close_ticket_btn")
    async def close_ticket(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_message("🔒 This ticket will be closed in 5 seconds...")
        import asyncio
        await asyncio.sleep(5)
        await interaction.channel.delete(reason="Ticket Closed")

    @discord.ui.button(label="🙋‍♂️ Claim Ticket", style=discord.ButtonStyle.secondary, custom_id="claim_ticket_btn")
    async def claim_ticket(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_message(f"📌 **{interaction.user.name}** has claimed this B.T.D ticket!")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    bot.add_view(TicketView())
    bot.add_view(TicketControlView())

@bot.command()
@commands.has_permissions(administrator=True)
async def setup_ticket(ctx):
    embed = discord.Embed(
        title=" BROTHERS TILL DEATH - OFFICIAL TICKET SYSTEM ",
        description="• **[+] # BTD 4LIFE**\n• **[+] Open a Ticket For Reports or Help**\n• **[+] B.T.D Gang - Stay Strong & Safe**",
        color=discord.Color.dark_red()
    )
    # Hna t-7tta l-image l-jdida dyalk b shkl nadi
    embed.set_image(url=GIF_BANNER_URL)
    embed.set_footer(text="B.T.D Security System • Powered 24/7")
    
    await ctx.send(embed=embed, view=TicketView())
    await ctx.message.delete()

if __name__ == "__main__":
    keep_alive() 
    bot.run("MTUzNjEyNTYxMDg4MjEwOTUxMA.GZWfk5.Hppg86pTQeaImLRkTUIipBOa3aYIVjt4GOq1jU")