import requests
import json
import re
from bs4 import BeautifulSoup


def parse_artisan_goods(name):
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
        if row.find("td").text.strip() == "Healing Effect":
            if row.find_all("td")[-1].text.strip() == "Inedible":
                continue
            cols = row.find_next_sibling("tr").find_all("table")
            data["energy"] = list(filter(lambda a: a != "Energy", cols[0].stripped_strings))
            data["health"] = list(filter(lambda a: a != "Health", cols[1].stripped_strings))
        if row.find("td").text.strip() == "Sell Price":
            print("price")
            data["prices"] = list(map(lambda a: a[:-1], list(row.find("td").stripped_strings)))
        if row.find("td").text.strip() == "Equipment:":
            data["equipment"] = row.find_all("td")[-1].text.strip()
        
        if row.find("td").text.strip() == "Processing Time:":
            data["processing_time"] = row.find_all("td")[-1].text.strip()

        if row.find("td").text.strip() == "Ingredients:":
            ingredients = list(row.find_all("td")[-1].text.strip().split(' or '))
            data["ingredients"] = list(map(lambda a: parse_ingredient(a), ingredients))

    if len(infotables) > 1:
        if "prices" not in data:
            price_table = infotables[1]
            prices = price_table.find("table")
            data["prices"] = list(map(lambda a: a[:-1], list(prices.stripped_strings)))

        info = infotables[2].find_all("tr")
        for row in info[1:]:
            if row.find("td").text.strip() == "Equipment:":
                data["equipment"] = row.find_all("td")[-1].text.strip()
            
            if row.find("td").text.strip() == "Processing Time:":
                data["processing_time"] = row.find_all("td")[-1].text.strip()

            if row.find("td").text.strip() == "Ingredients:":
                ingredients = list(row.find_all("td")[-1].text.strip().split(' or '))
                data["ingredients"] = list(map(lambda a: parse_ingredient(a), ingredients))

    

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

def parse_ingredient(string):
    regex = re.search(r'(.*)\((\d+)\)', string)
    if regex is None:
        return {
            "name": string.strip(),
            "quantity": 1
        }
    groups = regex.groups()
    return {
        "name": groups[0].strip(),
        "quantity": groups[1]
    }

artisan_goods = {"Honey","Beer","Cheese","Goat_Cheese","Mead","Pale_Ale","Wine","Cheese","Goat_Cheese","Beer","Coffee","Green_Tea","Juice","Mead","Pale_Ale","Wine","Cloth","Dinosaur_Mayonnaise","Duck_Mayonnaise","Mayonnaise","Void_Mayonnaise","Oil","Truffle_Oil","Aged_Roe","Caviar","Jellies_and_Pickles","Maple_Syrup","Oak_Resin","Pine_Tar","Piña_Colada"}
data = list(map(lambda a: parse_artisan_goods(a), artisan_goods))

with open("artisan-goods.json", "w") as f:
    f.write(json.dumps(data))


