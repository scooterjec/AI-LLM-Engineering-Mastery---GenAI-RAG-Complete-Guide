## This is a sample Python application

print("Hello there! This is a sample Python application.")
print(3*5)

## Vars and Data Types

name = "juan"
message = "hello there, this is good"
print(f"{message.title()}, {name.title()}!")

upper_case = message.upper()
print(upper_case)

## f-strings
nombre="juan"
mensaje="  hello   there,   this   is    good   "
print(f"{mensaje.strip()}, {nombre.title()}!")

## Numbers

age = 51
suma = age + 5
print(f"In five years, you will be {suma} years old.")

division = suma / 13
print(f"Dividing your age in five years by 13 gives: {division}")

# Lists
fruits = ["apple", "banana", "cherry"]
print(f"Fruits available: {fruits}")
print(f"First fruit: {fruits[0].title()}")

fruits.append("orange")
print(f"Fruits after adding orange: {fruits}")

fruits.remove("banana")
print(f"Fruits after removing banana: {fruits}")

fruits.pop()
print(f"Fruits after popping the last item: {fruits}")

fruits.pop(0)
print(f"Fruits after popping the first item: {fruits}")

# f-strings and individual values from lists

fruits = ["apple", "banana", "cherry"]
message = f"My favorite fruit is {fruits[1].title()}."
print(message)

# Sorting Lists and legth
ages = [25, 30, 22, 35, 28]
print(f"Original ages: {ages}")
ages.sort()
print(f"Sorted ages: {ages}")
ages.reverse()
print(f"Sorted ages in descending order: {ages}")

list_length = len(ages)
print(f"Number of ages in the list: {list_length}")

# Lists and loops
colors = ["red", "blue", "green"]
for color in colors:
    print(f"I like the color {color.title()}.")