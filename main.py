import math
from random import sample
from tkinter import *
#import tkinter as tk

k = 32

class Ranking:

    itemsDict = {}
    left = ""
    right = ""

    def __init__(self):
        reader = open("items.txt", "r")
        for i in reader:
            self.itemsDict[i.rstrip()] = 1500

    def itemCount(self):
        return len(self.itemsDict)

    def longestBreedName(self):
        longestBreedName = 0

        for breed in self.itemsDict.keys():
            if len(breed) > longestBreedName:
                longestBreedName = len(breed)

        return longestBreedName

    def getString(self):
        rankString = ""

        for breed,score in sorted(self.itemsDict.items(), key = lambda x : (-x[1], x[0])):
            rankString += "{brd:<{wid}} {scr}\n".format(brd=breed, wid = self.longestBreedName() + 5, scr = score)
        
        return rankString.rstrip()

    def nextMatchup(self):
        matchup = sample(self.itemsDict.keys(), 2)
        self.left = matchup[0]
        self.right = matchup[1]
        return matchup

    def calculateResult(self, result):
        if result == "left":
            winner = self.left
            loser = self.right
        elif result == "right":
            winner = self.right
            loser = self.left

        ExpectedScoreWinner = (1 + 10**((self.itemsDict[loser] - self.itemsDict[winner])/400.0))**-1
        ExpectedScoreLoser = 1 - ExpectedScoreWinner

        self.itemsDict[winner] = round(self.itemsDict[winner] + k*(1-ExpectedScoreWinner))
        self.itemsDict[loser] = round(self.itemsDict[loser] + k*(0-ExpectedScoreLoser))

class GUI:
    def __init__(self, master, ranker):
        self.master = master
        self.ranker = ranker
        master.title("Elo Ranker")

        self.leftButton = Button(master, text = "", command = self.left)
        self.leftButton.grid(row = 0, column = 0, sticky = N + S + W + E)

        self.rightButton = Button(master, text = "", command = self.right)
        self.rightButton.grid(row = 0, column = 1, sticky = N + S + W + E)

        self.ranking = Text(master, height = ranker.itemCount(), width = ranker.longestBreedName() + 15, state = DISABLED)
        self.ranking.grid(row = 1, columnspan = 2, sticky = N + S + W + E)
        self.ranking.tag_configure("center", justify = "center")
        self.updateRanks()

        self.master.grid_columnconfigure(0, weight = 1, uniform = 'half')
        self.master.grid_columnconfigure(1, weight = 1, uniform = 'half')
        self.master.grid_rowconfigure(0, weight = 1)
        self.master.grid_rowconfigure(1, weight = 1)

        self.updateButtons()

    def left(self):
        self.ranker.calculateResult("left")
        self.updateButtons()
        self.updateRanks()

    def right(self):
        self.ranker.calculateResult("right")
        self.updateButtons()
        self.updateRanks()

    def updateButtons(self):
        newItems = self.ranker.nextMatchup()
        self.leftButton.config(text = newItems[0])
        self.rightButton.config(text = newItems[1])

    def updateRanks(self):
        self.ranking['state'] = NORMAL
        self.ranking.delete(1.0, END)
        self.ranking.insert(END, ranker.getString())
        self.ranking.tag_add("center", 1.0, END)
        self.ranking['state'] = DISABLED

if __name__ == "__main__":
    ranker = Ranking()
    root = Tk()
    gui = GUI(root, ranker)
    root.mainloop()