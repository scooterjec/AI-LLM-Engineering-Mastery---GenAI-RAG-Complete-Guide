
import pathlib


try:
    print(5/1)
except ZeroDivisionError as e:
    print(f"Error occured: {e}")
else:
    print("All is well here")
finally:
    # clean up resources
    print("I always execute")
    
    
from pathlib import Path

path = Path("example.txt_")
try:
    contents = path.read_text()
    print(contents)
except FileNotFoundError as e:
    print(f"FnF: {e}")
    
names=["A","B","C"]
try:
    print(names[5])
except IndexError as e:
    print(f"Error: {e}")
    
class MyCustomError(Exception):
    pass
    
class ValueTooSmallError(MyCustomError):
    pass

class ValueTooLargeError(MyCustomError):
    pass
    
def check_value(number):
    if number < 5:
        raise ValueTooSmallError(f"The value is too small: {number}")
    elif number > 15:
        raise ValueTooLargeError(f"The value is too large: {number}")
    else:
        print(f"Right value: {number}")
        
try:
    user_input = int(input("Enter a number: "))
    check_value(user_input)
except ValueTooSmallError as e:
    print(e)
except ValueTooLargeError as e:
    print(e)
    