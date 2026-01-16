# Tuples are immutable
names = ('Juan','Pedro')
print(names)

for name in names:
    print(name)

# Esto falla: 'tuple' object does not support item assignment
names[0] = "Pepe"
