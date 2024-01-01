class ValidationError(BaseException):
    def __init__(self, *message):
        super().__init__("Unspecified ValidationError" if message is None else message)
        raise (self)


class Validate:
    def __new__(cls, *args, **kwargs):
        invalid_keys = ", ".join(
            [
                key
                for key in filter(
                    lambda key: key not in cls.__annotations__.keys(), kwargs.keys()
                )
            ]
        )
        if invalid_keys != "":
            raise (KeyError(invalid_keys))

        if len(args) > len(cls.__annotations__):
            raise (
                TypeError(
                    f"{cls} is annotated with {len(cls.__annotations__)} attributes but it was initialized with {len(args)}"
                )
            )

        suber = super().__new__(cls)

        for kw in kwargs.keys():
            if type(kwargs[kw]) != cls.__annotations__[kw]:
                ValidationError(f"{kw} is not a valid {type(kwargs[kw])}")
            setattr(suber, kw, kwargs[kw])

        for pair in map(lambda a, b: (type(a), b, a), args, cls.__annotations__):
            if pair[0] != cls.__annotations__[pair[1]]:
                ValidationError(
                    f"{pair[1]} is not a valid {cls.__annotations__[pair[1]]}"
                )
            setattr(suber, pair[1], pair[2])

        def wrapper(method):
            def valiation(*args, **kwargs):
                prev = [
                    suber.__getattribute__(attr)
                    for attr in suber.__dir__()
                    if not callable(suber.__getattribute__(attr))
                    and type(suber.__getattribute__(attr)) is dict
                ][-1].copy()
                call = method(*args, **kwargs)
                post = [
                    suber.__getattribute__(attr)
                    for attr in suber.__dir__()
                    if not callable(suber.__getattribute__(attr))
                    and type(suber.__getattribute__(attr)) is dict
                ][-1]
                for name in post.keys():
                    if name in prev.keys() and type(post[name]) != type(prev[name]):
                        raise (
                            ValidationError(
                                f"{method.__name__}: {name} was change to {type(post[name])} but it must be {type(prev[name])}"
                            )
                        )
                return call

            return valiation

        [
            setattr(
                suber,
                suber.__getattribute__(method).__name__,
                wrapper(suber.__getattribute__(method)),
            )
            for method in suber.__dir__().copy()
            if callable(suber.__getattribute__(method))
            and suber.__getattribute__(method).__name__
            not in [
                "__class__",
                "__getattribute__",
                "__dir__",
            ]  # __getattribute__ and __dir__ are to avoid recursion,
        ]  # there may be a way to work around

        return suber


def validate(cls):
    def inner(*args, **kwargs):
        new_class = type(f"{cls.__name__}", (Validate, cls), {})
        setattr(new_class, "__annotations__", cls.__annotations__)
        setattr(new_class, "__init__", cls.__init__)
        return new_class(*args, **kwargs)

    return inner
