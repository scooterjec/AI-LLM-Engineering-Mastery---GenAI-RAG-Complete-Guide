import json
from pathlib import Path

# person_Data= {
#     "name":"JEC",
#     "age":30,
#     "city":"NY",
#     "hasPets":False,
#     "titles":["Title 1", "Title 2"]
# }

names = ["James","Ruth","Mary"]
names_json = json.dumps(names)

print(names)
print(names_json)

with Path("names.json").open("w") as f:
    contents = json.dumps(names)
    f.write(contents)
    
with Path("names.json").open("r") as f:
    contents = json.load(f)
    print(contents)
    
def save_to_json(data, filename="countries.json"):
    """ Save the list od countries to a JSON file """
    with Path(filename).open("w") as f:
        json.dump(data, f)
        
def read_from_json(filename="countries.json"):
    with Path(filename).open('r') as f:
        return json.load(f)
        
def main():
    countries=[]
    print ("Enter country names. q to quit: ")
    while True:
        country = input("Country: ")
        if country.lower() == 'q':
            break
        countries.append(country)
        save_to_json(countries)
        saved_countries = read_from_json()
        print(f"Countries added: {saved_countries}")
        
if __name__ == "__main__":
    main()
            