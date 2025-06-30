#history management

from abc import ABC, abstractmethod
from logger import get_logger
from app.calculation import Calculation
import pandas as pd
log = get_logger("history")

save_file = 

class HistoryObserver(ABC):
    @abstractmethod
    def update(self,calc:Calculation)-> None:
        """
            Handle new calculation event
        """


class LoggingObserver(HistoryObserver):
    #logs calculation to the log
    def update(self,calc:Calculation)-> None:
        if calc is None:
            log.warn("{calc}, Calculation cannot be None") 
            raise AttributeError("Calculation cannot be None")

        log.info(f"Calculation Performed: Expression - {calc.expression}, Result - {result}"})
        

    
