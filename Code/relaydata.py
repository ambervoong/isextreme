
class Subject:
    def __init__(self):
        self.listObserver = []
        self.changed = False

    def registerObserver(self, observer):
        self.listObserver.append(observer)

    def removeObserver(self, observer):
        self.listObserver.remove(observer)

    def dataChanged(self):
        self.setChanged()
        self.notifyObservers()

    def setChanged(self):
        self.changed = True

    def notifyObservers(self):
        for observer in self.listObserver:
            observer.update(self)
        self.changed = False

class ProgressRelay(Subject):
    def __init__(self, stages=2):
        super().__init__()
        self.currStage = 0
        self.subStage = 0 # value between each Stage
        self.isComplete = False
        self.maxStage = stages

    def reset(self):
        self.isComplete = False
        self.currStage = 0
        self.resetSubStage()
        super().dataChanged()

    def resetSubStage(self):
        self.subStage = 0


    def setMeasurements(self, currVal, maxVal, whenToUpdate=2):
        # a value between 0 and 1
        self.subStage = currVal / maxVal
        if (currVal % whenToUpdate == 0):
            super().dataChanged()

    def incrementStage(self):
        self.currStage = self.currStage + 1
        self.resetSubStage()
        super().dataChanged()

    def complete(self):
        self.isComplete = True
        self.currStage = self.maxStage
        super().dataChanged()

    def progressReport(self):
        if self.isComplete:
            return 100
        else:
            report = (self.currStage + self.subStage) / self.maxStage * 100 * 0.95
            return report






