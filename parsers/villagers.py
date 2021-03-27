import requests
import json
from bs4 import BeautifulSoup

def parse_bachelor_villager(name):
    print("Parsing bachelor {}".format(name))
    url = "https://www.stardewvalleywiki.com/{}".format(name)
    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')

    data = {}

    infobox = soup.find(id="infoboxtable")

    name = infobox.find(id="infoboxheader").text.strip()
    data["name"] = name
    data["id"] = ''.join(e for e in name.replace(" ", "_") if (e.isalnum() or e == "_")).lower()
    data["image_url"] = "https://www.stardewvalleywiki.com{}".format(infobox.find("img")["src"])
    data["wiki_url"] = url

    for row in infobox.find_all("tr"):
        if row.find("td").text.strip() == "Birthday:":
            data["birthday"] = row.find_all("td")[-1].text.strip()
        if row.find("td").text.strip() == "Address:":
            data["address"] = row.find_all("td")[-1].text.strip()
        
    data["marriage"] = True
    tables = soup.find_all("table", "wikitable")
    schedule = {}
    gifts = {}
    for table in tables:
        # Find tables which are schedule
        if table.find("th").text.strip() == "Time":
            table_schedule = {}
            table_schedule["condition"] = table.find_previous_sibling(
                "p").text.strip()
            times = []
            for row in table.find_all("tr"):
                cells = row.find_all("td")
                if len(cells) != 2:
                    continue
                times.append(
                    {"time": cells[0].text.strip(), "location": cells[1].text.strip()})
            table_schedule["schedule"] = times
            season = table.parent.parent.parent.find("span").text.strip().lower()
            if season not in schedule:
                table_schedule["priority"] = 0
                schedule[season] = [table_schedule]
            else:
                table_schedule["priority"] = len(schedule[season])
                schedule[season].append(table_schedule)
        elif table.find("th").text.strip() == "Image":
            gift_reaction = table.find_previous_sibling("h3").text.strip().lower()
            items = []
            for row in table.find_all("tr")[1:]:
                cols = row.find_all("td")
                if len(cols) == 2:
                    bullets = cols[1].find_all("li")
                    for bullet in bullets:
                        items.append(
                            {"name": bullet.text.strip(), "collection": True})
                elif len(cols) > 2:
                    items.append(
                        {"name": cols[1].text.strip(), "collection": False})
            gifts[gift_reaction] = items
            if gift_reaction == "hate" or gift_reaction == "hates":
                break

    data["gifts"] = gifts
    data["schedule"] = schedule
    return data

def parse_villager(name):
    print("Parsing villager {}".format(name))
    response = requests.get("https://www.stardewvalleywiki.com/{}".format(name))

    soup = BeautifulSoup(response.text, 'html.parser')

    data = {}

    infobox = soup.find(id="infoboxtable")

    data["name"] = infobox.find(id="infoboxheader").text.strip()
    data["image_url"] = infobox.find("img")["src"]

    for row in infobox.find_all("tr"):
        if row.find("td").text.strip() == "Birthday:":
            data["birthday"] = row.find_all("td")[-1].text.strip()
        if row.find("td").text.strip() == "Address:":
            data["address"] = row.find_all("td")[-1].text.strip()
    data["marriage"] = False
    tables = soup.find_all("table", "wikitable")
    schedule = []
    gifts = {}
    for table in tables:
        # Find tables which are schedule
        if table.find("th").text.strip() == "Image":
            gift_reaction = table.find_previous_sibling("h3").text.strip().lower()
            items = []
            for row in table.find_all("tr")[1:]:
                cols = row.find_all("td")
                if len(cols) == 2:
                    bullets = cols[1].find_all("li")
                    for bullet in bullets:
                        items.append(
                            {"name": bullet.text.strip(), "collection": True})
                elif len(cols) > 2:
                    items.append(
                        {"name": cols[1].text.strip(), "collection": False})
            gifts[gift_reaction] = items
            if gift_reaction == "hate" or gift_reaction == "hates":
                break
        else:
            table_schedule = {}
            table_schedule["condition"] = table.find("th").text.strip()
            times = []
            for row in table.find_all("tr"):
                cells = row.find_all("td")
                if len(cells) != 2:
                    continue
                times.append(
                    {"time": cells[0].text.strip(), "location": cells[1].text.strip()})
            table_schedule["schedule"] = times
            table_schedule["priority"] = len(schedule)
            schedule.append(table_schedule)
        

    data["gifts"] = gifts
    data["schedule"] = schedule
    return data

all_villagers = []
bachelors = ["Shane","Alex","Elliot","Harvey","Sam","Sebastian","Abigail","Emily","Haley","Leah","Maru","Penny"]
villagers = ["Caroline","Clint","Demetrius","Evelyn","George","Gus","Jas","Jodi","Kent","Lewis","Linus","Marnie","Pam","Pierre","Robin","Sandy","Vincent","Willy","Wizard"]

for bachelor in bachelors:
    all_villagers.append(parse_bachelor_villager(bachelor))
for villager in villagers:
    all_villagers.append(parse_villager(villager))
with open("villagers.json", "w") as f:
    f.write(json.dumps(all_villagers))