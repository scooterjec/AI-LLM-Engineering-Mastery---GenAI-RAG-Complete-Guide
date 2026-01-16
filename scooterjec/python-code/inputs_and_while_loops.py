name = input("Enter your name: ")
age = int(input("How old are you?: "))
print(f"Your name is {name} and you are {age}!")
print(type(age))
mult=age*5
print(mult)

n = input("Enter a number: ")
n = int(n)

if n%2 == 0:
    print(f"{n} is even")
else:
    print(f"{n} is odd")

counter = 0
while counter < 5:
    print(f"Counter is {counter}")
    counter += 1
    
prompt = "\nEnter 'quit' to end the program"
prompt +="\nEnter your command:"
while True:
    command = input(prompt)
    if command == 'quit':
        break
    else:
        print(f"You entered {command}")


# remove all instance of specific value in a list
ingredients = ["avocado", "tomato", "avocado", "avocado", 'lettuce', "avocado", "apple"]
print(ingredients)
while "avocado" in ingredients:
    ingredients.remove("avocado")
print(ingredients)