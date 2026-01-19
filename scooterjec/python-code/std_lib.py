from random import randint, choice

# print(randint(a=2,b=9))

def rand_fruit(fruits):
    rand = randint(0, len(fruits)-1)
    # print(rand)
    rand_fruit=fruits[rand]
    return rand_fruit

def choice_fruit(fruits):
    if not fruits:
        return "The fruit list is empty"
    return choice(fruits)

items=["apple","banana","mango"]

# print(f"Rand Fruit: {rand_fruit(items)}")
# print(f"Choice Fruit: {choice_fruit(items)}")


from datetime import datetime, timedelta

now = datetime.now()
print(f"Current date and time: {now}")

future_date = now + timedelta(days=10)
print(f"Future date and time: {future_date}")

formatted_date = now.strftime("%d/%m/%Y")
print(formatted_date)