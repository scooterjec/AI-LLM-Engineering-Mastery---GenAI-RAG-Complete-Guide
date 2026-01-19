def greetings():
    print("Hello J!!!")

for i in range(0,10):
    greetings()

def greet(name, age=5):
    print(f"Hello there, {name}! you're {age}")
    
greet("pepe")

for i in range(0,10):
    greet(age=i+3, name='JEC')
    
def car_detail(car_type='truck', car_name='bmw'):
    print(f"I have a {car_type} named {car_name}")
car_detail()

def format_name(first_name, last_name):
    full_name = f"{first_name} {last_name}"
    return full_name.title()
    
formatted_name = format_name(first_name='james', last_name="bond")
print(f"{formatted_name}")

def multiply(a,b):
    """
    Takes 2 numbers and multiplies them
    """
    return a*b
res = multiply(5,6)
print(res)

def build_profile(first, last):
    """Build dictionary"""
    user = {"first":first, "last":last}
    return user
    
user = build_profile("Juan", "Espino")
print(user)

plants=["lemon-tree","mango-tree", "apple-tree"]
def water_plants(plants):
    for plant in  plants:
        action = f"Watering the {plant}."
        print(action)
    
water_plants(plants)

# Arbitrary number of args

def sumar(*args):
    return sum(args)
    
print(f"La suma es: {sumar(2,5,1,7,3)}")

def build_profile_2(first, last, **user_info):
    user_info["first_name"] = first
    user_info["last_name"] = last
    return user_info


user = build_profile_2("Juan", "Espino", city="NY", age=25)
print(user)

