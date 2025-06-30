import pytest
from app.operations import Operation
from app.exceptions import OperationError

def test_addition():
    assert Operation.addition(2, 3) == 5.0
    assert Operation.addition(-1, 1) == 0.0

def test_subtraction():
    assert Operation.subtraction(5, 2) == 3.0
    assert Operation.subtraction(2, 5) == -3.0

def test_absSubtraction():
    assert Operation.absSubtraction(2, 5) == 3.0
    assert Operation.absSubtraction(5, 2) == 3.0

def test_multiply():
    assert Operation.multiply(4, 3) == 12.0
    assert Operation.multiply(-2, 3) == -6.0

def test_divide():
    assert Operation.divide(10, 2) == 5.0
    with pytest.raises(OperationError, match="Divide By Zero Error"):
        Operation.divide(10, 0)

def test_modulo():
    assert Operation.modulo(10, 3) == 1.0
    with pytest.raises(OperationError, match="Divide By Zero Error"):
        Operation.modulo(10, 0)

def test_percentage():
    assert Operation.percentage(50, 200) == 25.0
    with pytest.raises(OperationError, match="Divide By Zero Error"):
        Operation.percentage(50, 0)

def test_intDivide():
    assert Operation.intDivide(10, 3) == 3.0
    with pytest.raises(OperationError, match="Divide By Zero Error"):
        Operation.intDivide(10, 0)

def test_pow():
    assert Operation.pow(2, 3) == 8.0
    with pytest.raises(OperationError, match="Zero raised to negative power is undefined"):
        Operation.pow(0, -1)

def test_root():
    assert Operation.root(16, 2) == 4.0
    with pytest.raises(OperationError, match="Root with zero index is undefined"):
        Operation.root(16, 0)
    with pytest.raises(OperationError, match="Even root of negative number is undefined"):
        Operation.root(-16, 2)
