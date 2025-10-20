"""Smart Calculator GUI

A modern desktop calculator app using ttkbootstrap (dark theme).

Features:
- Dark theme (ttkbootstrap)
- Basic + scientific buttons
- Smart English parsing for simple phrases (add/multiply/subtract/divide/power/sqrt)
- Safe evaluation using a restricted math namespace
- History panel with newest results on top
- Enter key binding to evaluate

Requires: Python 3.7+ and ttkbootstrap installed
"""

from __future__ import annotations

import math
import re
import sys
import tkinter as tk
from typing import Optional

import ttkbootstrap as ttk
from ttkbootstrap.constants import *


# ---------------------
# Smart expression parser
# ---------------------


def parse_smart_expression(text: str) -> str:
    """Convert simple English math phrases into a Python expression string.

    Examples:
    - "add 4 and 5" -> "4 + 5"
    - "subtract 9 from 20" -> "20 - 9"
    - "multiply 7 by 8" -> "7 * 8"
    - "divide 10 by 2" -> "10 / 2"
    - "sqrt(16) + sin(30)" -> unchanged (sin uses degrees in evaluator)

    This function performs conservative replacements and returns a best-effort
    Python expression. It does NOT evaluate the expression.
    """
    if not isinstance(text, str):
        return ""

    s = text.strip()
    if not s:
        return ""

    # normalize whitespace and lowercase for pattern matching, but keep original tokens where helpful
    original = s
    s = s.lower()

    # common pattern replacements first (handle the English sentence forms)
    # subtract X from Y -> Y - X
    s = re.sub(r"subtract\s+([\w\.\(\)]+)\s+from\s+([\w\.\(\)]+)", r"(\2 - \1)", s)

    # add X and Y -> X + Y
    s = re.sub(r"add\s+([\w\.\(\)]+)\s+and\s+([\w\.\(\)]+)", r"(\1 + \2)", s)

    # multiply X by Y -> X * Y
    s = re.sub(r"multiply\s+([\w\.\(\)]+)\s+by\s+([\w\.\(\)]+)", r"(\1 * \2)", s)

    # divide X by Y -> X / Y
    s = re.sub(r"divide\s+([\w\.\(\)]+)\s+by\s+([\w\.\(\)]+)", r"(\1 / \2)", s)

    # phrases like "what is" or "calculate" -> remove them
    s = re.sub(r"\b(what is|calculate|compute|please|=)\b", "", s)

    # convert 'power X to Y' or 'power X by Y' -> X ** Y
    s = re.sub(r"power\s+([\w\.\(\)]+)\s+(to|by|and)\s+([\w\.\(\)]+)", r"(\1 ** \3)", s)

    # standalone words -> symbols
    word_map = {
        r"\band\b": "+",
        r"\bplus\b": "+",
        r"\bminus\b": "-",
        r"\btimes\b": "*",
        r"\bmultiplied by\b": "*",
        r"\bover\b": "/",
        r"\bdivided by\b": "/",
        r"\bdivide\b": "/",
        r"\badd\b": "+",
        r"\bsubtract\b": "-",
        r"\bpower\b": "**",
        r"\bpercent\b": "%",
        r"\bpercent of\b": "%",
    }

    for patt, repl in word_map.items():
        s = re.sub(patt, repl, s)

    # attach parentheses for trig/log/sqrt if user writes like 'sin 30' -> 'sin(30)'
    func_names = ["sin", "cos", "tan", "asin", "acos", "atan", "sqrt", "log", "log10"]

    for fn in func_names:
        # only replace when function name is followed by a space + value (not already with parentheses)
        s = re.sub(rf"\b{fn}\s+([-\w\.\(\)]+)", rf"{fn}(\1)", s)

    # replace caret '^' (common user notation) with python power operator
    s = s.replace("^", "**")

    # collapse multiple spaces
    s = re.sub(r"\s+", " ", s).strip()

    # If parsing produced an empty string, fall back to original input (safe)
    return s or original


# ---------------------
# Safe evaluator
# ---------------------


def _safe_math_namespace() -> dict:
    """Return a restricted namespace with math functions and degree-based trig wrappers."""
    allowed: dict = {}

    # Import math functions/constants except private names
    for name, val in math.__dict__.items():
        if not name.startswith("__"):
            allowed[name] = val

    # Override trig functions to accept degrees (more natural for this calculator)
    def sin_deg(x):
        return math.sin(math.radians(float(x)))

    def cos_deg(x):
        return math.cos(math.radians(float(x)))

    def tan_deg(x):
        return math.tan(math.radians(float(x)))

    def asin_deg(x):
        if x < -1 or x > 1:
            raise ValueError("asin input must be in [-1,1]")
        return math.degrees(math.asin(float(x)))

    def acos_deg(x):
        if x < -1 or x > 1:
            raise ValueError("acos input must be in [-1,1]")
        return math.degrees(math.acos(float(x)))

    def atan_deg(x):
        return math.degrees(math.atan(float(x)))

    allowed.update(
        {
            "sin": sin_deg,
            "cos": cos_deg,
            "tan": tan_deg,
            "asin": asin_deg,
            "acos": acos_deg,
            "atan": atan_deg,
            # keep sqrt/log as-is (math.sqrt, math.log, math.log10 already present)
            "abs": abs,
            "round": round,
            # provide a safe alias for power
            "pow": pow,
        }
    )

    # constants
    allowed["pi"] = math.pi
    allowed["e"] = math.e

    return allowed


def evaluate_expression_safe(expr: str) -> float:
    """Evaluate expression using a restricted math namespace.

    Raises ValueError on invalid or non-numeric results.
    """
    if not expr or not expr.strip():
        raise ValueError("Empty expression")

    # Build safe globals
    safe_globals = {"__builtins__": None}
    safe_globals.update(_safe_math_namespace())

    # Prevent accidental attribute access like '__' or double-underscores
    if "__" in expr:
        raise ValueError("Invalid expression")

    try:
        result = eval(expr, safe_globals, {})
    except Exception as exc:
        raise ValueError(f"Error evaluating expression: {exc}") from exc

    # Accept ints/floats, or convertible to float
    if isinstance(result, (int, float)):
        return float(result)

    try:
        return float(result)
    except Exception:
        raise ValueError("Expression did not evaluate to a numeric result")


# ---------------------
# GUI
# ---------------------


class SmartCalculatorApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Smart Calculator")
        self.root.geometry("800x500")
        self.root.minsize(700, 450)

        # Fonts and styles
        self.display_font = ("Segoe UI", 18, "bold")
        self.button_font = ("Segoe UI", 12)

        # Main layout frames
        self.top_frame = ttk.Frame(self.root, padding=10)
        self.center_frame = ttk.Frame(self.root, padding=6)
        self.right_frame = ttk.Frame(self.root, padding=6)

        self.top_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")
        self.center_frame.grid(row=1, column=0, sticky="nsew")
        self.right_frame.grid(row=1, column=1, sticky="nsew")

        # configure grid weights
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=3)
        self.root.grid_columnconfigure(1, weight=1)

        self._build_top()
        self._build_buttons()
        self._build_history()

        # Bind Enter to calculate
        self.root.bind("<Return>", lambda event: self.calculate())

    def _build_top(self):
        # Input entry
        self.input_var = tk.StringVar()
        self.input_entry = ttk.Entry(
            self.top_frame, textvariable=self.input_var, font=self.display_font
        )
        self.input_entry.pack(fill="x", padx=6, pady=(0, 6))

        # Result label
        self.result_var = tk.StringVar(value="")
        self.result_label = ttk.Label(
            self.top_frame,
            textvariable=self.result_var,
            font=self.display_font,
            anchor="e",
        )
        self.result_label.pack(fill="x", padx=6)

    def _build_buttons(self):
        # Buttons layout: typical calculator layout
        btns = [
            ["7", "8", "9", "/", "sqrt"],
            ["4", "5", "6", "*", "pow"],
            ["1", "2", "3", "-", "log"],
            ["0", ".", "%", "+", "sin"],
            ["(", ")", "C", "←", "cos"],
            ["Clear History", "Ans", "=", "tan", " "],
        ]

        for r, row in enumerate(btns):
            for c, key in enumerate(row):
                if not key.strip():
                    continue
                btn = ttk.Button(
                    self.center_frame,
                    text=key,
                    bootstyle="secondary",
                    width=10,
                    command=lambda k=key: self.on_button(k),
                )
                btn.grid(row=r, column=c, padx=4, pady=4, sticky="nsew")

        # make columns expand evenly
        for i in range(5):
            self.center_frame.grid_columnconfigure(i, weight=1)

    def _build_history(self):
        # Title and buttons
        title = ttk.Label(
            self.right_frame, text="History", font=("Segoe UI", 12, "bold")
        )
        title.pack(anchor="w")

        # Scrollable listbox
        self.history_box = tk.Listbox(self.right_frame, height=20, activestyle="none")
        self.history_box.pack(
            side="left", fill="both", expand=True, padx=(0, 4), pady=6
        )

        scrollbar = ttk.Scrollbar(
            self.right_frame, orient="vertical", command=self.history_box.yview
        )
        scrollbar.pack(side="right", fill="y")
        self.history_box.config(yscrollcommand=scrollbar.set)

        # Control buttons
        clear_btn = ttk.Button(
            self.right_frame,
            text="Clear History",
            bootstyle="danger",
            command=self.clear_history,
        )
        clear_btn.pack(fill="x", pady=(6, 0))

        # Allow double-click on history to paste expression into input
        self.history_box.bind("<Double-1>", self.on_history_double)

    def on_button(self, key: str):
        if key == "C":
            self.input_var.set("")
            self.result_var.set("")
            return
        if key == "←":
            cur = self.input_var.get()
            self.input_var.set(cur[:-1])
            return
        if key == "Clear History":
            self.clear_history()
            return
        if key == "Ans":
            # insert last result
            last = self.result_var.get()
            if last:
                self._insert_text(str(last))
            return
        if key == "=":
            self.calculate()
            return

        # For functions, insert as func(...), for pow insert '^'
        if key in ("sqrt", "log", "sin", "cos", "tan", "pow"):
            if key == "pow":
                # insert caret for user-friendly power, will be converted to ** on parse
                self._insert_text("^")
            else:
                # insert function name and an opening paren so user can type the argument
                self._insert_text(f"{key}(")
            return

        # default: append the key
        self._insert_text(key)

    def _insert_text(self, txt: str):
        cur = self.input_var.get()
        # place at the end
        self.input_var.set(cur + txt)
        # focus back to entry
        self.input_entry.focus()
        # move cursor to end
        self.input_entry.icursor("end")

    def calculate(self):
        expr_in = self.input_var.get().strip()
        if not expr_in:
            return

        parsed = parse_smart_expression(expr_in)
        # convert caret to Python power operator (if any remained)
        parsed = parsed.replace("^", "**")

        try:
            result = evaluate_expression_safe(parsed)
        except Exception as exc:
            self.result_var.set(f"Error: {exc}")
            return

        # format result nicely
        if result.is_integer():
            display = str(int(result))
        else:
            display = str(round(result, 12)).rstrip("0").rstrip(".")

        self.result_var.set(display)
        # add to top of history: show the original user input for clarity
        hist_line = f"{expr_in} = {display}"
        self.history_box.insert(0, hist_line)

        # keep entry to the result so user can continue calculations if desired
        self.input_var.set(display)

    def clear_history(self):
        self.history_box.delete(0, "end")

    def on_history_double(self, event):
        sel = self.history_box.curselection()
        if not sel:
            return
        line = self.history_box.get(sel[0])
        # line is like 'expr = result' — put the expr into input
        if " = " in line:
            expr, _ = line.split(" = ", 1)
            self.input_var.set(expr)
        else:
            self.input_var.set(line)


# ---------------------
# Entrypoint
# ---------------------


def main():
    # Initialize ttkbootstrap style with a dark theme
    style = ttk.Style(theme="darkly")
    root = style.master

    app = SmartCalculatorApp(root)

    # Focus input on start
    app.input_entry.focus()

    root.mainloop()


if __name__ == "__main__":
    main()
