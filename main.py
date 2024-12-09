import tkinter as tk
import math
import re

class Calculator:
    def __init__(self, master):
        self.master = master
        master.title("Calculator")
        master.geometry("330x440")
        master.configure(bg="#030303")
        master.minsize(330, 440)

        self.display = tk.Entry(master, width=30, borderwidth=0, justify="center", font=("Segoe UI Black", 20), bg="#030303", fg="#030303")
        self.display.grid(row=0, column=0, columnspan=4, padx=10, pady=10, ipady=10)
        self.display.insert(0, "0")
        self.formula = "0"
        self.display.config(state="disabled")

        buttons = [
            ("x!", self.factorial), ("x²", self.square), ("√x", self.sqrt), ("⌫", self.delete),
            ("C", self.clear), ("()", lambda: self.append("()")), ("%", self.percent), ("÷", lambda: self.append("/")),
            ("7", lambda: self.append("7")), ("8", lambda: self.append("8")), ("9", lambda: self.append("9")), ("×", lambda: self.append("*")),
            ("4", lambda: self.append("4")), ("5", lambda: self.append("5")), ("6", lambda: self.append("6")), ("-", lambda: self.append("-")),
            ("1", lambda: self.append("1")), ("2", lambda: self.append("2")), ("3", lambda: self.append("3")), ("+", lambda: self.append("+")),
            ("±", self.change_sign), ("0", lambda: self.append("0")), (".", lambda: self.append(".")), ("=", self.equals), ("m", self.modul)
        ]

        row = 1
        col = 0

        for text, command in buttons:
            button_bg = "#F8F8FF"
            button_fg = "#030303"
            size = 18

            if text == "=":
                button_bg = "#008B00"
                button_fg = "#FFF0F5"
            if text in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", ".", "±"]:
                button_bg = "#1E1E1E"
                button_fg = "#FFF0F5"
            if text in ["()", "%", "÷", "×", "-", "+", "x!", "x²", "√x", "⌫"]:
                button_bg = "#1F1F1F"
                button_fg = "#66CD00"
            if text == "C":
                button_bg = "#1F1F1F"
                button_fg = "#FF4040"

            button = tk.Button(master, text=text, padx=2, pady=2, command=command, font=("Segoe UI Black", size), bg=button_bg, fg=button_fg, relief='ridge', activebackground="#DCDCDC", activeforeground="#030303")
            button.grid(row=row, column=col, padx=1, pady=1, sticky="nsew")
            col += 1
            if col > 3:
                col = 0
                row += 1

        for i in range(row):
            master.rowconfigure(i, weight=1)
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

        if char in self.operators and self.formula[-1] == '.':
            return

        if self.result_calculated and char.isdigit():
            self.formula = char
            self.result_calculated = False
            self.after_sqrt = False
            self.update_display(text=self.formula)
            return
        elif self.result_calculated and char == '.':
            self.result_calculated = False
            self.after_sqrt = False
            self.update_display(text=self.formula)
            return
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

        if self.formula == "0" and char == '()':
            self.formula = "("
            self.paren_count += 1
            self.last_input_was_operator = True
            self.update_display(self.formula)

        if self.formula == "0" and char == '.':
            self.formula += char
            self.update_display(self.formula)

        if self.formula == "0" and not char.isdigit():
            if char == '.':
                return
                self.last_input_was_number = True
                self.last_input_was_operator = False
                self.decimal_point_allowed = False
                self.has_decimal = True
            else:
                return

        elif self.formula[0] == "0" and char.isdigit():
            self.formula = char
            self.consecutive_digits = 1
            self.last_input_was_number = True
            self.last_input_was_operator = False
            self.decimal_point_allowed = True
            self.has_decimal = False

        elif self.formula[-1] == '0' and self.formula[-2] in self.operators:
            if char.isdigit():
                self.formula = self.formula[:-1] + char
            elif char == '.':
                self.formula += char
            else:
                return
            self.update_display(self.formula)

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
            if self.consecutive_digits >= 6 and char == '.':
                return
            if char == '.' and '.' in self.formula:
                return
            if self.formula and self.formula[-1] in ['+', '-', '*', '/', '**2', '√x']:
                return
                #self.formula = self.formula[:-1] + char
            if self.formula and self.formula[-1] == '(':
                return
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
        else:
            self.update_display("Error 105")
        if char.isdigit() or char == '.':
            self.last_input_type = "digit"
        elif char in ['+', '-', '*', '/', '()', '**2', '√x']:
            self.last_input_type = "operator"
        else:
            self.last_input_type = ""
        if len(self.formula) > 18:
            self.update_display("Expression too long")
            return
        self.update_display()
        self.update_display(text=self.formula)

    def clear(self):
        self.formula = "0"
        self.update_display()
        self.locked = False
        self.paren_count = 0
        self.consecutive_digits = 0

    def change_sign(self):
        if self.formula == '0':
            return
        try:
            if self.formula:
                match = re.search(r"([+*/-])?(\()?(-?\d+(\.\d+)?)\)?$", self.formula)
                if match:
                    prefix = match.group(1)
                    in_paren = bool(match.group(2))
                    num_str = match.group(3)

                    prefix_index = self.formula.rfind(prefix) if prefix else -1
                    pre_char = self.formula[prefix_index - 1] if prefix_index > 0 else ''

                    if prefix and prefix == '*':
                        new_num_str = '-' + num_str if not num_str.startswith('-') else num_str[1:]
                        replacement = f"*({new_num_str})"
                    elif prefix and prefix == '/':
                        new_num_str = '-' + num_str if not num_str.startswith('-') else num_str[1:]
                        replacement = f"/({new_num_str})"
                    elif prefix and prefix in ('+', '-'):
                        new_prefix = '-' if prefix == '+' else '+'
                        replacement = new_prefix + num_str
                    elif in_paren:
                        if num_str.startswith('-'):
                            replacement = num_str[1:]
                        else:
                            replacement = '-' + num_str

                    elif not prefix or pre_char == '':
                        if num_str.startswith('-'):
                            replacement = num_str[1:]
                        else:
                            replacement = '-' + num_str

                    else:
                        replacement = num_str

                    old_len = len(num_str) + (2 * in_paren) + (len(prefix) if prefix else 0)
                    new_len = len(replacement)
                    start_index = len(self.formula) - old_len
                    self.formula = self.formula[:start_index] + replacement + self.formula[start_index + old_len:]
                    self.update_display(self.formula)

        except (ValueError, TypeError, IndexError):
            self.update_display(f"Error 107")

    def count_digits_before_operator(self, formula):
        count = 0
        i = len(formula) - 1
        while i >= 0 and formula[i] not in ['+', '-', '*', '/', '(', ')', '**2', '.', '√x']:
            if formula[i].isdigit():
                count += 1
            i -= 1
        return count

    def factorial(self):
        try:
            if self.formula:
                match = re.search(r"([+\-*/])?(\d+(\.\d+)?)(?=[^\d\.\-*$]|$)", self.formula)

                if match:
                    sign = match.group(1)
                    num_str = match.group(2)
                    num = float(num_str)
                    sign_index = self.formula.rfind(sign) if sign else -1
                    pre_char = self.formula[sign_index - 1] if sign_index > 0 else ''

                    if num == int(num) and num >= 0:
                        factorial_result = math.factorial(int(num))
                        replacement = str(factorial_result)

                        if sign == '-' and pre_char == '':
                            self.update_display("Error 108")
                            return
                        elif sign and pre_char in ["1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                            replacement = sign + replacement

                        self.formula = self.formula.replace(match.group(0), replacement, 1)
                        if len(self.formula) > 18:
                            self.update_display("Result too long")
                            return
                        else:
                            self.update_display(self.formula)
                    else:
                        self.update_display("Error 108")
                        return
                else:
                    return
            else:
                return
        except (ValueError, OverflowError):
            self.update_display("Error 108")

    def modul(self):
        try:
            match = re.search(r"([+\-*/])?(\d+(\.\d+)?)(?=[^\d\.\-*$]|$)", self.formula)
            if match:
                minus = match.group(1)
                num = match.group(2)
                nums = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
                if self.formula and not self.formula[-1] in ")":
                    if self.formula[-1] in nums and self.formula[-2] in '-':
                        self.formula = self.formula[:-1] and self.formula[:-2]
                    elif self.formula[-2] in nums and self.formula[-3] in '-':
                        self.formula = self.formula[:-1] and self.formula[:-2] and self.formula[:-3]
                    elif self.formula[-3] in nums and self.formula[-4] in '-':
                        self.formula = self.formula[:-1] and self.formula[:-2] and self.formula[:-3] and self.formula[:-4]
                    elif self.formula[-4] in nums and self.formula[-5] in '-':
                        self.formula = self.formula[:-1] and self.formula[:-2] and self.formula[:-3] and self.formula[:-4] and self.formula[:-5]
                    elif self.formula[-5] in nums and self.formula[-6] in '-':
                        self.formula = self.formula[:-1] and self.formula[:-2] and self.formula[:-3] and self.formula[:-4] and self.formula[:-5] and self.formula[:-6]
                    elif self.formula[-6] in nums and self.formula[-7] in '-':
                        self.formula = self.formula[:-1] and self.formula[:-2] and self.formula[:-3] and self.formula[:-4] and self.formula[:-5] and self.formula[:-6] and self.formula[:-7]
                    self.formula = self.formula + "+" + num
                elif self.formula[-1] in ")" and self.formula[-2] in num and self.formula[-3] in "-" and not self.formula[-4] in nums:
                    print("2")
                    if self.formula[-2] in num and self.formula[-3] in '-':
                        self.formula = self.formula[:-1] and self.formula[:-2] and self.formula[:-3]
                    self.formula = self.formula + num + ")"
                elif self.formula[-1] in ")" and self.formula[-2] in nums and self.formula[-3] in "-" and self.formula[-4] in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                    print("3")
                    if self.formula[-2] in nums and self.formula[-3] in '-':
                        self.formula = self.formula[:-1] and self.formula[:-2] and self.formula[:-3]
                    self.formula = self.formula + "+" + num + ")"
                self.consecutive_digits = self.count_digits_before_operator(self.formula)
                self.update_display(self.formula)
        except:
            self.update_display("Error 110")

    def percent(self):
        try:
            if self.formula:
                match = re.findall(r"([+\-*/])?(\d+(\.\d+)?)(?=[^\d\.\-*$]|$)", self.formula)
                if match:
                    last_match = match[-1]
                    sign = last_match[0]
                    num_str = last_match[1]
                    num = float(num_str)
                    percentage = num / 100
                    replacement = str(percentage)
                    if sign:
                        replacement = sign + replacement
                    full_match_str = sign + num_str if sign else num_str
                    index = self.formula.rfind(full_match_str)

                    self.formula = self.formula[:index] + replacement + self.formula[index + len(full_match_str):]
                    if len(self.formula) > 18:
                        self.update_display("Result too long")
                        return
                    else:
                        self.update_display(self.formula)
                else:
                    return
            else:
                return
        except (ValueError, Exception):
            self.update_display("Error 109")
            return

    def sqrt(self):
        if not self.formula:
            return
        if self.formula == "0":
            return
        elif not self.formula or not self.formula.strip():
            self.update_display("Error 106")
            return
        try:
            result = math.sqrt(float(self.formula))
            result_str = str(result)
            if len(result_str) > 18:
                self.update_display("Result too long")
                return
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
        if self.formula and self.formula[-1] in ['+', '-', '*', '/', '**2', '√x']:
            self.formula = self.formula[:-1]
            self.consecutive_digits = self.count_digits_before_operator(self.formula)
        elif self.formula and self.formula[-1] == '(':
            self.formula = self.formula[:-1]
            self.consecutive_digits = self.count_digits_before_operator(self.formula)
            self.paren_count = 0
        elif self.formula and self.formula[-1] == ')':
            self.formula = self.formula[:-1]
            self.consecutive_digits = self.count_digits_before_operator(self.formula)
            self.paren_count = 1
        else:
            match = re.search(r"([+*/-])?(\()?(-?\d+(\.\d+)?)\)?$", self.formula)
            prefix = match.group(1)
            prefix_index = self.formula.rfind(prefix) if prefix else -1
            pre_char = self.formula[prefix_index - 1] if prefix_index > 0 else ''
            if pre_char == '':
                self.formula = "0"
                self.update_display()
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
            result_str = str(result)
            if len(result_str) > 18:
                self.update_display("Result too long")
                return
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
            result_str = str(result)
            if len(result_str) > 18:
                self.update_display("Result too long")
                return
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