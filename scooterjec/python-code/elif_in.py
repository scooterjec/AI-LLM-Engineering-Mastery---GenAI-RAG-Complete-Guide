temperature = 65
if temperature < 45:
    print("Wear a jacket")
elif temperature < 60:
    print("A t-shirt is right")
else:
    print("It's warm, stay cool")


participants=["Bob", "Jerry", "John"]
if "Bob" in participants:
    print("Bob is in")
else:
    print("Bob not registered")
    
day = 'Saturday'
fridge_contents=['eggs','bacon']

if day == 'Saturday':
    if 'eggs' and 'bacon' in fridge_contents:
        print("Time for a hearty breakfast!")
    else:
        print("Maybe cereals today!")
else:
    print("Quick breakfast!!")