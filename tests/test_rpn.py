"""Unit tests for the core RPN evaluator."""

import math

import pytest

from app.rpn import RPNError, evaluate


def test_happy_path_simple_addition():
    assert evaluate("3 4 +") == 7


def test_precedence_via_rpn_order():
    # (3 + 4) * 2 = 14, expressed in RPN without needing parentheses.
    assert evaluate("3 4 + 2 *") == 14


def test_precedence_via_rpn_order_division_first():
    # 5 + (6 / 3) = 7
    assert evaluate("5 6 3 / +") == 7


def test_subtraction():
    assert evaluate("10 4 -") == 6


def test_multiplication():
    assert evaluate("6 7 *") == 42


def test_division():
    assert evaluate("20 4 /") == 5


def test_power():
    assert evaluate("2 10 ^") == 1024


def test_sqrt():
    assert evaluate("16 sqrt") == 4


def test_sin():
    assert evaluate("0 sin") == pytest.approx(0)


def test_cos():
    assert evaluate("0 cos") == pytest.approx(1)


def test_tan():
    assert evaluate("0 tan") == pytest.approx(0)


def test_log_natural():
    assert evaluate(f"{math.e} log") == pytest.approx(1)


def test_complex_expression_combining_multiple_operators():
    # sqrt(3^2 + 4^2) = 5
    assert evaluate("3 2 ^ 4 2 ^ + sqrt") == pytest.approx(5)


def test_negative_numbers_are_parsed_correctly():
    assert evaluate("-5 3 +") == -2


def test_error_stack_underflow_binary_operator():
    with pytest.raises(RPNError, match="stack underflow"):
        evaluate("3 +")


def test_error_stack_underflow_unary_operator():
    with pytest.raises(RPNError, match="stack underflow"):
        evaluate("sqrt")


def test_error_division_by_zero():
    with pytest.raises(RPNError, match="division by zero"):
        evaluate("5 0 /")


def test_error_unknown_operator():
    with pytest.raises(RPNError, match="invalid token"):
        evaluate("3 4 %")


def test_error_non_numeric_token():
    with pytest.raises(RPNError, match="invalid token"):
        evaluate("3 abc +")


def test_error_empty_expression():
    with pytest.raises(RPNError, match="empty expression"):
        evaluate("")


def test_error_too_many_operands_left_on_stack():
    with pytest.raises(RPNError, match="invalid expression"):
        evaluate("1 2 3 +")


def test_error_sqrt_of_negative():
    with pytest.raises(RPNError, match="sqrt of negative"):
        evaluate("-4 sqrt")


def test_error_log_of_non_positive():
    with pytest.raises(RPNError, match="log of non-positive"):
        evaluate("0 log")
