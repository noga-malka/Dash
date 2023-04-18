from typing import Union

from handlers.packetBuilders.builder import PacketBuilder


class TextPacketBuilder(PacketBuilder):
    @staticmethod
    def format(value: Union[str, int], byte_number: int = 1):
        formatter = f'{{:0>{byte_number * 2}}}'
        return formatter.format(value)

    def build_packet(self, command: int, content: str, content_length: int):
        command = self.format(hex(int(command)).replace('0x', ''))
        length = self.format(hex(len(content)).replace('0x', ''))
        return bytes.fromhex('aa55aa' + command + length) + bytes(content, 'ascii')
