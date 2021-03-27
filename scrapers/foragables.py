import requests
import json
from bs4 import BeautifulSoup


def parse_foragable(name):
    print("Parsing foragable {}".format(name))
    url = "https://www.stardewvalleywiki.com/{}".format(name)
    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')

    data = {}

    infotables = soup.find_all(id="infoboxtable")
    if len(infotables) == 0:
        print("Failed to read {}".format(fish))
        return
    infobox = infotables[0]
    name = infobox.find(id="infoboxheader").text.strip()
    data["name"] = name
    data["id"] = ''.join(e for e in name.replace(" ", "_") if (e.isalnum() or e == "_")).lower()
    data["image_url"] = "https://www.stardewvalleywiki.com{}".format(infobox.find("img")["src"])
    data["wiki_url"] = url
    data["description"] = infobox.find("span").text.strip()

    for row in infobox.find_all("tr"):
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
foragables = {"Sap","Common_Mushroom","Daffodil","Dandelion","Leek","Morel","Salmonberry","Spring_Onion","Wild_Horseradish","Fiddlehead_Fern","Red_Mushroom","Spice_Berry","Sweet_Pea","Blackberry","Chanterelle","Common_Mushroom","Hazelnut","Wild_Plum","Crocus","Crystal_Fruit","Holly","Snow_Yam","Winter_Root","Clam","Cockle","Coral","Mussel","Nautilus_Shell","Oyster","Rainbow_Shell","Sea_Urchin","Seaweed","Cave_Carrot","Purple_Mushroom","Red_Mushroom","Cactus_Fruit","Coconut","Dinosaur_Egg","Fiddlehead_Fern","Ginger","Magma_Cap"}
data = []
for fish in foragables:
    data.append(parse_foragable(fish))
with open("../data/foragables.json", "w") as f:
    f.write(json.dumps(data))

