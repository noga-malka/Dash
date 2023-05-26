from typing import Union

from handlers.packetBuilders.builder import PacketBuilder


class SensorsPacketBuilder(PacketBuilder):
    @staticmethod
    def format(value: Union[str, int], byte_number: int = 1):
        formatter = f'{{:0>{byte_number * 2}}}'
        return formatter.format(value)

    def build_packet(self, command: int, content: Union[str, list], content_length: int):
        content = content if isinstance(content, list) else [content]
        parsed = "".join([self.__build_byte(byte, content_length) for byte in content])
        length = self.format(int(len(content) * content_length))
        return bytes.fromhex('aa55aa' + self.__build_byte(command) + length + parsed)

    def __build_byte(self, value: Union[str, int], length: int = 1):
        return self.format(hex(int(value)).replace('0x', ''), byte_number=length)
