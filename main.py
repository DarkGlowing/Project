import tkinter as tk
import math

class Calculator:
    def __init__(self, master):
        self.master = master
        master.title("Калькулятор")
        master.geometry("350x480")
        master.configure(bg="#333")

        self.display = tk.Entry(master, width=30, borderwidth=5, justify="right", font=("Arial", 18), bg="#444", fg="#eee")
        self.display.grid(row=0, column=0, columnspan=4, padx=10, pady=10, ipady=10)
        self.display.insert(0, "0")
        self.formula = "0"

        buttons = [
            ("C", self.clear), ("DEL", self.delete), ("*", lambda: self.append("*")), ("/", lambda: self.append("/")),
            ("7", lambda: self.append("7")), ("8", lambda: self.append("8")), ("9", lambda: self.append("9")), ("+", lambda: self.append("+")),
            ("4", lambda: self.append("4")), ("5", lambda: self.append("5")), ("6", lambda: self.append("6")), ("-", lambda: self.append("-")),
            ("1", lambda: self.append("1")), ("2", lambda: self.append("2")), ("3", lambda: self.append("3")), ("=", self.equals),
            ("0", lambda: self.append("0")), (".", lambda: self.append(".")), ("(", lambda: self.append("(")), (")", lambda: self.append(")")),
            ("x²", self.square)
        ]

        row = 1
        col = 0
        for text, command in buttons:
            button = tk.Button(master, text=text, padx=15, pady=10, command=command, font=("Arial", 14), bg="#555", fg="#eee", activebackground="#777", activeforeground="#eee")
            button.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
            col += 1
            if col > 3:
                col = 0
                row += 1

        for i in range(4):
            master.columnconfigure(i, weight=1)
            self.last_input_was_number = False
            self.last_input_was_operator = False
            self.operators = ['+', '-', '*', '/', '**2']
            self.decimal_point_allowed = True
            self.has_decimal = False
            self.paren_count = 0

    def append(self, char):
        if self.formula == "0" and not char.isdigit():
            if char == '.':
                return
                self.last_input_was_number = True
                self.last_input_was_operator = False
                self.decimal_point_allowed = False
                self.has_decimal = True
            else:
                return
        elif self.formula == "0" and char.isdigit():
            self.formula = char
            self.consecutive_digits = 1
            self.last_input_was_number = True
            self.last_input_was_operator = False
            self.decimal_point_allowed = True
            self.has_decimal = False
        elif char.isdigit():
            if self.formula and self.formula[-1] == ')':
                return
            if self.consecutive_digits >= 6:
                return
            self.formula += char
            self.consecutive_digits += 1
            self.last_input_was_number = True
            self.last_input_was_operator = False
        elif char == '.':
            if not self.decimal_point_allowed:
                return
            if self.formula and self.formula[-1] == ')':
                return
            if not self.formula or self.formula[-1] in self.operators:
                self.formula += '0.'
            else:
                self.formula += '.'
            self.last_input_was_number = True
            self.last_input_was_operator = False
            self.decimal_point_allowed = False
        elif char in self.operators:
            if self.formula and self.formula[-1] == ')':
                self.formula += char
                self.last_input_was_operator = True
            elif self.formula and self.formula[-1].isdigit():
                self.formula += char
                self.consecutive_digits = 0
                self.last_input_was_number = False
                self.last_input_was_operator = True
                self.decimal_point_allowed = True
                self.has_decimal = False
            else:
                return
        elif char == '(':
            if self.formula and self.formula[-1] == ')':
                if self.formula[-2:] in ['+-', '-*', '/-', '+*', '*+', '/+', '*-', '*+', '/*', '/+', '**2', '.(', '.)']:
                    pass
                elif len(self.formula) > 1 and self.formula[-2] not in ['+', '-', '*', '/', '(', '**2']:
                    return
            if self.formula and self.formula[-1].isdigit():
                return
            if self.paren_count > 0 and self.formula and self.formula[-1] != '(':
                return
            if self.formula and self.formula[-1] == '(':
                return
            self.formula += char
            self.paren_count += 1
            self.last_input_was_operator = True

        elif char == ')':
            if self.paren_count <= 0:
                return
            if self.formula and not self.formula[-1].isdigit():
                return
            self.formula += char
            self.paren_count -= 1
            self.last_input_was_operator = True
        else:
            self.update_display("Ошибка")
        self.update_display()

    def clear(self):
        self.formula = "0"
        self.update_display()

    def delete(self):
        if not self.formula:
            return

        if self.formula == "0":
            return

        if self.formula[-1:] in ['+', '-', '*', '/', '(', '.', ')']:
            self.formula = self.formula[:-1]

        self.formula = self.formula[:-1] or "0"
        self.update_display()

    def square(self):
        try:
            result = str(math.pow(float(self.formula), 2))
            self.formula = result
            self.update_display()
        except (ValueError, TypeError):
            self.update_display("Ошибка")

    def equals(self):
        if self.paren_count > 0:
            self.update_display("Ошибка")
            return
        try:
            result = eval(self.formula)
            self.formula = str(result)
            self.has_decimal = '.' in self.formula
            self.decimal_point_allowed = '.' not in self.formula
            self.update_display()
        except (SyntaxError, NameError, TypeError, ZeroDivisionError):
            self.update_display("Ошибка")
            self.decimal_point_allowed = True
            self.has_decimal = False

    def update_display(self, text=None):
        text = text if text is not None else self.formula
        self.display.delete(0, tk.END)
        self.display.insert(0, text or "0")

root = tk.Tk()
calc = Calculator(root)
root.mainloop()