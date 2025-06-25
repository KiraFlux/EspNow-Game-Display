from dataclasses import dataclass


@dataclass
class Instruction:
    """Исполняемая инструкция"""

    index: bytes
    """Префиксный индекс"""
    name: str
    """Наименование для отладки"""
