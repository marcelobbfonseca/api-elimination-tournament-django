
from apscheduler.schedulers.background import BackgroundScheduler
from abc import abstractclassmethod, ABCMeta

class Singleton(metaclass=ABCMeta):

    @abstractclassmethod
    def print_data():
        """ Implement in child class"""


class BGScheduler(Singleton):
    __instance = None
    
    def __init__(self) -> None:
        if BGScheduler.__instance != None:
            raise Exception('Singleton already instantiated')
        self.sched = BackgroundScheduler()
        self.sched.start()
        BGScheduler.__instance = self

    @staticmethod
    def get_instance():
        if BGScheduler.__instance == None:
            BGScheduler()
        return BGScheduler.__instance


    @staticmethod
    def print_data():
        print(BGScheduler.__instance)
