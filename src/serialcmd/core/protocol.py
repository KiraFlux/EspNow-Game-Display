from typing import Callable
from typing import Final

from rs.result import Result
from rs.result import err
from rs.result import ok
from serialcmd.abc.serializer import Serializable
from serialcmd.abc.serializer import Serializer
from serialcmd.abc.stream import Stream
from serialcmd.core.instruction import Instruction
from serialcmd.impl.serializer.primitive import PrimitiveSerializer

type OnReceiveFunction[T] = Callable[[T], Result[None, str]]
"""Вид обработчика приёма"""


class Protocol:
    """Протокол P2P общения по потоку с указанной структурой полей"""

    def __init__(
            self,
            stream: Stream,
            local_code: PrimitiveSerializer[int],
            remote_code: PrimitiveSerializer[int]
    ) -> None:
        self._stream: Final = stream
        self._local_instruction_code: Final = local_code
        self._remote_instruction_code: Final = remote_code
        self._receive_handlers: Final = dict[bytes, tuple[Instruction, OnReceiveFunction]]()
        self._send_handlers: Final = dict[bytes, Instruction]()

    def addReceiver[T: Serializable](
            self,
            name: str,
            signature: Serializer[T],
            handler: OnReceiveFunction[T]
    ) -> Result[None, str]:
        """Зарегистрировать обработчик входящих сообщений"""
        # Генерируем код для нового обработчика
        index = len(self._receive_handlers)
        code_result = self._local_instruction_code.pack(index)

        if code_result.is_err():
            return code_result.map(lambda _: None).map_err(
                lambda e: f"Failed to pack receiver code: {e}")

        code = code_result.unwrap()

        # Создаем инструкцию
        instruction = Instruction[T](code, name, signature)

        # Регистрируем обработчик
        self._receive_handlers[code] = (instruction, handler)
        return ok(None)

    def addSender[T: Serializable](
            self,
            name: str,
            signature: Serializer[T]
    ) -> Result[Instruction[T], str]:
        """Зарегистрировать исходящую инструкцию"""
        # Генерируем код для новой инструкции
        index = len(self._send_handlers)
        code_result = self._remote_instruction_code.pack(index)

        if code_result.is_err():
            # noinspection PyTypeChecker
            return code_result.map_err(lambda e: f"Failed to pack sender code: {e}")

        code = code_result.unwrap()

        # Создаем инструкцию
        instruction = Instruction[T](code, name, signature)

        # Регистрируем инструкцию
        self._send_handlers[code] = instruction
        return ok(instruction)

    def pull(self) -> Result[None, str]:
        """Обработать входящее сообщение"""
        # Читаем код инструкции
        code_size = self._remote_instruction_code.getSize()
        code_result = self._stream.read(code_size)

        if code_result.is_err():
            return code_result.map(lambda _: None).map_err(
                lambda e: f"Failed to read instruction code: {e}")

        code = code_result.unwrap()

        # Находим зарегистрированный обработчик
        if code not in self._receive_handlers:
            return err(f"Unknown instruction code: {code.hex()}")

        instruction, handler = self._receive_handlers[code]

        # Читаем аргументы
        args_result = instruction.receive(self._stream)
        if args_result.is_err():
            return args_result.map_err(
                lambda e: f"Failed to receive arguments: {e}").map(lambda _: None)

        # Вызываем обработчик
        return handler(args_result.unwrap())
