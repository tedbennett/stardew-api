import requests
import json
import re
from bs4 import BeautifulSoup


def parse_craftables():
    url = "https://www.stardewvalleywiki.com/Crafting"
    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')

    data = []

    for table in soup.find_all("table", "wikitable"):
        data.append(parse_table(table))

    return data

def parse_table(table):
    data = {}
    titles = list(map(lambda a: a.text.strip(), list(table.find_all("th"))))
    
    for row in table.find_all("tr"):
        for index, col in enumerate(row.find_all("td")):
            if titles[index] == "Image":
                data["image_url"] = "https://www.stardewvalleywiki.com{}".format(col.find("img")["src"])

            if titles[index] == "Name":
                data["name"] = col.text.strip()
                data["id"] = ''.join(e for e in col.text.strip().replace(" ", "_") if (e.isalnum() or e == "_")).lower()

            if titles[index] == "Description":
                data["description"] = col.text.strip()

            if titles[index] == "Ingredients":
                strings = list(col.stripped_strings)
                print(strings)
                ingredients = []
                for i in range(0, len(strings) // 2, 2):
                    num = re.search(r'\d+', strings[i + 1])
                    if num is None:
                        ingredients.append({"name": strings[i], "quantity": 1})
                    else:
                        ingredients.append({
                            "name": strings[i],
                            "quantity": num.group()
                        })
                data["ingredients"] = ingredients
        
            if titles[index] == "Recipe Source":
                data["recipe_source"] = col.text.strip()
    return data

def parse_ingredients(string):
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

data = parse_craftables()

with open("craftables.json", "w") as f:
    f.write(json.dumps(data))


