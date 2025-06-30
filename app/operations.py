import math
from app.exceptions import OperationError

class Operation:
    @staticmethod
    def addition(a: float, b: float) -> float:
        """
        Adds two values of type float
        **Params**
            - *a (float)*: First float value
            - *b (float)*: Second float value
        **Returns**
            - *float*: Sum of *a* and *b*
        """
        try:
            return a + b
        except OverflowError as e:
            raise OperationError(f"Addition overflow: {str(e)}")  # pragma: no cover

    @staticmethod
    def subtraction(a: float, b: float) -> float:
        """
        Subtracts two values of type float
        **Params**
            - *a (float)*: First float value
            - *b (float)*: Second float value
        **Returns**
            - *float*: Difference of *a* and *b*
        """
        try:
            return a - b
        except OverflowError as e:
            raise OperationError(f"Subtraction overflow: {str(e)}")  # pragma: no cover

    @staticmethod
    def multiply(a: float, b: float) -> float:
        """
        Multiplies two values of type float
        **Params**
            - *a (float)*: First float value
            - *b (float)*: Second float value
        **Returns**
            - *float*: Multiplication of *a* and *b*
        """
        try:
            return a * b
        except OverflowError as e:
            raise OperationError(f"Multiplication overflow: {str(e)}")  # pragma: no cover

    @staticmethod
    def divide(a: float, b: float) -> float:
        """
        Divides two values of type float
        **Params**
            - *a (float)*: First float value
            - *b (float)*: Second float value
        **Returns**
            - *float*: Division of *a* and *b*
        """
        if b == 0:
            raise OperationError("Divide By Zero Error")
        try:
            return a / b
        except OverflowError as e:
            raise OperationError(f"Division overflow: {str(e)}")  # pragma: no cover

    @staticmethod
    def pow(a: float, b: float) -> float:
        """
        Raises *a* to the power of *b*
        **Params**
            - *a (float)*: First float value
            - *b (float)*: Second float value
        **Returns**
            - *float*: Power of *a* to the *b*
        """
        try:
            if a == 0 and b < 0:
                raise OperationError("Zero raised to negative power is undefined")
            return math.pow(a, b)
        except OverflowError as e:
            raise OperationError(f"Power overflow: {str(e)}")  # pragma: no cover

    @staticmethod
    def root(a: float, b: float) -> float:
        """
        Computes the *b*-th root of *a*
        **Params**
            - *a (float)*: First float value
            - *b (float)*: Second float value
        **Returns**
            - *float*: Root of *a* with index *b*
        """
        if b == 0:
            raise OperationError("Root with zero index is undefined")
        if a < 0 and b % 2 == 0:
            raise OperationError("Even root of negative number is undefined")
        try:
            return math.pow(a, 1 / b)
        except OverflowError as e:
            raise OperationError(f"Root overflow: {str(e)}")  # pragma: no cover

    @staticmethod
    def modulo(a: float, b: float) -> float:
        """
        Computes modulo of two values of type float
        **Params**
            - *a (float)*: First float value
            - *b (float)*: Second float value
        **Returns**
            - *float*: Modulo of *a* and *b*
        """
        if b == 0:
            raise OperationError("Divide By Zero Error")
        try:
            return a % b
        except OverflowError as e:
            raise OperationError(f"Modulo overflow: {str(e)}")  # pragma: no cover

    @staticmethod
    def intDivide(a: float, b: float) -> float:
        """
        Divides two values of type float, removing remainder
        **Params**
            - *a (float)*: First float value
            - *b (float)*: Second float value
        **Returns**
            - *float*: Integer division of *a* and *b*
        """
        if b == 0:
            raise OperationError("Divide By Zero Error")
        try:
            return a // b
        except OverflowError as e:
            raise OperationError(f"Integer division overflow: {str(e)}")  # pragma: no cover

    @staticmethod
    def percentage(a: float, b: float) -> float:
        """
        Computes percentage of two values of type float
        **Params**
            - *a (float)*: First float value
            - *b (float)*: Second float value
        **Returns**
            - *float*: Percentage of *a* over *b*
        """
        if b == 0:
            raise OperationError("Divide By Zero Error")
        try:
            return (a / b) * 100
        except OverflowError as e:
            raise OperationError(f"Percentage overflow: {str(e)}")  # pragma: no cover

    @staticmethod
    def absSubtraction(a: float, b: float) -> float:
        """
        Subtracts two values of type float and returns absolute value
        **Params**
            - *a (float)*: First float value
            - *b (float)*: Second float value
        **Returns**
            - *float*: Absolute difference of *a* and *b*
        """
        try:
            return abs(a - b)
        except OverflowError as e:
            raise OperationError(f"Absolute subtraction overflow: {str(e)}")  # pragma: no cover
