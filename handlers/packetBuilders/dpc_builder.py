from handlers.packetBuilders.builder import PacketBuilder


class DPCPacketBuilder(PacketBuilder):
    def build_packet(self, command: str, content: str = ''):
        return bytes(command + content + '\r', 'utf-8')
