class PacketBuilder:
    def build_packet(self, command, content, content_length: int):
        raise NotImplementedError
