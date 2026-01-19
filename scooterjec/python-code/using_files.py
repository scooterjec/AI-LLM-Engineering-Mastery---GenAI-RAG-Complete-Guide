from pathlib import Path

p = Path(".")
print(p.cwd())
print(p.absolute())

path = Path('example.txt')
contents=path.read_text()
print(contents.lower())

path = Path('./subpath/another_example.txt')
contents=path.read_text()
print(contents.upper())

# path = Path('./subpath/')
# st = path.stem()
# print(st)

path = Path('./subpath/another_example.bad')
if path.exists():
    contents=path.read_text()
    print(contents.upper())
else:
    print("path doesn't exist")
    
content = "Writing code!"
path = Path("test.txt")
path.write_text(content)

content += "Are u writing code or sth else?\n"
content += "Another line"
path = Path("test.txt")
path.write_text(content)
