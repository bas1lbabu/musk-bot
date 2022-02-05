import os
from discord.ext import commands
import discord
import random
from discord_verify import verify_user


class g_r_mod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.role_name=os.environ["ROLE_NAME"]
        self.mod_role=os.environ["MOD_ROLE"]
        self.v_channel_id=os.environ["V_CHANNEL_ID"]

    @commands.Cog.listener()
    # on ready function to display login :)
    async def on_ready(self):
        print(f"logged in as :: >> {self.bot.user.name}")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        # welcomes new users to server :)
        channel = member.guild.system_channel
        cvalue = random.randint(0, 0xffffff)
        embed = discord.Embed(
            description=f"Welcome {member.name} :)", color=cvalue)
        await channel.send(embed=embed)
        if verify_user(str(member.id)):
            await self.assign_role(guild=member.guild, author=member)
        else:
            await member.channel.send(f"Id of {member.name} not found in database")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            pass
            # await ctx.send("Command not found!")

    @commands.command()
    async def verify(self, ctx):
        if str(ctx.channel.id)!=str(self.v_channel_id):
            return
        role = discord.utils.get(ctx.guild.roles, name=self.role_name)
        if role not in ctx.message.author.roles:
            if verify_user(str(ctx.message.author.id)):
                guild = ctx.guild
                author = ctx.message.author
                await self.assign_role(guild, author)
                await ctx.send(f"{author.name} is verified successfully.")
            else:
                await ctx.send(f"Unable to verify.Ping the mods `@{self.mod_role}` for more info.")
        else:
            await ctx.send("User already verified")

    async def assign_role(self, guild, author):
        if not discord.utils.get(guild.roles, name=self.role_name):
            # print(f"created role {self.role_name}\n")
            cvalue = random.randint(0, 0xffffff)
            await guild.create_role(name=self.role_name, color=cvalue)
        # else:
            # print(f"role {self.role_name} exists")
        role = discord.utils.get(guild.roles, name=self.role_name)
        if not role in author.roles:
            try:
                await author.add_roles(role)
            except Exception as err:
                print(err)


def setup(bot):
    bot.add_cog(g_r_mod(bot))
