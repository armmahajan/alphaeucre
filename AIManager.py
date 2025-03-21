import AIPlayer
class AIManager:

    def AIManager(self):
        self.playersArr=[]
        pass

    def setPlayers(self):

        for i in range(1,4):
            self.playersArr[i] = AIPlayer.AIPlayer(self.createNewQtable())
        pass


    def createNewQtable(self):
        return 0;

    def IsTrainingComplete(self):
        # if Q-values have minimal change or if Q-values are cycling training is complete return true. else false
        return False