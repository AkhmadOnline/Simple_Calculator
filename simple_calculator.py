import re
from tkinter import *

calculation = ''
last_result = None
WIDTH = 65
HEIGHT = 65
INDENT = 4
BG_COLOR = "black"

root = Tk()
root.title("Калькулятор")
root.geometry("280x455")
root.config(bg=BG_COLOR)
root.resizable(width=False, height=False)

#Окно для ввода и вывода
entry = Entry(root, font=("Arial", 24), state="readonly", justify=RIGHT)
entry.place(x=0+INDENT, y=0+INDENT, width=271, height=100)

def parse_expression(expression):
    """
    Парсит математическое выражение и возвращает список токенов.
    """
    tokens = []
    current_number = ""
    for i, char in enumerate(expression):
        if char.isdigit() or char == ".":
            current_number += char
        elif char in ('x', '/', '+', '-', '%'):
            if current_number:
                tokens.append(float(current_number))
                current_number = ""
            if char == '-' and (i == 0 or expression[i-1] in ('x', '/', '+', '-', '(')):
                current_number = '-'
            else:
                tokens.append(char)
    if current_number:
        tokens.append(float(current_number))
    return tokens


def calculate(expression):
    """
    Вычисляет значение математического выражения.
    """
    tokens = parse_expression(expression)

    # Обработка процентов
    i = 0
    while i < len(tokens):
        if tokens[i] == '%':
            if i > 0 and isinstance(tokens[i - 1], float):
                tokens[i - 1] *= 0.01
                tokens.pop(i)
            else:
                raise ValueError("Некорректное использование процента")
        else:
            i += 1

    # Умножение и деление
    i = 0
    while i < len(tokens):
        if tokens[i] == 'x':
            tokens[i - 1] = tokens[i - 1] * tokens[i + 1]
            tokens.pop(i)
            tokens.pop(i)
            i -= 1
        elif tokens[i] == '/':
            tokens[i - 1] = tokens[i - 1] / tokens[i + 1]
            tokens.pop(i)
            tokens.pop(i)
            i -= 1
        else:
            i += 1

    # Сложение и вычитание
    i = 0
    while i < len(tokens):
        if tokens[i] == '+':
            tokens[i - 1] = tokens[i - 1] + tokens[i + 1]
            tokens.pop(i)
            tokens.pop(i)
            i -= 1
        elif tokens[i] == '-':
            tokens[i - 1] = tokens[i - 1] - tokens[i + 1]
            tokens.pop(i)
            tokens.pop(i)
            i -= 1
        else:
            i += 1

    return tokens[0]

#Округляем результат
def format_result(value):
    if isinstance(value, float):
        if value == 0:
            return "0"  # Всегда возвращаем "0" вместо "-0"
        rounded = round(value, 9)
        str_value = f"{rounded:.9f}"
        str_value = str_value.rstrip('0')
        if str_value.endswith('.'):
            str_value = str_value[:-1]
        return str_value
    return str(value)

# Вычисление значения
def calculate_result():
    global calculation, last_result
    try:
        result = calculate(calculation)
        formatted_result = format_result(result)
        entry.config(state="normal")
        entry.delete(0, END)
        entry.insert(0, formatted_result)
        entry.config(state="readonly")
        calculation = formatted_result
        last_result = result  # Сохраняем неокругленный результат для дальнейших вычислений
    except:
        entry.config(state="normal")
        entry.delete(0, END)
        entry.insert(0, "Ошибка")
        entry.config(state="readonly")
        calculation = ""
        last_result = None


# Функции для обработки событий
def handle_digit_button(digit):
    global calculation
    entry.config(state="normal")
    current = entry.get()
    if current == "0" or current == "Ошибка":
        entry.delete(0, END)
        calculation = ""
    elif current == "-0":
        entry.delete(0, END)
        entry.insert(END, "-")
        calculation = "-"
    entry.insert(END, str(digit))
    calculation += str(digit)
    entry.config(state="readonly")

def handle_operation_button(operation):
    global calculation
    entry.config(state="normal")
    current = entry.get()
    if current and current != "Ошибка":
        if current[-1] in ('x', '/', '+', '-', '%'):
            calculation = calculation[:-1] + operation
            entry.delete(0, END)
            entry.insert(END, calculation)
        else:
            calculation += operation
            entry.insert(END, operation)
    entry.config(state="readonly")

def handle_equals_button():
    global calculation
    current = entry.get()
    if current and current != "Ошибка":
        calculation = current
        calculate_result()

def handle_reset_button():
    global calculation
    entry.config(state="normal")
    calculation = ''
    entry.delete(0, END)
    entry.insert(0, "0")
    entry.config(state="readonly")

def handle_negative_button():
    global calculation
    entry.config(state="normal")
    current = entry.get()
    if current and current != "Ошибка":
        parts = re.split(r'([x/+\-])', current)
        last_part = parts[-1]
        
        if last_part:
            if last_part[0] == '-':
                parts[-1] = last_part[1:]
            else:
                parts[-1] = '-' + last_part
        else:
            parts.append('-0')
        
        new_expression = ''.join(parts)
        entry.delete(0, END)
        entry.insert(0, new_expression)
        calculation = new_expression
    entry.config(state="readonly")

def handle_percent_button():
    global calculation
    entry.config(state="normal")
    current = entry.get()
    if current and current != "Ошибка":
        entry.insert(END, "%")
        calculation += "%"
    entry.config(state="readonly")

def handle_point_button():
    global calculation
    entry.config(state="normal")
    current = entry.get()
    if current and current != "Ошибка":
        # Разделим текущее выражение на числа и операторы
        parts = re.split(r'([x/+\-])', current)
        last_part = parts[-1]
        
        # Проверяем, есть ли уже точка в последнем числе
        if '.' not in last_part:
            if last_part == '' or not last_part[-1].isdigit():
                entry.insert(END, "0.")
                calculation += "0."
            else:
                entry.insert(END, ".")
                calculation += "."
    entry.config(state="readonly")

#Кнопка умножение
multiplication_button = Button(root, text="x", command=lambda: handle_operation_button("x"))
multiplication_button.place(x=215-INDENT, y=195-INDENT*4, width=WIDTH, height=HEIGHT)

#Кнопка деление
division_button = Button(root, text="/", command=lambda: handle_operation_button("/"))
division_button.place(x=215-INDENT, y=130-INDENT*5, width=WIDTH, height=HEIGHT)

#Кнопка плюс
plus_button = Button(root, text="+", command=lambda: handle_operation_button("+"))
plus_button.place(x=215-INDENT, y=325-INDENT*2, width=WIDTH, height=HEIGHT)

#Кнопка минус
minus_button = Button(root, text="-", command=lambda: handle_operation_button("-"))
minus_button.place(x=215-INDENT, y=260-INDENT*3, width=WIDTH, height=HEIGHT)

#Кнопка Равно
equals_button = Button(root, text="=", command=handle_equals_button)
equals_button.place(x=215-INDENT, y=390-INDENT, width=WIDTH, height=HEIGHT)

#Кнопка точки
point_button = Button(root, text=".", command=handle_point_button)
point_button.place(x=150-INDENT*2, y=390-INDENT, width=WIDTH, height=HEIGHT)

#Кнопка ноль
zero_button = Button(root, text="0", command=lambda: handle_digit_button(0))
zero_button.place(x=0+INDENT, y=390-INDENT, width=135, height=HEIGHT)

#Кнопка один
one_button = Button(root, text="1", command=lambda: handle_digit_button(1))
one_button.place(x=0+INDENT, y=325-INDENT*2, width=WIDTH, height=HEIGHT)

#Кнопка два
two_button = Button(root, text="2", command=lambda: handle_digit_button(2))
two_button.place(x=65+INDENT*2, y=325-INDENT*2, width=WIDTH, height=HEIGHT)

#Кнопка три
three_button = Button(root, text="3", command=lambda: handle_digit_button(3))
three_button.place(x=150-INDENT*2, y=325-INDENT*2, width=WIDTH, height=HEIGHT)

#Кнопка четыре
four_button = Button(root, text="4", command=lambda: handle_digit_button(4))
four_button.place(x=0+INDENT, y=260-INDENT*3, width=WIDTH, height=HEIGHT)

#Кнопка пять
five_button = Button(root, text="5", command=lambda: handle_digit_button(5))
five_button.place(x=65+INDENT*2, y=260-INDENT*3, width=WIDTH, height=HEIGHT)

#Кнопка шесть
six_button = Button(root, text="6", command=lambda: handle_digit_button(6))
six_button.place(x=150-INDENT*2, y=260-INDENT*3, width=WIDTH, height=HEIGHT)

#Кнопка семь
seven_button = Button(root, text="7", command=lambda: handle_digit_button(7))
seven_button.place(x=0+INDENT, y=195-INDENT*4, width=WIDTH, height=HEIGHT)

#Кнопка восемь
eight_button = Button(root, text="8", command=lambda: handle_digit_button(8))
eight_button.place(x=65+INDENT*2, y=195-INDENT*4, width=WIDTH, height=HEIGHT)

#Кнопка девять
nine_button = Button(root, text="9", command=lambda: handle_digit_button(9))
nine_button.place(x=150-INDENT*2, y=195-INDENT*4, width=WIDTH, height=HEIGHT)

#Кнопка сброса
reset_button = Button(root, text="C", command=handle_reset_button)
reset_button.place(x=0+INDENT, y=130-INDENT*5, width=WIDTH, height=HEIGHT)

#Кнопка отрицательного числа
negative_button = Button(root, text="+/-", command=handle_negative_button)
negative_button.place(x=65+INDENT*2, y=130-INDENT*5, width=WIDTH, height=HEIGHT)

#Кнопка процента
percent_button = Button(root, text="%", command=handle_percent_button)
percent_button.place(x=150-INDENT*2, y=130-INDENT*5, width=WIDTH, height=HEIGHT)

root.mainloop()