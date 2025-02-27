from .binify import binify
import struct




def to_binary_array(d: dict[str, int|list], counter):
    b = []
    
    for i in range(0, counter):
        if isinstance(d.get(i), int):
            bits = d[i].bit_length()
            bytes_required = (bits + 7) // 8
            if bytes_required <= 4:
                b.append(0x04)
                bits = 32
            else:
                bits = 64
                b.append(0x05)
            b.extend(list(d[i].to_bytes(bits//8)))
        elif isinstance(d.get(i), list):
            for i2 in d[i]:
                b.append(i2)
        else:
            b.append(0)
        
    return str(bytes(bytearray(b)).hex())
            
    



def compile(files: list[str]):
    code = binify(files)
    data = to_binary_array(code[1], code[2])
    code = to_binary_array(code[0], code[2])   
    return (code, data)
