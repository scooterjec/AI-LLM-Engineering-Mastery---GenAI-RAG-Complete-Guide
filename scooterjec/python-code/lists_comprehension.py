# List comprehension

list_sqrs = []
for value in range(0,10):
    list_sqrs.append(value*2)

print(list_sqrs)

ls_sqrs = [value * 2 for value in range(0,10) ]
print(ls_sqrs)