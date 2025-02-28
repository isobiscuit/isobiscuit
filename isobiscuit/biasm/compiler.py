from .binify import binify
import struct




def to_binary_array(d: dict[str, int|list|str], counter):
    b = []
    
    for i in range(0, counter):
        item = d.get(i)
        if isinstance(item, int):
            bits = item.bit_length()
            bytes_required = (bits + 7) // 8
            if bytes_required <= 4:
                b.append(0x04)
                bits = 32
            else:
                bits = 64
                b.append(0x05)
            b.extend(list(item.to_bytes(bits//8)))
        elif isinstance(item, list):
            for i2 in item:
                if isinstance(i2, int):
                    b.append(i2)
                elif isinstance(i2, str):
                    for i3 in range(0, len(i2)):
                        i4 = i2[i3:i3+2]
                        b.append(int(i4, 16))
        else:
            b.append(0)
        
    return str(bytes(bytearray(b)).hex())
            
    



def compile(files: list[str]):
    code = binify(files)
    data = to_binary_array(code[1], code[2])
    code = to_binary_array(code[0], code[2])   
    return (code, data)

