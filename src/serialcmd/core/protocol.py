from typing import Callable
from typing import Final
from typing import Iterable

from rs.result import Result
from rs.result import err
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

    def getSenders(self) -> Iterable:
        """Получить все обработчики на отправку"""
        return self._send_handlers.values()

    def getReceivers(self) -> Iterable:
        """Получить все обработчики на приём"""
        return (i for i, j in self._receive_handlers.values())

    def addReceiver[T: Serializable](self, signature: Serializer[T], handler: OnReceiveFunction[T], name: str = None) -> None:
        """Зарегистрировать обработчик входящих сообщений"""
        index = len(self._receive_handlers)
        code = self._local_instruction_code.pack(index).unwrap()
        instruction = Instruction(code, signature, name)
        self._receive_handlers[code] = (instruction, handler)

    def addSender[T: Serializable](self, signature: Serializer[T], name: str = None) -> Instruction[T]:
        """Зарегистрировать исходящую инструкцию"""
        index = len(self._send_handlers)
        code = self._remote_instruction_code.pack(index).unwrap()
        instruction = Instruction(code, signature, name)
        self._send_handlers[code] = instruction
        return instruction

    def pull(self) -> Result[None, str]:
        """Обработать входящее сообщение"""
        code_size = self._remote_instruction_code.getSize()
        code_result = self._stream.read(code_size)

        if code_result.is_err():
            return code_result.map(lambda _: None).map_err(
                lambda e: f"Failed to read instruction code: {e}")

        code = code_result.unwrap()

        if code not in self._receive_handlers:
            return err(f"Unknown instruction code: {code.hex()}")

        instruction, handler = self._receive_handlers[code]
        args_result = instruction.receive(self._stream)

        if args_result.is_err():
            return args_result.map_err(lambda e: f"Failed to receive arguments: {e}").map(lambda _: None)

        return handler(args_result.unwrap())
