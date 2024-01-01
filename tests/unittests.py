from src.tsclasses import *


# Without annotations or methods
class Validated(Validate):
    pass


Validated()

try:
    Validated(5)
    Validated(number="five")
except TypeError or KeyError:
    print("Successfully blocks instatiation with non-annotated attributes")
    pass


# With annotations, without methods
class Validated(Validate):
    number: int


Validated()
Validated(5)
Validated(number=5)

try:
    Validated("five")
    Validated(number="five")
except ValidationError:
    print("Successfully blocks instatiation with incorrect types")
    pass


# With annotations and methods
class Validated(Validate):
    number: int

    def __init__(self, *args, **kwargs):
        self.string = "five"

    def valid_method(self):
        self.number = 5

    def invalid_method(self):
        self.string = 5


Validated().valid_method()
Validated(5).valid_method()
Validated(number=5).valid_method()

try:
    Validated(5).invalid_method()
except ValidationError:
    print("Successfully blocks methods that change the type of an attribute")
    pass


# With the class decorator
@validate
class Validated:
    number: int

    def __init__(self, *args, **kwargs):
        self.string = "five"

    def valid_method(self):
        self.number = 5

    def invalid_method(self):
        self.string = 5


Validated().valid_method()
Validated(5).valid_method()
Validated(number=5).valid_method()

try:
    Validated(5).invalid_method()
except ValidationError:
    print("Successfully blocks methods that change the type of an attribute")
    pass
