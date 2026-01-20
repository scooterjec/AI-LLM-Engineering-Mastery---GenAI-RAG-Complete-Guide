from pathlib import Path

path = Path('example.txt')

# Path.open(Path('example.txt'),"r")

with Path('example.txt').open("r") as file:
    contents = file.read()
    print(contents)
    
with Path('example2.txt').open("w") as f:
    contents = f.write("This is all new text!!")
    print(contents)