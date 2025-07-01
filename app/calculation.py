from abc import ABC, abstractmethod
from app.operations import Operation

class Calculation(ABC):
    def __init__(self, a: float, b: float) -> None:  # pragma: no cover
        self.a: float = a  # pragma: no cover
        self.b: float = b  # pragma: no cover

    @abstractmethod
    def execute(self) -> float:  # pragma: no cover
        pass  # pragma: no cover

    def __str__(self) -> str:  # pragma: no cover
        result = self.execute()  # pragma: no cover
        operation_name = self.__class__.__name__.replace("Calculation", "")  # pragma: no cover
        return f"{self.__class__.__name__}: {self.a} {operation_name} {self.b} = {result}"  # pragma: no cover

    def __repr__(self) -> str:  # pragma: no cover
        return f"{self.__class__.__name__}(a={self.a},b={self.b})"  # pragma: no cover

class CalculationFactory:
    _calculation = {}

    @classmethod
    def register_calculation(cls, calculation_type: str):
        def decorator(subclass):
            if calculation_type in cls._calculation:  # pragma: no cover
                raise ValueError(f"Calculation type '{calculation_type}' is already part of calculations")  # pragma: no cover
            cls._calculation[calculation_type] = subclass
            return subclass
        return decorator
    
    @classmethod
    def create_calculation(cls, calculation_type: str, a: float, b: float) -> Calculation:
        calculation_class = cls._calculation.get(calculation_type)
        if not calculation_class:
            available_types = ', '.join(cls._calculation.keys())
            raise ValueError(f"Unsupported calculation '{calculation_type}', Available: '{available_types}'")
        return calculation_class(a, b)

@CalculationFactory.register_calculation('+')
class AddCalculation(Calculation):
    def execute(self) -> float:
        return Operation.addition(self.a, self.b)

@CalculationFactory.register_calculation('-')
class SubtractCalculation(Calculation):
    def execute(self) -> float:
        return Operation.subtraction(self.a, self.b)

@CalculationFactory.register_calculation('/')
class DivisionCalculation(Calculation):
    def execute(self) -> float:
        return Operation.divide(self.a, self.b)

@CalculationFactory.register_calculation('*')
class MultiplyCalculation(Calculation):
    def execute(self) -> float:
        return Operation.multiply(self.a, self.b)

@CalculationFactory.register_calculation('%')
class ModuloCalculation(Calculation):
    def execute(self) -> float:
        return Operation.modulo(self.a, self.b)

@CalculationFactory.register_calculation('^')
class PowCalculation(Calculation):
    def execute(self) -> float:
        return Operation.pow(self.a, self.b)

@CalculationFactory.register_calculation('?')
class RootCalculation(Calculation):
    def execute(self) -> float:
        return Operation.root(self.a, self.b)

@CalculationFactory.register_calculation('//')
class IntegerDivisionCalculation(Calculation):
    def execute(self) -> float:
        return Operation.intDivide(self.a, self.b)

@CalculationFactory.register_calculation('--')
class AbsoluteDiffCalculation(Calculation):
    def execute(self) -> float:
        return Operation.absSubtraction(self.a, self.b)

@CalculationFactory.register_calculation('/%')
class PercentageCalculation(Calculation):
    def execute(self) -> float:
        return Operation.percentage(self.a, self.b)
