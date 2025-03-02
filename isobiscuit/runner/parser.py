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




opcodes = {
    "wa": [0x40, 0x41, 0x43, 0x44, 0x45, 0x46, 0x47, 0x4b],  # With Address Argument
    "al0": [0x4c],
    "al1": [0x2d, 0x43, 0x44, 0x45, 0x46, 0x47, 0x49, 0x4a, 0x4b],  # Argument Length 1
    "al2": [0x1b, 0x1c, 0x1d, 0x1e, 0x1f, 0x20, 0x2a, 0x2b, 0x2c, 0x2e, 0x2f, 0x40, 0x41, 0x42, 0x48]  # Argument Length 2
}

def parse_code_sector(code_sector_hex: str):
    code = binascii.unhexlify(code_sector_hex)
    offset = 0
    parsed_code = {}
    address = 0

    while offset < len(code):
        prefix = code[offset]
        offset += 1
        
        if prefix == 0x03:  # Special case for 0x03 prefix (no op)
            address += 1
        elif prefix in opcodes["al0"]:
            parsed_code[address] = (format(prefix, '02x'),)
            address += 1
        elif prefix in opcodes["al1"]:  # Argument Length 1
            if prefix in opcodes["wa"]:  # With Address Argument
                # Handle 4-byte address for 32-bit opcodes (e.g., LOAD, STORE)
                parsed_code[address] = (format(prefix, '02x'), struct.unpack(">I", code[offset:offset+4])[0])
                offset += 4
                address += 1
            else:
                parsed_code[address] = (format(prefix, '02x'), code[offset])
                offset += 1
                address += 1
        elif prefix in opcodes["al2"]:  # Argument Length 2
            arg1 = code[offset]
            offset += 1
            if prefix in opcodes["wa"]:  # With Address Argument (could be 32 or 64-bit)
                # Check if the instruction is one that uses 8-byte address (like JMP)
                
                    # Handle 4-byte address for 32-bit opcodes
                arg2 = struct.unpack(">I", code[offset:offset+4])[0]  # Unpack as 4-byte (32-bit)
                offset += 4
            else:  # Regular AL2 opcode
                arg2 = code[offset]
                offset += 1
                
            parsed_code[address] = (format(prefix, '02x'), arg1, arg2)
            address += 1
        else:
            print(parsed_code)
            raise ValueError(f"Unknown opcode: {hex(prefix)} at offset {offset}")

    return parsed_code