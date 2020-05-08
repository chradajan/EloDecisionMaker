from urllib.request import Request, urlopen
import urllib.error
from html.parser import HTMLParser
import re

def getName(decodedLine):
    result = re.search(r"title=\"(\w+ ?'?-?\w+)", decodedLine)
    return result.group(1).rstrip()

def parser():
    link = 'https://animalcrossing.fandom.com/wiki/Villager_list_(New_Horizons)'
    WebSocHTML = Request(link, headers={'User-Agent': 'Mozilla/5.0'})

    with urlopen(WebSocHTML) as file:

        trCounter = 0
        location = 0

        for line in file:
            decodedLine = line.decode()

            if location > 0:
                if location == 1:
                    print(getName(decodedLine))
                #...
                elif location == 6:
                    location = 0
                    continue

                location += 1
                continue

            if decodedLine.startswith('<tr>'):
                trCounter += 1
                if trCounter > 3:
                    location = 1


if __name__ == '__main__':
    parser()