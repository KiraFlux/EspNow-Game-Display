from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Vector2D[T]:
    """Ход игрока"""

    x: T
    y: T

    def toTuple(self) -> tuple[T, T]:
        """Преобразовать в кортеж"""
        return self.x, self.y

    def __add__(self, other: Vector2D[T]):
        return Vector2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Vector2D[T]):
        return Vector2D(self.x - other.x, self.y - other.y)

    def __mul__(self, other: T):
        return Vector2D(self.x * other, self.y * other)

    def __truediv__(self, other: T):
        return Vector2D(self.x / other, self.y / other)


@dataclass(frozen=True)
class Vector3D[T]:
    """Ход игрока"""

    x: T
    y: T
    z: T

    def __add__(self, other: Vector3D[T]):
        return Vector3D(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: Vector3D[T]):
        return Vector3D(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other: T):
        return Vector3D(self.x * other, self.y * other, self.z * other)

    def __truediv__(self, other: T):
        return Vector3D(self.x / other, self.y / other, self.z / other)
