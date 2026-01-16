activities = ["hiking", "swimming", "museum", "picnic"]
group_interest=["art","history", "swimming"]

if "museum" in activities and ("art" in group_interest or "history" in group_interest):
    print("We should visit a museum!")
elif "swimming" in activities and "swimming" in group_interest:
    print("Go to the pool!")
else:
    print("Let's plan a picnic!")
    
age = 22
topping=["olives", "tomatoes"]

if topping[0] != "mangoes":
    print("No mangoes for toppings!")
if 'mangoes' not in topping:    
    print("No mangoes for toppings!")

if age != 23:
    print("Not 23")
