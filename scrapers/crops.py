import requests
import json
import re
from bs4 import BeautifulSoup


def parse_crops(name):
    print("Parsing crop {}".format(name))
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
        if row.find("td").text.strip() == "Growth Time:":
            growth = row.find_all("td")[-1].text.strip()
            data["growth_time"] = re.match(r'\d+', growth).group()

        if row.find("td").text.strip() == "Season:":
            data["season"] = list(map(lambda a: a.strip(), row.find_all("td")[-1].text.strip().split(" • ")))

        if row.find("td").text.strip() == "XP:":
            xp = row.find_all("td")[-1].text.strip()
            data["xp"] = re.search(r'\d+', xp).group()[-1]

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
        if table.find("th").text.strip() == "Stage 1":
            last_row = table.find_all("tr")[-1]
            cell = last_row.find_all("td")[-1].text.strip()
            if "Regrowth" in cell:
                data["regrowth_time"] = re.search(r'\d+', cell).group()[-1]
                print(data["regrowth_time"])

        if table.find("th").text.strip() == "Villager Reactions":
            villager_reactions = table
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

# NOTE grape is a crop, not a foragable
crops = {"Blue_Jazz","Cauliflower","Coffee_Bean","Garlic","Green_Bean","Kale","Parsnip","Potato","Rhubarb","Strawberry","Tulip","Unmilled_Rice",
"Blueberry","Coffee_Bean","Corn","Hops","Hot_Pepper","Melon","Poppy","Radish","Red_Cabbage","Starfruit","Summer_Spangle","Sunflower","Tomato","Wheat",
"Amaranth","Artichoke","Beet","Bok_Choy","Corn","Cranberries","Eggplant","Fairy_Rose","Grape","Pumpkin","Sunflower","Wheat","Yam",
"Ancient_Fruit","Cactus_Fruit","Pineapple","Qi_Fruit","Sweet_Gem_Berry","Taro_Root","Tea_Leaves"}


data = list(map(lambda a: parse_crops(a), crops))

with open("../data/crops.json", "w") as f:
    f.write(json.dumps(data))