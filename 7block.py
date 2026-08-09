import discord
from discord.ext import commands
from keep_alive import keep_alive

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# قائمة الأزرار لأنواع التذاكر (الدعم والتقارير)
class TicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="الدعم الفني (Support)", style=discord.ButtonStyle.primary, custom_id="support_ticket")
    async def support_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.create_ticket(interaction, "support")

    @discord.ui.button(label="التقارير (Report)", style=discord.ButtonStyle.danger, custom_id="report_ticket")
    async def report_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.create_ticket(interaction, "report")

    async def create_ticket(self, interaction: discord.Interaction, ticket_type: str):
        guild = interaction.guild
        category_name = "الدعم الفني" if ticket_type == "support" else "التقارير"
        
        # البحث عن القسم أو إنشاؤه تلقائياً
        category = discord.utils.get(guild.categories, name=category_name)
        if not category:
            category = await guild.create_category(category_name)

        # منع الأعضاء الآخرين من رؤية التذكرة لحماية الخصوصية
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            interaction.user: discord.PermissionOverwrite(view_channel=True, send_messages=True),
            guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True)
        }

        channel = await guild.create_text_channel(
            f"{ticket_type}-{interaction.user.name}",
            category=category,
            overwrites=overwrites
        )

        await interaction.response.send_message(f"تم إنشاء تذكرتك بنجاح: {channel.mention}", ephemeral=True)
        await channel.send(f"مرحباً {interaction.user.mention}! تم فتح تذكرة {ticket_type}. الرجاء كتابة تفاصيل مشكلتك وسيرد عليك الفريق قريباً.")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

# أمر لإرسال لوحة الأزرار في أي روم (!ticket)
@bot.command()
@commands.has_permissions(administrator=True)
async def ticket(ctx):
    view = TicketView()
    await ctx.send("اختر نوع التذكرة التي ترغب في فتحها:", view=view)

if __name__ == "__main__":
    keep_alive()  # للحفاظ على البوت شغّالاً
    bot.run("MTUzNjEyNTYxMDg4MjEwOTUxMA.GSqQUt.uo5VODIfLZD65hs756oWSvGaWlZbUtKN34b6RQ")  # <--- حط التوكن ديالك هنا بين العلامتين