"""The cog for bf2042 portal"""
import discord
from discord.ext import commands
from discord import app_commands

from . import tool_list, command_docs


class Battlefield_2042(commands.Cog, name="bf2042"):
    """Battlefield 2042 public tools"""

    def __init__(self, bot: commands.AutoShardedBot):
        self.bot = bot
        super().__init__()

    group = app_commands.Group(name="bf2042", description="Battlefield 2042 public tools cog")
    group.allowed_installs = app_commands.AppInstallationType(guild=True, user=True)
    
    @group.command(
        name="tools",
        description="Shows a list of tools made by the Battlefield community.",
    )
    async def tools(self, interaction: discord.Interaction) -> None:
        """Community tools"""
        await interaction.response.defer()
        await tool_list.portal_tools(interaction)

    @tools.error
    async def tools_error(self, interaction: discord.Interaction, _error) -> None:
        """Error handling"""
        embed = discord.Embed(color=0xE74C3C, description="Failed to get list of tools")
        await interaction.followup.send(embed=embed)

    @group.command(
        name="portal",
        description="Returns the documentation of a block used in portal's rule editor.",
    )
    @app_commands.describe(block_name="Name of the block")
    @app_commands.autocomplete(block_name=command_docs.autocomplete_blocks)
    async def portal(self, interaction: discord.Interaction, block_name: str) -> None:
        """Blocks docs"""
        await interaction.response.defer()
        await command_docs.docs(interaction, block_name)

    @portal.error
    async def portal_error(self, interaction: discord.Interaction, _error) -> None:
        """Error handling"""
        embed = discord.Embed(color=0xE74C3C, description="Failed to get block info")
        await interaction.followup.send(embed=embed)
