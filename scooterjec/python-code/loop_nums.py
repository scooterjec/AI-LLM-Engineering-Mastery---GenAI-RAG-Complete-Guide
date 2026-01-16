# list of numbers and range function

list_nums=[]
for value in range(1,10):
    value = value*2
    list_nums.append(value)
    print(f"Number: {value} ")

print(f"List of numbers: {list_nums}")

list_nums=[]
for value in range(1,10):
    list_nums.append(value)

#max
max_num = max(list_nums)
print(f"list_nums: {list_nums}")
print(f"Max: {max_num}")

# min
min_num = min(list_nums)
print(f"Min: {min_num}")

# sum
sum_nums = sum(list_nums)
print(f"Sum: {sum_nums}")

# Range function options
evens = list(range(0,100, 2))
print(f"Even numbers: {evens}")