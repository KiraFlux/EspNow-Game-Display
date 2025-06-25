from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from typing import Callable

from rs.exceptions import Panic
from rs.option import Option
from rs.option import none
from rs.option import some


@dataclass(frozen=True, kw_only=True)
class Result[T, E]:
    """
    Тип-обертка для представления результата операции, который может быть
    успешным (содержит значение типа T) или ошибочным (содержит ошибку типа E).

    Вдохновлен аналогичным типом из Rust и Haskell Either, предоставляет безопасный
    способ обработки операций, которые могут завершиться с ошибкой.
    """

    _is_ok: bool
    _value: T | E

    def is_ok(self) -> bool:
        """Проверить, содержит ли результат успешное значение"""
        return self._is_ok

    def is_err(self) -> bool:
        """Проверить, содержит ли результат ошибку"""
        return not self._is_ok

    def ok(self) -> Option[T]:
        """Преобразовать в Option[T], где Some содержит успешное значение"""
        return some(self._value) if self.is_ok() else none()

    def err(self) -> Option[E]:
        """Преобразовать в Option[E], где Some содержит ошибку"""

        return some(self._value) if self.is_err() else none()

    def map[U](self, f: Callable[[T], U]) -> Result[U, E]:
        """
        Применить функцию к успешному значению, оставив ошибку без изменений

        Args:
            f: Функция для преобразования успешного значения

        Returns:
            Новый Result с преобразованным значением или исходной ошибкой
        """

        return ok(f(self._value)) if self.is_ok() else err(self._value)

    def map_err[F](self, f: Callable[[E], F]) -> Result[T, F]:
        """
        Применить функцию к ошибке, оставив успешное значение без изменений

        Args:
            f: Функция для преобразования ошибки

        Returns:
            Новый Result с преобразованной ошибкой или исходным значением
        """

        return err(f(self._value)) if self.is_err() else ok(self._value)

    def and_then[U](self, f: Callable[[T], Result[U, E]]) -> Result[U, E]:
        """
        Композиция операций, возвращающих Result (flatMap)

        Args:
            f: Функция, принимающая значение и возвращающая новый Result

        Returns:
            Результат функции, если текущий Result успешен, иначе текущая ошибка
        """

        return f(self._value) if self.is_ok() else err(self._value)

    def or_else[F](self, op: Callable[[E], Result[T, F]]) -> Result[T, F]:
        """
        В случае ошибки применить операцию к ошибке и вернуть новый Result.
        В случае успеха вернуть исходный успешный результат без изменений.

        Полезен для обработки ошибок или восстановления после сбоев.
        """

        if self.is_ok():
            return ok(self._value)
        else:
            return op(self._value)

    def unwrap(self) -> T:
        """
        Извлечь успешное значение или вызвать исключение Panic при ошибке

        Внимание: Используйте только когда уверены в успешности результата,
        в противном случае используйте unwrap_or() или обработку ошибок

        Raises:
            Panic: При попытке извлечь значение из ошибочного результата
        """

        if self.is_ok():
            return self._value

        raise Panic(f"Attempt to unwrap an error: {self}")

    def unwrap_or(self, default: T) -> T:
        """
        Извлечь успешное значение или вернуть значение по умолчанию

        Args:
            default: Значение, возвращаемое в случае ошибки
        """

        return self._value if self.is_ok() else default

    def __repr__(self) -> str:
        status = "ok" if self.is_ok() else "err"
        return f"{status}({self._value})"


def ok[T](value: T) -> Result[T, Any]:
    """Создать успешный результат с заданным значением"""
    return Result(_is_ok=True, _value=value)


def err[E](error: E) -> Result[Any, E]:
    """Создать результат с заданной ошибкой"""
    return Result(_is_ok=False, _value=error)
