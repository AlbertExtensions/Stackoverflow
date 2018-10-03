import time

from albertv0 import *
import json
import requests
from os import path


__iid__ = "PythonInterface/v0.1"
__prettyname__ = "Stackoverflow"
__version__ = "0.1"
__trigger__ = ".so "
__author__ = "Bharat kalluri"
__dependencies__ = ["requests"]

stackoverflow_api = "https://api.stackexchange.com/2.2/search/advanced?pagesize=20&order=desc&sort=relevance&q={}" \
                    "&site=stackoverflow"

icon_folder = "{}/icons/".format(path.dirname(__file__))
default_icon = "{}{}.png".format(icon_folder, "StackOverflow")
answered_icon = "{}{}.png".format(icon_folder, "answered")


def handleQuery(query):
    results = []

    if query.isTriggered and query.string.strip():

        # avoid rate limiting
        time.sleep(0.3)
        if not query.isValid:
            return

        item = Item(
            id=__prettyname__,
            icon=default_icon,
            completion=query.rawString,
            text=__prettyname__,
            actions=[]
        )

        if len(query.string) >= 4:
            try:
                api_url = stackoverflow_api.format(query.string)
                api_response = requests.get(api_url)
                json_response = json.loads(api_response.content)
                for question in json_response["items"]:
                    results.append(Item(
                        id=__prettyname__,
                        icon=answered_icon if question["is_answered"] else default_icon,
                        text=question["title"],
                        subtext="Tags: {}".format(",".join(question["tags"])),
                        actions=[UrlAction("Open in Stackoverflow", question["link"])])
                    )
                if len(results) == 0:
                    item.subtext = "No answers found on stackoverflow :("
                    return item
            except Exception as err:
                print(err)
                print("Troubleshoot internet connection")
                item.subtext = "Connection error"
                return item
        else:
            item.subtext = "Search in Stackoverflow!"
            return item
    return results
