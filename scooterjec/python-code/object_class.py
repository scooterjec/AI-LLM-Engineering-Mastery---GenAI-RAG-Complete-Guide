class Vehicle:
    def __init__(self, name, year) -> None:
        self.name=name
        self.year=year
        
    def __str__(self) -> str:
        return f"{self.year} -> {self.name}"
        
class Car(Vehicle):
    def __init__(self, name, year, mileage) -> None:
        super().__init__(name, year)
        self.mileage=mileage
        
    def __str__(self) -> str:
        return f"{super().__str__()} with {self.mileage} miles"
        
print(issubclass(Vehicle, object))
print(issubclass(Vehicle, Car))
print(issubclass(Car, object))
print(Vehicle.__bases__)
print(Car.__bases__)
