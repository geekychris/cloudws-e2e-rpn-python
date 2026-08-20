"""Core evaluator for Reverse Polish Notation (RPN) scientific expressions."""

import math

BINARY_OPERATORS = {"+", "-", "*", "/", "^"}
UNARY_OPERATORS = {"sqrt", "sin", "cos", "tan", "log"}


class RPNError(ValueError):
    """Raised when an RPN expression cannot be evaluated."""


def _apply_binary(op: str, a: float, b: float) -> float:
    if op == "+":
        return a + b
    if op == "-":
        return a - b
    if op == "*":
        return a * b
    if op == "/":
        if b == 0:
            raise RPNError("division by zero")
        return a / b
    if op == "^":
        try:
            return a**b
        except (ValueError, OverflowError) as exc:
            raise RPNError(f"invalid operands for '^': {a}, {b}") from exc
    raise RPNError(f"unknown operator: {op!r}")


def _apply_unary(op: str, a: float) -> float:
    if op == "sqrt":
        if a < 0:
            raise RPNError(f"sqrt of negative number: {a}")
        return math.sqrt(a)
    if op == "sin":
        return math.sin(a)
    if op == "cos":
        return math.cos(a)
    if op == "tan":
        return math.tan(a)
    if op == "log":
        if a <= 0:
            raise RPNError(f"log of non-positive number: {a}")
        return math.log(a)
    raise RPNError(f"unknown operator: {op!r}")


def evaluate(expression: str) -> float:
    """Evaluate a space-separated RPN expression and return the numeric result."""
    tokens = expression.strip().split()
    if not tokens:
        raise RPNError("empty expression")

    stack: list[float] = []

    for token in tokens:
        if token in BINARY_OPERATORS:
            if len(stack) < 2:
                raise RPNError(
                    f"stack underflow: operator '{token}' requires 2 operands, "
                    f"but only {len(stack)} available"
                )
            b = stack.pop()
            a = stack.pop()
            stack.append(_apply_binary(token, a, b))
            continue

        if token in UNARY_OPERATORS:
            if len(stack) < 1:
                raise RPNError(
                    f"stack underflow: operator '{token}' requires 1 operand, "
                    f"but only {len(stack)} available"
                )
            a = stack.pop()
            stack.append(_apply_unary(token, a))
            continue

        try:
            stack.append(float(token))
        except ValueError as exc:
            raise RPNError(f"invalid token: {token!r} is not a number or known operator") from exc

    if len(stack) != 1:
        raise RPNError(
            f"invalid expression: {len(stack)} values remain on the stack after evaluation "
            "(expected exactly 1)"
        )

    return stack[0]
