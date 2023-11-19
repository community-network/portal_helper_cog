"""Commands for the cog"""
import re
import random
import discord
from discord import app_commands
from typing import List
from rapidfuzz import fuzz
from . import shared
from .utils.github_api import DataHandler, CleanDoc

dh = DataHandler()
dh.load_data()


async def autocomplete_blocks(
    interaction: discord.Interaction, current: str
) -> list[app_commands.Choice[str]]:
    """For discord.py"""
    return await get_autocomplete_blocks(interaction, current)


async def get_autocomplete_blocks(
    _interaction: discord.Interaction, current: str, closest_match: bool = False
) -> list[app_commands.Choice[str]]:
    """
    Returns a list of 25 elements, sorted by highest fuzz.ratio.

    :param ctx: block name
    :param closest_match: only Returns the closest match
    :return: list
    """
    ratio_list = [
        (i, fuzz.partial_ratio((current if closest_match else current), i))
        for i in dh.docs_dict.keys()
    ]
    blocks = [
        app_commands.Choice(name=i[0], value=i[0])
        for i in sorted(ratio_list, key=lambda x: x[1], reverse=True)
    ][0 : (1 if closest_match else 25)]
    if closest_match:
        return blocks[0]
    return blocks


class RuleBlockPages:
    def __init__(self, clean_doc: CleanDoc):

        self.event_groups = [
            "Rule",
            "OnGoing",
            "OnPlayer",
            "OnCapture",
            "OnMCOM",
            "OnGameMode",
            "OnVehicle",
        ]
        self.options = {"Description": ""}
        summary = clean_doc["summary"][220:]
        re_groups = list(re.finditer(r"^\*\*.*\*\*$", summary, flags=re.MULTILINE))
        re_groups_len = len(re_groups)
        for index, event in enumerate(re_groups):
            if index != re_groups_len - 1:
                desc = summary[event.end() : re_groups[index + 1].start() - 1]
            else:
                desc = summary[event.end() :]
            self.options[event.group().replace("*", "")] = desc

        self.pages = [
            discord.Embed(title="Rule", description=clean_doc["summary"][0:184]),
            discord.Embed(title="OnGoing Events", description=self.options["Ongoing"]),
        ]
        self.pages[0].set_image(
            url="https://raw.githubusercontent.com/battlefield-portal-community/Image-CDN/main/portal_blocks/Rule.png"
        )

        for event in self.event_groups[2:]:
            embed = discord.Embed(title=f"{event.replace('On','', 1)} Events")
            [
                embed.add_field(name=local_event, value=value, inline=False)
                for local_event, value in self.options.items()
                if local_event.startswith(event)
            ]
            if event == "OnPlayer":
                for _ in ["OnMandown", "OnRevived"]:
                    embed.add_field(name=_, value=self.options[_], inline=False)
            self.pages.append(embed)


# async def rule_block_pagination(ctx: discord.ApplicationContext):
#     rule_block_pages = RuleBlockPages(dh.get_doc("Rule"))
#     page_groups = [
#         pages.PageGroup(
#             pages=[page],
#             label=f"{option} Events",
#         ) for option, page in zip(rule_block_pages.event_groups, rule_block_pages.pages)
#     ]
#     paginator = pages.Paginator(
#         pages=page_groups,
#         show_menu=True,
#         menu_placeholder="Choose Event Type",
#         show_disabled=False,
#         show_indicator=False,
#         timeout=None,
#     )
#     await paginator.respond(ctx.interaction, ephemeral=False)


def make_bold(text):
    """Discord bot text"""
    content_final = ""
    for word in text.split(" "):
        if word.isupper():
            content_final += f"**{word}** "
        else:
            content_final += f"{word} "
    return content_final


def make_embed(block_name: str) -> discord.Embed:
    """
    Parses data returned by GitHub Api and returns an embed
    :param block_name: str
    :return: discord.Embed
    """
    image_url = f"https://raw.githubusercontent.com/battlefield-portal-community/Image-CDN/main/portal_blocks/{block_name}.png"
    if block_name == "all":
        # todo: Show Complete list of all blocks
        raise NotImplementedError("command to get all blocks not implemented yet")
        # return special_embeds("all")
    elif block_name in dh.docs_dict.keys():
        doc = dh.get_doc(str(block_name))
    else:
        closet_match = get_autocomplete_blocks(block_name, closest_match=True)
        if closet_match != "rule":
            doc = dh.get_doc(closet_match)
        else:
            raise ValueError(f"Unknown Block {block_name}")

    embed_fields = []
    if "inputs" in doc.keys():
        embed_fields.append(
            {"name": "Inputs", "value": "\n".join(doc["inputs"]), "inline": False}
        )
    if "output" in doc.keys():
        embed_fields.append({"name": "Output", "value": "\n".join(doc["output"])})
    embed = discord.Embed(
        title=doc["block"],
        url=f"https://docs.bfportal.gg/docs/blocks/{doc['block']}",
        description=doc["summary"],
        color=random.choice(shared.COLORS),
    )
    for field in embed_fields:
        embed.add_field(**field)
    embed.set_image(url=image_url)
    return embed


async def docs(interaction: discord.Interaction, block_name):
    """Get doc of block"""
    try:
        embed = make_embed(block_name)
        await interaction.followup.send(embed=embed)
    except NotImplementedError as e:
        print(e)
        await interaction.followup.send(
            embed=discord.Embed(
                title="Not Yet Implemented",
                description=f"Command {block_name}",
                color=int("ff0000", 16),
            ),
        )
    except BaseException as e:
        print(
            f"Error {e} with {block_name} {autocomplete_blocks(block_name, closest_match=True)}"
        )
        await interaction.followup.send(
            embed=discord.Embed(
                title=f"Error getting docs for {block_name}",
                description="\u200b",
                color=int("ff0000", 16),
            )
        )
    except ValueError as e:
        print(e)
        await interaction.followup.send(
            embed=discord.Embed(
                title=f"Error getting docs for {block_name}",
                description="\u200b",
                color=int("ff0000", 16),
            )
        )
