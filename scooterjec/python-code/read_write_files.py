from pathlib import Path

path = Path('example.txt')

# Path.open(Path('example.txt'),"r")

with Path.open('example.txt',"r") as file:
    contents = file.read()
    print(contents)
    
with Path.open("example2.txt","w") as f:
    contents = f.write("This is all new text!!")
    print(contents)