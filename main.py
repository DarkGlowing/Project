import tkinter as tk
import math

class Calculator:
    def __init__(self, master):
        self.master = master
        master.title("Calculator")
        master.geometry("330x450")
        master.configure(bg="#FFF0F5")

        self.display = tk.Entry(master, width=30, borderwidth=5, justify="right", font=("Segoe UI Black", 20), bg="#F8F8FF", fg="#030303")
        self.display.grid(row=0, column=0, columnspan=4, padx=10, pady=10, ipady=10)
        self.display.insert(0, "0")
        self.formula = "0"
        self.display.config(state="disabled")

        buttons = [
            ("±", self.sqrt), ("%", self.square), ("C", self.clear), ("⌫", self.delete),
            ("x!", self.sqrt), ("x²", self.square), ("√x", self.sqrt), ("÷", lambda: self.append("/")),
            ("7", lambda: self.append("7")), ("8", lambda: self.append("8")), ("9", lambda: self.append("9")), ("×", lambda: self.append("*")),
            ("4", lambda: self.append("4")), ("5", lambda: self.append("5")), ("6", lambda: self.append("6")), ("-", lambda: self.append("-")),
            ("1", lambda: self.append("1")), ("2", lambda: self.append("2")), ("3", lambda: self.append("3")), ("+", lambda: self.append("+")),
            ("()", lambda: self.append("()")), ("0", lambda: self.append("0")), (".", lambda: self.append(".")), ("=", self.equals)
        ]

        row = 1
        col = 0

        for text, command in buttons:
            button_bg = "#F8F8FF"
            button_fg = "#030303"

            if text == "=":
                button_bg = "#8A3324"
                button_fg = "#FFF0F5"
            if text in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]:
                button_bg = "#FCFCFC"
                button_fg = "#030303"

            button = tk.Button(master, text=text, padx=2, pady=2, command=command, font=("Segoe UI Black", 18), bg=button_bg, fg=button_fg, relief='ridge', activebackground="#DCDCDC", activeforeground="#030303")
            button.grid(row=row, column=col, padx=1, pady=1, sticky="nsew")
            col += 1
            if col > 3:
                col = 0
                row += 1

        for i in range(4):
            master.columnconfigure(i, weight=1)
            self.last_input_was_number = False
            self.last_input_was_operator = False
            self.operators = ['+', '-', '*', '/', '**2', '√x']
            self.decimal_point_allowed = True
            self.has_decimal = False
            self.paren_count = 0
            self.result_calculated = False
            self.squared = False
            self.history = ""
            self.locked = False
            self.last_input_type = ""
            self.consecutive_digits = 0
            self.after_sqrt = False
            self.last_operation = None

    def append(self, char):
        if '.' in self.formula:
            decimal_part = self.formula.split('.')[1]
            if decimal_part and decimal_part[-1] == '0' and len(decimal_part) >= 5:
                self.locked = True
            else:
                self.locked = False
        if char in ['+', '-', '*', '/', '()', '**2', '.']:
            self.last_operation = char
        if self.locked:
            self.update_display("Error 104")
            return
        if self.after_sqrt and char == '.':
            return

        if self.result_calculated and char.isdigit():
            self.formula = char
            self.result_calculated = False
            self.after_sqrt = False
            self.update_display(text=self.formula)
            return
        elif self.result_calculated and char == '.':
            self.formula = '.'
            self.result_calculated = False
            self.after_sqrt = False
            self.update_display(text=self.formula)
        elif self.result_calculated:
            return

        if char == '√x':
            self.after_sqrt = True
            self.last_operation = '√x'
            self.formula += char
            self.consecutive_digits = 0

            self.consecutive_digits = 0
        if self.squared:
            if char.isdigit():
                self.formula = char
            elif char == '.':
                self.formula = '0.'
            self.squared = False
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
        elif self.formula == "0" and char in ['+', '-', '*', '/', '**2', '√x']:
            self.formula += char
        elif self.formula == "0" and char == '.':
            self.formula += char
        elif self.formula == "0":
            return

        elif char.isdigit():
            if self.consecutive_digits >= 6:
                return
            if self.formula and self.formula[-1] == ')':
                return
            if '.' in self.formula and len(self.formula.split('.')[1]) >= 5:
                return
            self.formula += char
            self.consecutive_digits += 1
            self.last_input_was_number = True
            self.last_input_was_operator = False
            self.decimal_point_allowed = True
            self.has_decimal = False
        elif char in ['+', '-', '*', '/', '**2', '√x', '.']:
            if char == '.' and '.' in self.formula:
                return
            if self.formula and self.formula[-1] in ['+', '-', '*', '/', '**2', '√x']:
                return
                #self.formula = self.formula[:-1] + char
            if char == '.':
                if self.last_operation == '√x':
                    return
            else:
                self.formula += char
            self.consecutive_digits = 0
        if char == '.':
            if '.' in self.formula:
                return
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
            if self.formula and self.formula[-1].isdigit():
                self.formula += char
                self.consecutive_digits = 0
                self.last_input_was_number = False
                self.last_input_was_operator = True
                self.decimal_point_allowed = True
                self.has_decimal = False
            elif self.formula and self.formula[-1] in self.operators:
                self.formula = self.formula[:-1] + char
                self.last_input_was_operator = True
            else:
                return
        elif char == '()':
            if self.paren_count == 0:
                if self.formula and self.formula[-1] == ')':
                    if self.formula[-2:] in ['+-', '-*', '/-', '+*', '*+', '/+', '*-', '*+', '/*', '/+', '**2', '√x']:
                        pass
                    elif len(self.formula) > 1 and self.formula[-2] not in ['+', '-', '*', '/', '(', '**2', '√x']:
                        return
                if self.formula and self.formula[-1] == '.':
                    return
                if self.formula and self.formula[-1].isdigit():
                    return
                if self.paren_count > 0 and self.formula and self.formula[-1] != '(':
                    return
                if self.formula and self.formula[-1] == '(':
                    return
                self.formula += "("
                self.paren_count += 1
                self.last_input_was_operator = True
            else:
                if self.paren_count <= 0:
                    return
                if self.formula and not self.formula[-1].isdigit():
                    return
                self.formula += ")"
                self.paren_count -= 1
                self.last_input_was_operator = True
        #elif char == ')':
          #  if self.paren_count <= 0:
          #      return
          #  if self.formula and not self.formula[-1].isdigit():
          #      return
          #  self.formula += char
          #  self.paren_count -= 1
          #  self.last_input_was_operator = True
        else:
            self.update_display("Error 105")
        if char.isdigit() or char == '.':
            self.last_input_type = "digit"
        elif char in ['+', '-', '*', '/', '()', '**2', '√x']:
            self.last_input_type = "operator"
        else:
            self.last_input_type = ""
        self.update_display()
        self.update_display(text=self.formula)

    def clear(self):
        self.formula = "0"
        self.update_display()
        self.locked = False
        self.paren_count = 0
        self.consecutive_digits = 0

    def count_digits_before_operator(self, formula):
        count = 0
        i = len(formula) - 1
        while i >= 0 and formula[i] not in ['+', '-', '*', '/', '(', ')', '**2', '.', '√x']:
            if formula[i].isdigit():
                count += 1
            i -= 1
        return count

    def sqrt(self):
        if not self.formula:
            return
        if self.formula == "0":
            return  # Prevent sqrt operation on zero
        elif not self.formula or not self.formula.strip():  # проверка на пустоту
            self.update_display("Error 106")
            return
        try:
            result = math.sqrt(float(self.formula))
            self.formula = str(result)
            self.update_display()
            self.result_calculated = True
            self.after_sqrt = False
        except ValueError:
            self.update_display("Error 106")
        except OverflowError:
            self.update_display("Error 106")

    def delete(self):
        if not self.formula:
            return
        if self.formula == "0":
            return
        if self.formula and self.formula[-1] in ['+', '-', '*', '/', '(', ')', '**2', '√x']:
            self.formula = self.formula[:-1]
            self.consecutive_digits = self.count_digits_before_operator(self.formula)
        else:
            i = len(self.formula) - 1
            while i >= 0 and (self.formula[i].isdigit() or self.formula[i] == '.'):
                i -= 1
            self.formula = self.formula[:i + 1]
            self.consecutive_digits = 0
        if not self.formula:
            self.formula = "0"
        self.update_display()
        self.locked = False

    def square(self):
        try:
            if not self.formula or not self.formula[-1].isdigit():
                return
            last_num_index = len(self.formula) - 1
            while last_num_index > 0 and self.formula[last_num_index - 1] not in ['+', '-', '*', '/', '(', ')', '√x']:
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
            self.update_display("Error 101")

    def equals(self):
        if self.result_calculated or self.squared:
            self.update_display("Error 102")
            return
        if self.paren_count > 0:
            self.update_display("Error 103")
            return
        if '.' in self.formula:
            decimal_part = self.formula.split('.')[1]
            if decimal_part and decimal_part[-1] == '0' and len(decimal_part) >= 5:
                self.locked = True
            else:
                self.locked = False
        if self.locked:
            self.update_display("Error 104")
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
            self.update_display("Error 101")
            self.decimal_point_allowed = True
            self.has_decimal = False
            self.result_calculated = False

    def update_display(self, text=None):
        if text:
            self.display.insert(tk.END, text)
            self.display.config(font=("Segoe UI Black", 20))
        text = text if text is not None else self.formula
        self.display.config(state="normal")
        self.display.delete(0, tk.END)
        self.display.insert(0, text or "0")
        self.display.config(state="disabled")

root = tk.Tk()
calc = Calculator(root)
root.mainloop()