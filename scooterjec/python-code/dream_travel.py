dream_dest = {}
print("Enter travel itinerary")
print ("Enter 'done' when you're finished")

while True:
    country = input("Country to visit?")
    if country.lower() == 'done':
        break
    
    note = input(f"What to see in {country}? (Press enter to skip)")
    
    #Add country and optional note to dict
    dream_dest[country] = note if note else "N/A"
    
print("\nYour dream travel itinerary:")
for country, note in dream_dest.items():
    print(f"-{country} - {note}")
    
print("Done!!!")
