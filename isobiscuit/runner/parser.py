import binascii
import struct



def parse_data_sector(data_sector_hex: str):
    data = binascii.unhexlify(data_sector_hex)
    offset = 0
    parsed_data = {}
    address = 0
    while offset < len(data):
        prefix = data[offset]
        if prefix == 0x00:
            offset += 1
            address += 1
        elif prefix == 0x01:
            offset += 1
            string_data = b""
            while offset < len(data) and data[offset] != 0x02:
                string_data += bytes([data[offset]])
                offset += 1
            offset += 1
            parsed_data[address] = string_data.decode()
            address += 1
        elif prefix == 0x04:
            offset += 1
            int_value = struct.unpack(">I", data[offset:offset+4])[0]
            parsed_data[address] = int_value
            offset += 4
            address += 1
        elif prefix == 0x05:
            offset += 1
            int_value = struct.unpack(">Q", data[offset:offset+8])[0]
            parsed_data[address] = int_value
            offset += 8
            address += 1
        else:
            raise ValueError(f"Unknown prefix: {hex(prefix)} at offset {offset}")
    return parsed_data

