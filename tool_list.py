"""List of tools made by the community"""
import random
import discord
from . import shared


async def portal_tools(interaction: discord.Interaction):
    """List of tools discord return"""
    fields = [
        {
            "name": "BF2042-Portal-Extensions",
            "value": "Extension to add various QOL features to portal's logic editor",
            "url": "https://github.com/LennardF1989/BF2042-Portal-Extensions",
            "user_id": 182574451366428672,
        },
        {
            "name": "Portal-unleashed",
            "value": "Chrome extension allowing you to make your Portal Experience directly in "
            "pseudo-Javascript from a VSCode editor in your browser",
            "url": "https://github.com/Ludonope/BFPortalUnleashed",
            "user_id": 145955873913700352,
        },
        {
            "name": "Game Tools",
            "value": "Community Network aims to provide public tools for different games. Starting with Battlefield, "
            "we are bringing back online concurrent player stats, as well as personal stats and much more in"
            " future",
            "url": "https://gametools.network/",
            "user_id": 140391046822494208,
        },
        {
            "name": "2042 Compendium",
            "value": "A bot with a growing database of information about Weapons, Specialists, Maps, Eastereggs and more!",
            "url": "https://top.gg/bot/676103413355905045",
            "user_id": 599688337401577472,
        },
        {
            "name": "Battlefield Portal Blocks",
            "value": "A repository of some useful Portal Rule Editor Blocks",
            "url": "https://github.com/Andygmb/Battlefield-Portal-Blocks",
            "user_id": 152173878376923136,
        },
        {
            "name": "Portal Helper",
            "value": "This Bot which gives you access to various commands to help with portal",
            "url": "https://github.com/p0lygun/portal-docs-bot",
            "user_id": 338947895665360898,
        },
    ]
    thumbnail_url = (
        "https://cdn.discordapp.com/attachments/"
        "908104736455155762/912999248910495784/Animation_logo_discord.gif"
    )
    embed = discord.Embed(
        title="By the Community For the Community",
        url="https://bfportal.gg/",
        description="**A list of tools/resources made by the community**\n\n"
        + "\n\n".join(
            [
                f'**[{i["name"]}]({i["url"]})**\n{i["value"]}\nMaintained by <@{i["user_id"]}>'
                for i in fields
            ]
        ),
        color=random.choice(shared.COLORS),
    )
    embed.set_thumbnail(url=thumbnail_url)
    await interaction.followup.send(embed=embed)
