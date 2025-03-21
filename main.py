# This is a sample Python script.
from GameMaster import GameMaster
from AIManager import AIManager




# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    Manager = AIManager()
    Game = GameMaster()
    savePeriod = 100
    curCount = 0
    while(not AIManager.IsTrainingComplete()): #training Loop
        Game.SetPlayers(AIManager.setPlayers())
        results = Game.RunGame()
        AIManager.UpdateTables(results)
        if curCount%100==0:
            AIManager.saveQTables(curCount)
        curCount=curCount+1







