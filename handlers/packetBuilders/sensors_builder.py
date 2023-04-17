from typing import Union

from handlers.packetBuilders.builder import PacketBuilder


class SensorsPacketBuilder(PacketBuilder):
    @staticmethod
    def format(value: Union[str, int], byte_number: int = 1):
        formatter = f'{{:0>{byte_number * 2}}}'
        return formatter.format(value)

    def build_packet(self, command: int, content: str, content_length: int):
        content = self.format(hex(int(content)).replace('0x', ''), byte_number=content_length)
        command = self.format(hex(int(command)).replace('0x', ''))
        length = self.format(int(len(content) / 2))
        return bytes.fromhex('aa55aa' + command + length + content)
