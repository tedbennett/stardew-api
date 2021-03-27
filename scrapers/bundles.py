import requests
import json
import re
from bs4 import BeautifulSoup


def parse_bundles():
    url = "https://stardewvalleywiki.com/Bundles"
    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')

    data = []

    tables = soup.find_all("table", "wikitable")
    room = {}
    for table in tables:
        
        title = table.find("th").text.strip()
        rows = table.find_all("tr")
        print(title)
        if "Reward" in table.find("tr").text.strip():
            if room != {}:
                data.append(room)
                room = {}
            name = table.find_previous_sibling("h3").text.strip()
            room["name"] = name
            room["id"] = ''.join(e for e in name.replace(" ", "_") if (e.isalnum() or e == "_")).lower()

            room["bundles"] = []
            room["reward"] = table.find("td").text.strip()
            continue

        if "Bundle" in title and len(rows) > 2:
            bundle = {"title": title}
            bundle["image_url"] = "https://www.stardewvalleywiki.com{}".format(table.find("th").find("img")["src"])
            bundle["cover_image_url"] = "https://www.stardewvalleywiki.com{}".format(rows[1].find_all("td")[0].find("img")["src"])
            bundle["slots"] = len(rows[1].find_all("td")[1].find_all("img"))
            items = []
            print(len(rows[1:]))
            for row in rows[1:]:
                cols = row.find_all("td")
                if len(cols) == 2:
                    item = cols[0].text.strip()
                elif len(cols) == 4:
                    item = cols[2].text.strip()
                else:
                    continue
                if item == "Reward:":
                    bundle["reward"] = get_item_quantity(cols[1].text.strip())
                elif item == "" and cols[1].text.strip() != "":
                    items.append(get_item_quantity(cols[1].text.strip()))
                elif item != "":
                    items.append(get_item_quantity(item))
                
                
            bundle["items"] = items
            room["bundles"].append(bundle)
    data.append(room)
    return data

def get_item_quantity(item):
    regex = re.search(r'(.*)\((\d*)\)', item)
    if regex is not None and len(regex.groups()) > 1:
        quality = re.search('(.*)quality(.*)', regex.groups()[0])
        if quality is not None and len(quality.groups()) > 1:
            return {
                "name": quality.groups()[1].strip(),
                "quantity": int(regex.groups()[1].strip()),
                "quality": quality.groups()[0].strip()
            }
        else:
            return {
                "name": regex.groups()[0].strip(),
                "quantity": int(regex.groups()[1].strip())
            }
            
    else:
        quality = re.search('(.*)quality(.*)', item)
        if quality is not None and len(quality.groups()) > 1:
            return {
                "name": quality.groups()[1].strip(),
                "quantity": 1,
                "quality": quality.groups()[0].strip()
            }
        else:
            return {
                "name": item,
                "quantity": 1
            }

data = parse_bundles()
with open("../data/bundles.json", "w") as f:
    f.write(json.dumps(data))