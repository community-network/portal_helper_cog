import random
import asyncio
from requests import get
import json
import discord
from discord import app_commands
from typing import List
from pathlib import Path
from rapidfuzz import fuzz
from . import shared

async def autocomplete_blocks(
        interaction: discord.Interaction,
        current: str
    ) -> List[app_commands.Choice[str]]:
        return await get_autocomplete_blocks(interaction, current)

async def get_autocomplete_blocks(
        interaction: discord.Interaction,
        current: str,
        closest_match: bool = False
    ) -> List[app_commands.Choice[str]]:
    """
    Returns a list of 25 elements, sorted by highest fuzz.ratio.
    :param ctx: block name
    :param closest_match: only Returns the closest match
    :return: list
    """
    ratio_list = [(i, fuzz.partial_ratio((current if closest_match else current), i)) for i in dh.docs_dict.keys()]
    blocks = [
        app_commands.Choice(name=i[0], value=i[0])
        for i in sorted(ratio_list, key=lambda x: x[1], reverse=True)
    ][0:(1 if closest_match else 25)]
    if closest_match:
        return blocks[0]
    return blocks
    

class DataHandler:
    def __init__(self, update: bool = True):
        self.github_endpoint = r"https://api.github.com/repos/battlefield-portal-community/portal-docs/contents/docs_json"
        self.local_file_path = Path(__file__).parents[1] / "data/blocks_info"
        Path(self.local_file_path).parent.mkdir(exist_ok=True)
        Path(self.local_file_path).touch(exist_ok=True)
        self.docs_dict = dict()
        if update:
            self.update_data()

    def update_data(self):
        print("Updating GitHub data")
        github_content_json = get(self.github_endpoint).json()
        for item in github_content_json:
            if item['name'] == ".gitignore":
                continue
            self.docs_dict[Path(item['name']).stem] = item['download_url']

        with open(self.local_file_path, 'w') as FILE:
            json.dump(self.docs_dict, FILE)
        print("Updating GitHub Complete")

    def load_data(self):
        print("Loading GitHub Data")
        with open(self.local_file_path) as FILE:
            tmp = FILE.read()
        try:
            json_data = json.loads(tmp)
        except json.JSONDecodeError:
            raise

        self.docs_dict = json_data
        print("Loading GitHub Data Complete")

    def get_doc(self, target: str):
        if target not in self.docs_dict.keys():
            raise ValueError("Specified Block not found")

        url = self.docs_dict[target]
        data = get(url)
        if data.status_code != 200:
            raise ValueError(f"Unable to get {target} from github, api url {url}")
        return json.loads(data.text)


dh = DataHandler()
dh.load_data()

if __name__ == "__main__":
    dh = DataHandler(update=True)
    dh.load_data()
    # dh.update_data()
    print(asyncio.run(autocomplete_blocks(None, "EnableCapturePointDeploying")))

def special_embeds(block_name):
    if block_name == "rule":
        doc_list = [i for i in dh.get_doc("rule").split("\n") if i != ""]

        fields_list = []
        for i in range(4, len(doc_list) - 1, 2):
            fields_list.append({
                "name": doc_list[i],
                "value": doc_list[i + 1],
                "inline": False
            })

        embed = discord.Embed(
            title=make_bold(doc_list[0]),
            url=f"https://docs.bfportal.gg/docs/blocks/{doc_list[0]}",
            description=doc_list[1] + f"\n**{doc_list[3]}**",
            color=random.choice(shared.COLORS),
        )
        for field in fields_list:
            embed.add_field(**field)
        return embed

    if block_name == "all":
        pass


def make_bold(text):
    content_final = ""
    for word in text.split(" "):
        if word.isupper():
            content_final += f"**{word}** "
        else:
            content_final += f"{word} "
    return content_final


def make_embed(block_name: str) -> discord.Embed:
    """
    Parses data returned by Github Api and returns an embed
    :param block_name: str
    :return: discord.Embed
    """
    img = 'Rule' if block_name.lower() == 'rule' else block_name
    image_url = f"https://raw.githubusercontent.com/battlefield-portal-community/Image-CDN/main/portal_blocks/{img}.png"
    if block_name == "all":
        # todo: Show Complete list of all blocks
        raise NotImplementedError("command to get all blocks not implemented yet")
        # return special_embeds("all")
    elif block_name == "rule":
        return special_embeds("rule")
    elif block_name in dh.docs_dict.keys():
        doc = dh.get_doc(str(block_name))
    else:
        closet_match = autocomplete_blocks(None, block_name, closest_match=True)
        if closet_match != "rule":
            doc = dh.get_doc(closet_match)
        else:
            return special_embeds("rule")

    embed_fields = []
    if 'inputs' in doc.keys():
        embed_fields.append({
            "name": "Inputs",
            "value": "\n".join(doc['inputs']),
            "inline": False
        })
    if 'output' in doc.keys():
        embed_fields.append({
            "name": "Output",
            "value": "\n".join(doc['output'])
        })
    embed = discord.Embed(
        title=doc['block'],
        url=f"https://docs.bfportal.gg/docs/blocks/{doc['block']}",
        description=doc['summary'],
        color=random.choice(shared.COLORS),
    )
    for field in embed_fields:
        embed.add_field(**field)
    embed.set_image(url=image_url)
    return embed


async def docs(interaction: discord.Interaction, block_name):
    try:
        embed = make_embed(block_name)
        await interaction.followup.send(embed=embed)
    except NotImplementedError as e:
        print(e)
        await interaction.followup.send(
            embed=discord.Embed(
                title="Not Yet Implemented",
                description=f"Command {block_name}",
                color=int("ff0000", 16)
            ),
        )
    except BaseException as e:
        print(f"Error {e} with {block_name} {autocomplete_blocks(block_name, closest_match=True)}")
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


