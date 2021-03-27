import requests
import json
import re
from bs4 import BeautifulSoup


def parse_animal_products(name):
    print("Parsing animal product {}".format(name))
    url = "https://www.stardewvalleywiki.com/{}".format(name)
    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')

    data = {}

    infotables = soup.find_all(id="infoboxtable")
    if len(infotables) == 0:
        print("Failed to read {}".format(name))
        return
    infobox = infotables[0]
    name = infobox.find(id="infoboxheader").text.strip()
    data["name"] = name
    data["id"] = ''.join(e for e in name.replace(" ", "_") if (e.isalnum() or e == "_")).lower()
    data["image_url"] = "https://www.stardewvalleywiki.com{}".format(infobox.find("img")["src"])
    data["wiki_url"] = url
    data["description"] = infobox.find("span").text.strip()

    for row in infobox.find_all("tr"):
        if row.find("td").text.strip() == "Source:":
            data["sources"] = list(map(lambda a: a.strip(), row.find_all("td")[-1].text.strip().split(" • ")))
        if row.find("td").text.strip() == "Season:":
            data["season"] = list(map(lambda a: a.strip(), row.find_all("td")[-1].text.strip().split(" • ")))

        if row.find("td").text.strip() == "Healing Effect":
            cols = row.find_next_sibling("tr").find_all("table")
            data["energy"] = list(filter(lambda a: a != "Energy", cols[0].stripped_strings))
            data["health"] = list(filter(lambda a: a != "Health", cols[1].stripped_strings))

        if row.find("td").text.strip() == "Sell Price:":
            data["prices"] = list(map(lambda a: a[:-1], row.find_all("td")[-1].stripped_strings))
        
        if row.find("td").text.strip() == "Sell Prices":
            prices = row.find_next_sibling("tr").find_next_sibling("tr").find("table").stripped_strings
            data["prices"] = list(map(lambda a: a[:-1], prices))

    tables = soup.find_all("table", "wikitable")
    for table in tables:
        if table.find("th").text.strip() == "Villager Reactions":
            villager_reactions = table
        if table.find_previous_sibling("h2").text.strip() == "Artisan Goods":
            usedIn = []
            for row in table.find_all("tr"):
                if len(row.find_all("td")) > 2:
                    usedIn.append(row.find_all("td")[1].text.strip())
            data["used_in"] = usedIn

    gifts = {}
    for row in villager_reactions.find_all("tr"):
        reaction = row.find("th").text.strip().lower()
        if reaction == "villager reactions":
            continue
        villagers = row.find("td")
        if villagers is not None:
            gifts[reaction] = list(map(lambda a: a.strip(), villagers.text.strip().split(' • ')))

    data["gifts"] = gifts

    return data

animal_products = ["Egg","Large_Egg","Dinosaur_Egg","Duck_Egg","Duck_Feather","Golden_Egg","Wool","Rabbit's_Foot","Void_Egg","Milk","Large_Milk","Goat_Milk","Large_Goat_Milk","Wool","Ostrich_Egg","Truffle","Roe","Slime","Slime_Egg"]

data = list(map(lambda a: parse_animal_products(a), animal_products))

with open("../data/animal-products.json", "w") as f:
    f.write(json.dumps(data))

