full_name = {'Juan':'Espino', 'Guille':'Moreno'}
print(full_name)

person={"name":"Alex", "age": 34, "city":"NY"}
print(person)

print(person["name"])
# return Error
# print(person["nam"])
print(person.get("age"))
#return None pero no hay Error
print(person.get("ag"))

person["email"]="pp@pp.com"
person["is_employed"]=True
person["age"] = 40
# Remove a K-V
person.pop("city")
print(person)

#Delete an item from memory at all
del person["is_employed"]
print(person)

#Delete the dict
#person.clear()
#print(person)

# Iterate through keys
for key in person:
    print(key)

# Iterate through values
for value in person.values():
    print(value)

for k,v in person.items():
    print(f"{k} -> {v}")
    
#Nested dicts
family = {
    "mom": {"name":"Gina","age":40},
    "dad": {"name":"Papa","age":45}
}

print(family)

for name, info in family.items():
    print(name, info)
    
for name, info in family.items():
    print(f"\n Parent Type: {name}")
    parent_name = f"Name: {info["name"]}"
    parent_age = f"Name: {info["age"]}"
    print(f"{parent_name}")
    print(f"{parent_age}")

# Dicts with List inside
speakers = {
    "Alice": ["Book 1","Book 2","Book 3"],
    "Bob": ["Book A","Book B","Book C"],
    "Carol": ["Pencil 1","Pencil 2","Pencil 3"]
}
for name, topics in speakers.items():
    print(f"\n{name} will show :")
    for topic in topics:
        print(f"-{topic}")