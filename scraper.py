from urllib.request import Request, urlopen, urlretrieve
import urllib.error
import re

currentName = ''

def getName(decodedLine):
    result = re.search(r"title=\"(\w+ ?'?-?\w+)", decodedLine)
    name = result.group(1)
    return name

def getImage(decodedLine, name):
    result = re.search(r'a href=\"([\w\?\%:/.=_-]+)\"', decodedLine)
    link = result.group(1)
    destination = "villagers/photos/{}.jpg".format(name.replace(' ', '_'))
    urlretrieve(link, destination)
    return destination

def getPersonality(decodedLine):
    result = re.search(r"a href=\"/wiki/(\w+)\"", decodedLine)
    personality = result.group(1)
    return personality

def getSpecies(decodedLine):
    result = re.search(r"a href=\"/wiki/([a-zA-Z]+).*\" title", decodedLine)
    species = result.group(1)
    return species

def getBirthday(decodedLine):
    result = re.search(r"> +(\w+ \d\d?)<", decodedLine)
    birthday = result.group(1)
    return birthday

def getCatchphrase(decodedLine):
    result = re.search(r"<i> ?\"(.*)\" ?</i>", decodedLine)
    catchphrase = result.group(1)
    return catchphrase

def parser():
    link = 'https://animalcrossing.fandom.com/wiki/Villager_list_(New_Horizons)'
    WebSocHTML = Request(link, headers={'User-Agent': 'Mozilla/5.0'})

    with urlopen(WebSocHTML) as file:

        trCounter = 0
        location = 0
        name = ''
        villagers = open('villagers/villagers.txt', 'w')

        for line in file:
            decodedLine = line.decode()

            if location > 0:
                if location == 1:
                    name = getName(decodedLine)
                    villagers.write(name + '\n')
                if location == 2:
                    path = getImage(decodedLine, name)
                    villagers.write(path + '\n')
                if location == 3:
                    personality = getPersonality(decodedLine)
                    villagers.write(personality + '\n')
                if location == 4:
                    species = getSpecies(decodedLine)
                    villagers.write(species + '\n')
                if location == 5:
                    birthday = getBirthday(decodedLine)
                    villagers.write(birthday + '\n')
                elif location == 6:
                    catchphrase = getCatchphrase(decodedLine)
                    villagers.write(catchphrase + '\n\n')
                    location = 0
                    continue

                location += 1
                continue

            if decodedLine.startswith('<tr>'):
                trCounter += 1
                if trCounter > 3:
                    location = 1
        
        villagers.close()


if __name__ == '__main__':
    parser()