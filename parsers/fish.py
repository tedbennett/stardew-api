import requests
import json
from bs4 import BeautifulSoup


def parse_fish(name):
    print("Parsing fish {}".format(name))
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
        if row.find("td").text.strip() == "Found in:":
            data["location"] = list(map(lambda a: a.strip(), row.find_all("td")[-1].text.strip().split(" • ")))
        if row.find("td").text.strip() == "Time of Day:":
            data["time"] = row.find_all("td")[-1].get_text(",", strip=True).split(",")
        if row.find("td").text.strip() == "Season:":
            data["season"] = list(map(lambda a: a.strip(), row.find_all("td")[-1].text.strip().split(" • ")))
        if row.find("td").text.strip() == "Weather:":
            data["weather"] = list(map(lambda a: a.strip(), row.find_all("td")[-1].text.strip().split(" • ")))

        if row.find("td").text.strip() == "Difficulty:":
            data["difficulty"] = row.find_all("td")[-1].text.strip()

        if row.find("td").text.strip() == "Behaviour:":
            data["behaviour"] = row.find_all("td")[-1].text.strip()

        if row.find("td").text.strip() == "Size (inches):":
            data["size"] = row.find_all("td")[-1].text.strip()

        if row.find("td").text.strip() == "Fishing XP:":
            data["xp"] = list(row.find_all("td")[-1].stripped_strings)

        if row.find("td").text.strip() == "Healing Effect":
            cols = row.find_next_sibling("tr").find_all("table")
            data["energy"] = list(filter(lambda a: a != "Energy", cols[0].stripped_strings))
            data["health"] = list(filter(lambda a: a != "Health", cols[1].stripped_strings))

    if len(infotables) == 1:
        return data

    prices = infotables[1].find_all("tr")[2].find("td")
    data["prices"] = list(map(lambda a: a[:-1], prices.stripped_strings))


    villager_reactions = soup.find("table", "wikitable").find_all("tr")
    gifts = {}
    for row in villager_reactions:
        reaction = row.find("th").text.strip().lower()
        if reaction == "villager reactions":
            continue
        villagers = row.find("td")
        if villagers is not None:
            gifts[reaction] = list(map(lambda a: a.strip(), villagers.text.strip().split(' • ')))

    data["gifts"] = gifts

    return data


fishes = {"Angler","Crimsonfish","Glacierfish","Glacierfish_Jr.","Legend","Legend_II","Ms._Angler","Mutant_Carp","Radioactive_Carp","Son_of_Crimsonfish","Albacore","Anchovy","Clam","Cockle","Crimsonfish","Eel","Flounder","Halibut","Herring","Mussel","Octopus","Oyster","Pufferfish","Red_Mullet","Red_Snapper","Sardine","Sea_Cucumber","Squid","Super_Cucumber","Tilapia","Tuna","Angler","Bream","Catfish","Chub","Dorado","Glacierfish","Lingcod","Perch","Pike","Rainbow_Trout","Salmon","Shad","Smallmouth_Bass","Sunfish","Tiger_Trout","Walleye", "Bullhead","Carp","Chub","Largemouth_Bass","Legend","Lingcod","Midnight_Carp","Perch","Rainbow_Trout","Sturgeon","Walleye","Midnight_Carp","Perch","Pike","Smallmouth_Bass","Walleye","Carp","Catfish","Woodskip","Ghostfish","Ice_Pip","Lava_Eel","Stonefish","Carp","Mutant_Carp","Sandfish","Scorpion_Carp","Carp","Slimejack","Void_Salmon","Blobfish","Midnight_Squid","Spook_Fish","Clam","Cockle","Crab","Crayfish","Lobster","Mussel","Oyster","Periwinkle","Shrimp","Snail","Blue_Discus","Lionfish","Stingray"}
print(fishes)
data = []
for fish in fishes:
    data.append(parse_fish(fish))
with open("fish.json", "w") as f:
    f.write(json.dumps(data))
