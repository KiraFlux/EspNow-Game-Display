from dataclasses import dataclass
from dataclasses import field
from typing import Callable
from typing import Iterable

from rs.result import Result
from rs.result import err
from serialcmd.abc.serializer import Serializable
from serialcmd.abc.serializer import Serializer
from serialcmd.abc.stream import Stream
from serialcmd.core.instruction import Instruction
from serialcmd.impl.serializer.primitive import PrimitiveSerializer


@dataclass(kw_only=True, frozen=True)
class Protocol:
    """Протокол P2P общения по потоку"""

    type OnReceiveFunction[T] = Callable[[T], Result[None, str]]
    """Вид обработчика приёма"""

    _stream: Stream
    """Поток общения"""

    _local_instruction_code: PrimitiveSerializer[int]
    """Ширина локального кода инструкции (Локально: приём)"""
    _remote_instruction_code: PrimitiveSerializer[int]
    """Ширина удаленного кода инструкции (Локально: отправка)"""

    _receive_handlers: dict[bytes, tuple[Instruction, OnReceiveFunction]] = field(init=False, default_factory=dict)
    """Обработчики на приём"""
    _send_handlers: dict[bytes, Instruction] = field(init=False, default_factory=dict)
    """Обработчики на передачу"""

    def getReceivers(self) -> Iterable:
        """Получить вид на обработчиков приёма"""
        return self._receive_handlers.values()

    def getSenders(self) -> Iterable:
        """Получить вид на обработчиков отправки"""
        return self._send_handlers.values()

    def registerReceiver[T: Serializable](
            self,
            name: str,
            signature: Serializer[T],
            handler: OnReceiveFunction[T]
    ) -> Result[None, str]:
        """Зарегистрировать обработчик приёма сообщений"""

        def _register_handler(instruction: Instruction[T], f: Callable) -> None:
            self._receive_handlers[instruction.code] = (instruction, f)

        index = len(self._receive_handlers)

        return (
            self._local_instruction_code.pack(index)
            .map(lambda code: _register_handler(Instruction(code, name, signature), handler))
            .map_err(lambda e: f"Protocol register receiver error: {e}")
        )

    def registerSender[T: Serializable](
            self,
            name: str,
            signature: Serializer[T]
    ) -> Result[Instruction[T], str]:
        """Зарегистрировать обработчик отправки сообщений"""

        def _register_handler(instruction: Instruction[T]) -> Instruction[T]:
            self._send_handlers[instruction.code] = instruction
            return instruction

        index = len(self._send_handlers)

        return (
            self._remote_instruction_code.pack(index)
            .map(lambda code: Instruction[T](code, name, signature))
            .map(_register_handler)
            .map_err(lambda e: f"Protocol register sender error: {e}")
        )

    def pull(self) -> Result[None, str]:
        """Обработка входящих сообщений"""

        code_result = self._stream.read(self._remote_instruction_code.getSize())

        if code_result.is_err():
            return code_result.map(lambda _: None).map_err(lambda e: f"Code read error: {e}")

        handler_info = self._receive_handlers.get(code_result.unwrap())

        if not handler_info:
            return err(f"Invalid code: {code_result.unwrap().hex()}")

        instruction, handler = handler_info
        args_result = instruction.receive(self._stream)

        if args_result.is_err():
            return args_result.map_err(lambda e: f"Arguments read error: {e}")

        return handler(args_result.unwrap())
