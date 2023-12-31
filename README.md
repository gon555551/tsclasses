# Class Attribute Type Validation

Includes the `Validate` superclass and the `ValidationError` exception.

Inheriting from `Validate` will result in instantiation type-checking based on annotations, as well as in-method attribute static-typing by raising `ValidationError`.

## Example
```python
from tsclasses import Validate


class Example(Validate):
    number: int
    
    def __init__(self, *args, **kwargs):
        self.string = "five"
    
    def valid_method(self):
        self.number = 5
        
    def invalid_method(self):
        self.string = 5
```
