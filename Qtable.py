from pathlib import Path

import numpy as np

class Qtable:
    """
    Qtable Setup
    Table is a 3d array
    first values: player types
        tables 0-3 = attacking
        tables 4-7 = defending

        for each table above
            1st = player one First to play
            2nd = player 2
            3rd = player 3
            4th = player 4

    second value: current play state
        0 = team is winning trick with high probability. Threshold value to be decided.
        1 = team is winning trick with slim probability. Threshold value to be decided.
        2 = team is losing trick with slim probability.
        3 = team is losing trick with high probability.

    third value: actions
        0: Use trump
        1: Use led Suit
        2: throwaway trump
        3: throwaway suit led

    For 1st player Qtable is different
        second value is 0: state is same

        third value:
            0: Lead high off suit
            1: Set up partner
            2: trump showdown

    """


    def __init__(self):
        self.counter = 0
        self.table = np.zeros((8, 4, 4))
        self.training=True
        #self.UseQtable() todo
        #self.Startat()
        #self.prob = np.empty((0, 2), dtype=float)

    def UseQtable(self):
        counter = 6600000
        file = f"milestoneQTables/QtableAt{counter}.npy"
        filePath = Path(file)
        if filePath.exists():
            self.table = np.load(file)

    def getQvalue(self, state, action):
        return 0

    def updateQvalue(self, state, action, value):
        pass

    def nextStateBestValue(self,state,action):
        pass

    def SaveProb (self, probo,player):
       new_pair = np.array([[probo, player]])
       self.prob= np.vstack([self.prob, new_pair])

    def Startat(self, counter):
        file = f"milestoneQTables/QtableAt{counter}.npy"
        filePath = Path(file)
        if filePath.exists():
            self.table = np.load(file)

    def getTable(self):
        return self.table

    def updateCounter(self):
        # update every round. Tracks number of games and saves QTables at intervals.
        self.counter = self.counter + 1
        print(f"counter::::::::::::::::::::{self.counter}")
        if self.counter %1000 ==0:
            self.checkDifference()
            np.save("tempQtables/temp.npy",self.table)

        if self.counter % 100000 == 0:
            filename = f"milestoneQTables/QtableAt{self.counter}.npy"
            np.save(filename, self.table)
           # np.savetxt(f"milestoneQTables/ProbabilityAt{self.counter}.csv", self.prob, delimiter=",", header="x,y", fmt="%.2f")


    def checkDifference(self):
        file = "tempQtables/temp.npy"
        filePath = Path(file)
        if filePath.exists():
            oldQtable= np.load(file)
            diff_precent = np.mean(np.abs(self.table-oldQtable)/oldQtable)
            if diff_precent < .001:# less that .1%
                self.training=False

