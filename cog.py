import discord
from discord.ext import commands
from discord import app_commands

from . import tool_list, command_docs

class Battlefield_2042(commands.GroupCog, name="bf2042"):
    """Battlefield 2042 public tools"""
    
    def __init__(self, bot: commands.AutoShardedBot):
        self.bot = bot
        super().__init__()
        
        
        
    @app_commands.command(name="tools", description="Shows a list of tools made by the Battlefield community.")
    async def tools(self, interaction: discord.Interaction) -> None:
        await interaction.response.defer()
        await tool_list.portalTools(interaction)

    @tools.error
    async def tools_error(self, interaction: discord.Interaction, error) -> None:
        embed = discord.Embed(color=0xe74c3c, description=f"Failed to get list of tools")
        await interaction.followup.send(embed=embed)



    @app_commands.command(name="portal", description="Returns the documentation of a block used in portal's rule editor.")
    @app_commands.describe(block_name="Name of the block")
    @app_commands.autocomplete(block_name=command_docs.autocomplete_blocks)
    async def portal(self, interaction: discord.Interaction, block_name: str) -> None:
        await interaction.response.defer()
        await command_docs.docs(interaction, block_name)

    @portal.error
    async def portal_error(self, interaction: discord.Interaction, error) -> None:
        embed = discord.Embed(color=0xe74c3c, description=f"Failed to get block info")
        await interaction.followup.send(embed=embed)