import tkinter as tk
import math

class Calculator:
    def __init__(self, master):
        self.master = master
        master.title("Calculator")
        master.geometry("350x480")
        master.configure(bg="#333")

        self.display = tk.Entry(master, width=30, borderwidth=5, justify="right", font=("Arial", 18), bg="#444", fg="#eee")
        self.display.grid(row=0, column=0, columnspan=4, padx=10, pady=10, ipady=10)
        self.display.insert(0, "0")
        self.formula = "0"
        self.display.config(state="disabled")

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
            self.result_calculated = False
            self.squared = False
            self.history = ""

    def append(self, char):
        if self.result_calculated:
            if char.isdigit():
                self.formula = char
                self.result_calculated = False
                self.update_display(text=self.formula)
            elif char == '.':
                return
                self.result_calculated = False
                self.update_display(text=self.formula)
            return
        if self.squared:
            if char.isdigit():
                self.formula = char
            elif char == '.':
                self.formula = '0.'
            self.squared = False
            self.update_display()
            return
        elif self.result_calculated:
            self.formula = char if char.isdigit() else '0' + char if char in self.operators else char
            self.result_calculated = False
            self.update_display()
            return
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
            elif self.formula and self.formula[-1] in self.operators:
                self.formula = self.formula[:-1] + char
            else:
                return
        elif char == '(':
            if self.formula and self.formula[-1] == ')':
                if self.formula[-2:] in ['+-', '-*', '/-', '+*', '*+', '/+', '*-', '*+', '/*', '/+', '**2']:
                    pass
                elif len(self.formula) > 1 and self.formula[-2] not in ['+', '-', '*', '/', '(', '**2']:
                    return
            if self.formula and self.formula[-1] == '.':
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
            self.update_display("Error")
        self.update_display()
        self.update_display(text=self.formula)

    def clear(self):
        self.formula = "0"
        self.update_display()

    def delete(self):
        if not self.formula:
            return

        if self.formula == "0":
            return

        self.formula = self.formula[:-1] or "0"
        self.update_display()

    def square(self):
        try:
            if not self.formula or not self.formula[-1].isdigit():
                return
            last_num_index = len(self.formula) - 1
            while last_num_index > 0 and self.formula[last_num_index - 1] not in ['+', '-', '*', '/', '(', ')']:
                last_num_index -= 1
            last_number = self.formula[last_num_index:]
            if last_number.endswith("."):
                last_number = last_number[:-1]
            if last_number == '0' or last_number == "":
                return
            result = str(eval('(' + last_number + ')**2'))
            self.history = last_number + "**2 = "
            self.formula = self.formula[:last_num_index] + result
            self.update_display()
            self.last_input_was_operator = True
            self.decimal_point_allowed = True
            self.squared = True

        except (ValueError, TypeError, IndexError, SyntaxError):
            self.update_display("Error")

    def equals(self):
        if self.result_calculated or self.squared:
            self.update_display("Error")
            return
        if self.paren_count > 0:
            self.update_display("Error")
            return
        try:
            result = str(eval(self.formula))
            self.history = self.formula + " = "
            self.formula = str(result)
            self.has_decimal = '.' in self.formula
            self.decimal_point_allowed = '.' not in self.formula
            self.update_display()
            self.result_calculated = True
        except (SyntaxError, NameError, TypeError, ZeroDivisionError):
            self.update_display("Error")
            self.decimal_point_allowed = True
            self.has_decimal = False
            self.result_calculated = False

    def update_display(self, text=None, history_text=None, history_color="black"):
        if history_text:
            self.display.insert(0, history_text + " ")
            self.display.config(font=("Arial", 10))
            self.display.tag_add("history", "1.0", "1.end")
            self.display.tag_config("history", font=("Arial", 10), foreground=history_color)
        if text:
            self.display.insert(tk.END, text)
            self.display.config(font=("Arial", 18))
        text = text if text is not None else self.formula
        self.display.config(state="normal")
        self.display.delete(0, tk.END)
        self.display.insert(0, text or "0")
        self.display.config(state="disabled")

root = tk.Tk()
calc = Calculator(root)
root.mainloop()