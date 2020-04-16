import math
from random import sample
from tkinter import *
#import tkinter as tk

k = 32

class Ranking:

    itemsDict = {}
    lastMatchup = []
    longestItemName = 0
    left = ""
    right = ""

    def __init__(self):
        reader = open("items.txt", "r")
        for i in reader:
            self.itemsDict[i.rstrip()] = 1500

        for item in self.itemsDict.keys():
            if len(item) > self.longestItemName:
                self.longestItemName = len(item)

    def itemCount(self):
        return len(self.itemsDict)

    def getLongestItemName(self):
        return self.longestItemName

    def getItemsWithScores(self):
        returnString = ""

        for item,score in sorted(self.itemsDict.items(), key = lambda x : (-x[1], x[0])):
            returnString += "{itm:<{wid}} {scr}\n".format(itm = item, wid = self.longestItemName + 5, scr = score)
        
        return returnString.rstrip()

    def getItemsNoScores(self):
        returnString = ""

        for item,score in sorted(self.itemsDict.items(), key = lambda x : (-x[1], x[0])):
            returnString += "{itm:<{wid}}\n".format(itm = item, wid = self.longestItemName)
        
        return returnString
    
    def getAlphabeticalItemsWithScores(self):
        returnString = ""

        for item in sorted(self.itemsDict.keys()):
            returnString += "{itm:<{wid}} {scr}\n".format(itm = item, wid = self.longestItemName + 5, scr = self.itemsDict[item])

        return returnString.rstrip()

    def getAlphabeticalItemsNoScores(self):
        returnString = ""

        for item in sorted(self.itemsDict.keys()):
            returnString += "{itm:<{wid}}\n".format(itm = item, wid = self.longestItemName)

        return returnString


    def nextMatchup(self):
        matchup = sample(self.itemsDict.keys(), 2)
        
        while (matchup[0] in self.lastMatchup and matchup[1] in self.lastMatchup):
            matchup = sample(self.itemsDict.keys(), 2)

        self.lastMatchup = matchup
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
        self.hideScores = IntVar()
        self.hideOrder = IntVar()
        self.hideAll = IntVar()
        master.title("Elo Ranker")

        #Left Button
        self.leftButton = Button(master, text = "", command = self.left)
        self.leftButton.grid(row = 0, column = 0, sticky = N + S + W + E)

        #Right Button
        self.rightButton = Button(master, text = "", command = self.right)
        self.rightButton.grid(row = 0, column = 1, sticky = N + S + W + E)

        #Text Box
        self.ranking = Text(master, height = ranker.itemCount(), width = ranker.getLongestItemName() + 15, state = DISABLED)
        # self.ranking.grid(row = 2, columnspan = 2, sticky = N + S + W + E)
        self.ranking.grid(row = 1, column = 0, sticky = N + S + W + E)
        self.ranking.tag_configure("center", justify = "center")
        self.updateRanks()

        #Menu
        self.optionsFrame = Frame(master)
        self.optionsFrame.grid(row = 1, column = 1, sticky = N + S + W + E)

        self.optionsLabel = Label(self.optionsFrame, text = 'Options')
        self.optionsLabel.pack()

        self.hideScoresButton = Checkbutton(self.optionsFrame, text = 'Hide Scores', variable = self.hideScores, command = self.updateRanks)
        self.hideOrderButton = Checkbutton(self.optionsFrame, text = 'Hide Order  ', variable = self.hideOrder, command = self.updateRanks)
        self.hideAllButton = Checkbutton(self.optionsFrame, text = 'Hide List      ', variable = self.hideAll, command = self.hideAllFunction)
        self.hideScoresButton.pack()
        self.hideOrderButton.pack()
        self.hideAllButton.pack()
        

        #Grid Configuration
        self.master.grid_columnconfigure(0, weight = 1, uniform = 'half')
        self.master.grid_columnconfigure(1, weight = 1, uniform = 'half')
        self.master.grid_rowconfigure(0, weight = 1)
        self.master.grid_rowconfigure(1, weight = 1)

        self.updateButtons()

    def hideAllFunction(self):
        if self.hideAll.get() == 1: #Button turned on
            self.hideScoresButton.select()
            self.hideScoresButton['state'] = DISABLED
            self.hideOrderButton.select()
            self.hideOrderButton['state'] = DISABLED
        else:
            self.hideScoresButton.deselect()
            self.hideScoresButton['state'] = NORMAL
            self.hideOrderButton.deselect()
            self.hideOrderButton['state'] = NORMAL

        self.updateRanks()

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

        if self.hideAll.get() == 1:
            self.ranking.insert(END, "")
        elif self.hideScores.get() == 1 and self.hideOrder.get() == 1:
            self.ranking.insert(END, ranker.getAlphabeticalItemsNoScores())
        elif self.hideScores.get() == 1:
            self.ranking.insert(END, ranker.getItemsNoScores())
        elif self.hideOrder.get() == 1:
            self.ranking.insert(END, ranker.getAlphabeticalItemsWithScores())
        else:    
            self.ranking.insert(END, ranker.getItemsWithScores())

        self.ranking.tag_add("center", 1.0, END)
        self.ranking['state'] = DISABLED

if __name__ == "__main__":
    ranker = Ranking()
    root = Tk()
    gui = GUI(root, ranker)
    root.mainloop()