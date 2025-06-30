from abc import ABC, abstractmethod
from app.operations import Operation

#Calculation Starts
class Calculation(ABC):
    """
        Calculation Class that will handle all calculations of the, this is just a template that future subclasses will be forced to follow
    """
    def __init__(self, a: float, b: float) -> None:
        """
            Initializes a calculation
        """
        self.a: float = a
        self.b: float = b

    @abstractmethod
    def execute(self) -> float:
        """
            Each subclass will have a execution that will return a float output
        """

        pass

    def __str__(self) -> str:
        result = self.execute()
        operation_name = self.__class__.__name__.replace("Calculation", "") #derives calculation name from subclass
        return f"{self.__class__.__name__}: {self.a} {operation_name} {self.b} = {result}" #toString

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(a={self.a},b={self.b})"


class CalculationFactory:
    """
        Creates instances of Calculation subclasses to make object creation flexible.
    """
    _calculation = {}

    @classmethod
    def register_calculation(cls,calculation_type: str):
        """
            to be able to map a calculation to a indentifier "+" for addition, "-" for subtraction etc
        """     
        def decorator(subclass):
            if calculation_type in cls._calculation:
                raise ValueError(f"Calculation type '{calculation_type}' is alread apart of calculations")
            cls._calculation[calculation_type] = subclass
            return subclass
        #print(cls._calculation)
        return decorator
    
    @classmethod
    def create_calculation(cls,calculation_type: str, a:float, b:float) -> Calculation:
        """
            Create an instance of a specific subclass for each calculation type given.
        """
        #print("test_cc")
        #print(calculation_type,a,b)
        #print(cls._calculation)
        calculation_class = cls._calculation.get(calculation_type)
        #print("test3")
        if not calculation_class:
            #print("test4_bad")
            available_types = ', '.join(cls._calculations.keys())
            raise ValueError(f"Unsupported calculation '{calculation_type}', Available: 'available_types'")
        return calculation_class(a,b)


### Calculation Classes

@CalculationFactory.register_calculation('+')
class AddCalculation(Calculation):
    '''
        Class for adding two numbers, (adds addition to calculator) '+' for addition
    '''
    def execute(self) -> float:
        #print("test2")
        return Operation.addition(self.a,self.b)


@CalculationFactory.register_calculation('-')
class SubtractCalculation(Calculation):
    '''
        Class for subracting two numbers, (adds subtraction to calculator) '-' for subtraction
    '''

    def execute(self) -> float:
        return Operation.subtraction(self.a,self.b)

        
@CalculationFactory.register_calculation('/')
class DivisionCalculation(Calculation):
    '''
        Class for dividing two numbers, (adds subtraction to calculator) '/' for division
    '''

    def execute(self) -> float:
        return Operation.divide(self.a,self.b)


@CalculationFactory.register_calculation('*')
class MultiplyCalculation(Calculation):
    '''
        Class for multiplying two numbers, (adds subtraction to calculator) '*' for multiplcation
    '''

    def execute(self) -> float:
        return Operation.multiply(self.a,self.b)

@CalculationFactory.register_calculation('%')
class ModuloCalculation(Calculation):
    '''
        Class for Modulo two numbers, (adds subtraction to calculator) '%' for modulous
    '''

    def execute(self) -> float:
        return Operation.modulo(self.a,self.b)


@CalculationFactory.register_calculation('^')
class PowCalculation(Calculation):
    '''
        Class for power of a to b, (adds subtraction to calculator) '^' for pow
    '''

    def execute(self) -> float:
        return Operation.pow(self.a,self.b)


@CalculationFactory.register_calculation('?')
class RootCalculation(Calculation):
    '''
        Class for Root of A given B, (adds subtraction to calculator) '?' for root
    '''

    def execute(self) -> float:
        return Operation.root(self.a,self.b)
