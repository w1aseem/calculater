"""A small scientific calculator module with input validation, a console menu,
and helper hooks for GUI integration.

This refactor fixes logic issues, adds validation and error handling, and
provides a clearer structure for extending (e.g. tkinter GUI).
"""

from __future__ import annotations

import math
from typing import Callable, Dict, List, Optional, Tuple, Union


Number = Union[int, float]


def add(x: Number, y: Number) -> float:
    return float(x + y)


def subtract(x: Number, y: Number) -> float:
    return float(x - y)


def multiply(x: Number, y: Number) -> float:
    return float(x * y)


def divide(x: Number, y: Number) -> float:
    if y == 0:
        raise ZeroDivisionError("Division by zero")
    return float(x / y)


def exponent(x: Number, y: Number) -> float:
    return float(x**y)


def modulus(x: Number, y: Number) -> float:
    if y == 0:
        raise ZeroDivisionError("Modulus by zero")
    return float(x % y)


def floor_divide(x: Number, y: Number) -> int:
    if y == 0:
        raise ZeroDivisionError("Floor division by zero")
    return int(x // y)


# single-input operations


def square_root(x: Number) -> float:
    if x < 0:
        raise ValueError("Square root of negative number")
    return math.sqrt(x)


def log10(x: Number) -> float:
    if x <= 0:
        raise ValueError("log10 undefined for non-positive numbers")
    return math.log10(x)


def natural_log(x: Number) -> float:
    if x <= 0:
        raise ValueError("ln undefined for non-positive numbers")
    return math.log(x)


def sine(x: Number) -> float:
    # expects degrees
    return math.sin(math.radians(float(x)))


def cosine(x: Number) -> float:
    return math.cos(math.radians(float(x)))


def tangent(x: Number) -> float:
    return math.tan(math.radians(float(x)))


def factorial(x: Number) -> int:
    # math.factorial requires an integer >= 0
    if not float(x).is_integer():
        raise ValueError("factorial requires an integer value")
    n = int(x)
    if n < 0:
        raise ValueError("factorial not defined for negative integers")
    return math.factorial(n)


def absolute(x: Number) -> float:
    return abs(x)


def power_of_ten(x: Number) -> float:
    return float(10**x)


def to_radians(x: Number) -> float:
    return math.radians(float(x))


def to_degrees(x: Number) -> float:
    return math.degrees(float(x))


def sign(x: Number) -> int:
    if x > 0:
        return 1
    if x < 0:
        return -1
    return 0


def sinh(x: Number) -> float:
    return math.sinh(float(x))


def cosh(x: Number) -> float:
    return math.cosh(float(x))


def tanh(x: Number) -> float:
    return math.tanh(float(x))


def asin(x: Number) -> float:
    if x < -1 or x > 1:
        raise ValueError("asin input must be in [-1, 1]")
    # return degrees
    return math.degrees(math.asin(float(x)))


def acos(x: Number) -> float:
    if x < -1 or x > 1:
        raise ValueError("acos input must be in [-1, 1]")
    return math.degrees(math.acos(float(x)))


def atan(x: Number) -> float:
    return math.degrees(math.atan(float(x)))


# two-input and multi-input utilities


def clamp(x: Number, min_value: Number, max_value: Number) -> float:
    if min_value > max_value:
        raise ValueError("min_value cannot be greater than max_value")
    return float(max(min(x, max_value), min_value))


def percentage(x: Number, percent: Number) -> float:
    return float((x * percent) / 100.0)


def gcd(x: Number, y: Number) -> int:
    return math.gcd(int(x), int(y))


def lcm(x: Number, y: Number) -> int:
    a, b = int(x), int(y)
    if a == 0 or b == 0:
        return 0
    return abs(a * b) // math.gcd(a, b)


def log_custom(x: Number, base: Number) -> float:
    if x <= 0 or base <= 0 or base == 1:
        raise ValueError("log undefined for given x/base")
    return math.log(x, base)


# Menu and input helpers


UNARY_OPS: Dict[str, Tuple[str, Callable[[Number], Number]]] = {
    "7": ("square_root", square_root),
    "9": ("log10", log10),
    "10": ("ln", natural_log),
    "11": ("sin (deg)", sine),
    "12": ("cos (deg)", cosine),
    "13": ("tan (deg)", tangent),
    "14": ("factorial", factorial),
    "15": ("abs", absolute),
    "16": ("10^x", power_of_ten),
    "17": ("to radians", to_radians),
    "18": ("to degrees", to_degrees),
    "19": ("sign", sign),
    "25": ("sinh", sinh),
    "26": ("cosh", cosh),
    "27": ("tanh", tanh),
    "28": ("asin (return deg)", asin),
    "29": ("acos (return deg)", acos),
    "30": ("atan (return deg)", atan),
}


BINARY_OPS: Dict[str, Tuple[str, Callable[..., Number]]] = {
    "1": ("add", add),
    "2": ("subtract", subtract),
    "3": ("multiply", multiply),
    "4": ("divide", divide),
    "5": ("exponent", exponent),
    "6": ("modulus", modulus),
    "8": ("floor_divide", floor_divide),
    "21": ("percentage", percentage),
    "22": ("gcd", gcd),
    "23": ("lcm", lcm),
    "24": ("log base", log_custom),
}


def print_menu() -> None:
    print("\nSelect operation:")
    print("1. Add")
    print("2. Subtract")
    print("3. Multiply")
    print("4. Divide")
    print("5. Exponent")
    print("6. Modulus")
    print("7. Square root")
    print("8. Floor divide (x // y)")
    print("9. Log base 10")
    print("10. Natural log (ln)")
    print("11. Sine (degrees)")
    print("12. Cosine (degrees)")
    print("13. Tangent (degrees)")
    print("14. Factorial")
    print("15. Absolute value")
    print("16. Power of 10 (10^x)")
    print("17. Convert to radians")
    print("18. Convert to degrees")
    print("19. Sign function")
    print("20. Clamp value")
    print("21. Percentage")
    print("22. GCD")
    print("23. LCM")
    print("24. Log with custom base")
    print("25. Sinh")
    print("26. Cosh")
    print("27. Tanh")
    print("28. Asin (input -1..1, returns degrees)")
    print("29. Acos (input -1..1, returns degrees)")
    print("30. Atan (returns degrees)")
    print("31. Exit")
    print("32. Evaluate full expression")


def _parse_number(raw: str) -> Number:
    # Try int first to preserve integers for factorial/gcd/lcm
    try:
        if raw.strip().lower().endswith("j"):
            raise ValueError
        iv = int(raw)
        return iv
    except Exception:
        try:
            return float(raw)
        except Exception as exc:
            raise ValueError(f"Invalid number: {raw}") from exc


def get_input_number(prompt: str) -> Number:
    raw = input(prompt)
    return _parse_number(raw)


class Calculator:
    """Encapsulates calculator state (history, memory) and the interactive loop.

    This keeps the module usable as both a script and an importable component for
    GUI or tests.
    """

    def __init__(self) -> None:
        self.history: List[str] = []
        self.memory: Optional[Number] = None

    def _show_history(self) -> None:
        print("History:")
        for idx, entry in enumerate(self.history[-50:], start=1):
            print(f"{idx}. {entry}")

    def _handle_unary(self, choice: str) -> None:
        name, func = UNARY_OPS[choice]
        raw = input(f"Enter number for {name}: ")
        x = _parse_number(raw)
        result = func(x)
        print("Result:", result)
        self.history.append(f"{name}({x}) = {result}")
        self.memory = result

    def _handle_binary(self, choice: str) -> None:
        name, func = BINARY_OPS[choice]
        raw1 = input(f"Enter first number for {name}: ")
        raw2 = input(f"Enter second number for {name}: ")
        a = _parse_number(raw1)
        b = _parse_number(raw2)
        result = func(a, b)
        print("Result:", result)
        self.history.append(f"{name}({a}, {b}) = {result}")
        self.memory = result

    def _handle_clamp(self) -> None:
        raw = input("Enter number to be clamped: ")
        raw_min = input("Enter minimum value: ")
        raw_max = input("Enter maximum value: ")
        x = _parse_number(raw)
        mn = _parse_number(raw_min)
        mx = _parse_number(raw_max)
        result = clamp(x, mn, mx)
        print("Result:", result)
        self.history.append(f"clamp({x}, {mn}, {mx}) = {result}")
        self.memory = result

    def _handle_eval(self) -> None:
        expr = input("Enter expression to evaluate: ")
        try:
            result = evaluate_expression(expr, self.memory)
        except Exception as exc:
            print("Error evaluating expression:", exc)
        else:
            print("Result:", result)
            self.history.append(f"eval({expr}) = {result}")
            self.memory = result

    def run(self) -> None:
        while True:
            print_menu()
            choice = input(
                "Enter choice (1-32). You can type 'm' to recall memory, 'h' to show history: "
            ).strip()
            if not choice:
                continue
            if choice.lower() == "h":
                self._show_history()
                continue
            if choice.lower() == "m":
                print(f"Memory: {self.memory}")
                continue
            if choice == "31":
                print("Goodbye")
                break

            try:
                if choice in UNARY_OPS:
                    self._handle_unary(choice)
                    continue

                if choice in BINARY_OPS:
                    self._handle_binary(choice)
                    continue

                if choice == "32":
                    self._handle_eval()
                    continue

                if choice == "20":
                    self._handle_clamp()
                    continue

                print("Unknown choice. Please select a valid option.")

            except Exception as exc:  # catch validation/ValueError/ZeroDivisionError
                print("Error:", exc)


def launch_tkinter() -> None:
    """Launch a minimal tkinter GUI for evaluating expressions.

    This GUI is intentionally small: an entry for expressions, an Evaluate
    button that uses the same safe evaluator, and a label that shows the result.
    Use this as a starting point for a fuller calculator UI.
    """
    try:
        import tkinter as tk
    except Exception:
        print("tkinter not available in this environment")
        return

    calc = Calculator()

    root = tk.Tk()
    root.title("Simple Calculator - Expression Eval")

    expr_var = tk.StringVar()
    result_var = tk.StringVar()

    tk.Label(root, text="Expression:").grid(row=0, column=0, sticky="w")
    tk.Entry(root, textvariable=expr_var, width=40).grid(row=0, column=1, columnspan=2)

    def on_eval() -> None:
        expr = expr_var.get()
        try:
            res = evaluate_expression(expr, calc.memory)
        except Exception as e:
            result_var.set(f"Error: {e}")
        else:
            result_var.set(str(res))
            calc.history.append(f"eval({expr}) = {res}")
            calc.memory = res

    tk.Button(root, text="Evaluate", command=on_eval).grid(row=1, column=1)
    tk.Label(root, textvariable=result_var, fg="blue").grid(row=1, column=2)

    root.mainloop()


def main() -> None:
    """Compatibility main() function that runs the interactive calculator."""
    calc = Calculator()
    calc.run()


def get_operations_for_gui() -> Dict[str, Callable]:
    """Return a flat mapping of operation names to callables for GUI integration.

    Keys are descriptive strings suitable for button labels; values are callables
    that accept the appropriate number of number arguments.
    """
    ops: Dict[str, Callable] = {}
    for k, (name, func) in UNARY_OPS.items():
        ops[name] = func
    for k, (name, func) in BINARY_OPS.items():
        ops[name] = func
    ops["clamp"] = clamp
    return ops


def _safe_math_namespace(memory: Optional[Number] = None) -> Dict[str, object]:
    """Create a safe namespace exposing math functions/constants and a few builtins.

    Excludes any dunder names from math. Adds 'abs', 'round', and memory token 'M'.
    """
    allowed: Dict[str, object] = {}
    for name, val in math.__dict__.items():
        if not name.startswith("__"):
            allowed[name] = val

    # add safe builtins
    allowed["abs"] = abs
    allowed["round"] = round

    # constants alias
    allowed["pi"] = math.pi
    allowed["e"] = math.e

    # memory placeholder
    allowed["M"] = memory

    # Provide degree-based trig helpers to match calculator behavior
    def _sin_deg(x: Number) -> float:
        return math.sin(math.radians(float(x)))

    def _cos_deg(x: Number) -> float:
        return math.cos(math.radians(float(x)))

    def _tan_deg(x: Number) -> float:
        return math.tan(math.radians(float(x)))

    def _asin_deg(x: Number) -> float:
        if x < -1 or x > 1:
            raise ValueError("asin input must be in [-1, 1]")
        return math.degrees(math.asin(float(x)))

    def _acos_deg(x: Number) -> float:
        if x < -1 or x > 1:
            raise ValueError("acos input must be in [-1, 1]")
        return math.degrees(math.acos(float(x)))

    def _atan_deg(x: Number) -> float:
        return math.degrees(math.atan(float(x)))

    allowed["sin"] = _sin_deg
    allowed["cos"] = _cos_deg
    allowed["tan"] = _tan_deg
    allowed["asin"] = _asin_deg
    allowed["acos"] = _acos_deg
    allowed["atan"] = _atan_deg

    return allowed


def evaluate_expression(expr: str, memory: Optional[Number] = None) -> Number:
    """Safely evaluate a math expression using a restricted globals mapping.

    The expression may use functions from the math module (sin, cos, sqrt, etc.),
    builtins abs() and round(), and constants pi/e. The memory variable 'M' is
    available to insert the last result.

    Security: eval() is called with {'__builtins__': None} and a curated globals dict.
    """
    if not isinstance(expr, str) or not expr.strip():
        raise ValueError("Empty expression")

    safe_globals = {"__builtins__": None}
    safe_globals.update(_safe_math_namespace(memory))

    # Locals are empty to prevent access to outer scope
    try:
        # Evaluate the expression
        result = eval(expr, safe_globals, {})
    except Exception as exc:
        # Re-raise common errors with clearer messages
        raise ValueError(f"Error evaluating expression: {exc}") from exc

    if isinstance(result, (int, float)):
        return result
    # allow results that can be converted to float
    try:
        return float(result)
    except Exception:
        raise ValueError("Expression did not evaluate to a numeric result")


if __name__ == "__main__":
    main()
