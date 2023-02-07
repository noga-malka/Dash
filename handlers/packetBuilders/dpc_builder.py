from handlers.packetBuilders.builder import PacketBuilder


class DPCPacketBuilder(PacketBuilder):
    @staticmethod
    def build_packet(self, command: str, content: str = ''):
        return command + content + '\r'
