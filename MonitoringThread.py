import threading
import time

class MonitoringThread(threading.Thread):
    def __init__(self, totalTime, updateInfoFunction):
        super(MonitoringThread, self).__init__()
        self.totalTime = totalTime
        self.updateInfoFunction = updateInfoFunction
        self.currentTime = 0
        self.isRunning = True
        
    def run(self):
        print(self.currentTime)
        print(self.totalTime)
        while self.isRunning and self.currentTime < self.totalTime:
            self.updateInfoFunction()
            self.currentTime += 1
            threading.Thread(target=self._stop).start() 

    def _stop(self):
        if self.currentTime >= self.totalTime:
            self.isRunning = False