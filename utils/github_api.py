import json
import re
from pathlib import Path
from typing import TypedDict, Optional
from requests import get
import logging


class CleanDoc(TypedDict):
    block: str
    summary: str
    inputs: list | None
    output: list | None


class DataHandler:
    def __init__(self, update: bool = True):
        self.logger = logging.getLogger("portal_helper_cog")
        self.github_endpoint = (
            "https://api.github.com/repos/battlefield-portal-community"
            "/portal-docs/contents/generators/blocks_json/docs_json"
        )
        self.local_file_path = Path(__file__).parents[1] / "data/blocks_info"
        self.cache = dict()
        Path(self.local_file_path).parent.mkdir(exist_ok=True)
        Path(self.local_file_path).touch(exist_ok=True)
        self.docs_dict = dict()
        if update:
            self.update_data()

    def update_data(self):
        self.logger.info("Updating GitHub data")
        github_content_json = get(self.github_endpoint).json()
        for item in github_content_json:
            if item["name"] == ".gitignore":
                continue
            self.docs_dict[Path(item["name"]).stem] = item["download_url"]

        with open(self.local_file_path, "w") as FILE:
            json.dump(self.docs_dict, FILE)
        self.cache.clear()
        self.logger.info("Updating GitHub Complete")

    def load_data(self):
        self.logger.info("Loading GitHub Data")
        with open(self.local_file_path) as FILE:
            tmp = FILE.read()
        try:
            json_data = json.loads(tmp)
        except json.JSONDecodeError:
            raise

        self.docs_dict = json_data
        self.logger.info("Loading GitHub Data Complete")

    def get_doc(self, target: str) -> CleanDoc:
        if target not in self.docs_dict.keys():
            raise ValueError("Specified Block not found")

        if target not in self.cache.keys():
            self.logger.info(f"cache miss:- {target}")
            url = self.docs_dict[target]
            data = get(url)
            if data.status_code != 200:
                raise ValueError(f"Unable to get {target} from github, api url {url}")
            self.cache[target] = json.loads(data.text)

        return self.cache[target]


if __name__ == "__main__":
    dh = DataHandler(update=False)
    dh.load_data()
    doc = dh.get_doc("Rule")["summary"][220:]
    f = list(re.finditer(r"^\*\*.*\*\*$", doc, flags=re.MULTILINE))
    for index, match in enumerate(f):
        self.logger.info(index, match.group())
