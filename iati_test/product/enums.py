from enum import Enum


class SizeType(Enum):
    MAN = "man"
    WOMAN = "woman"
    UNISEX = "unisex"

    @classmethod
    def choices(cls):
        return [(choice.value, choice.name) for choice in cls]
