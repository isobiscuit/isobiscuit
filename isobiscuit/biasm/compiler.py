from .binify import binify
import struct
import binascii



def to_binary_array(d: dict[str, int|list|str], counter):
    b = []
    
    for i in range(0, counter):
        item = d.get(i)
        if isinstance(item, int):
            bits = item.bit_length()
            bytes_required = (bits + 7) // 8
            if bytes_required <= 4:
                b.append("04")
                bits = 32
            else:
                bits = 64
                b.append("05")
            b.extend(str(item.to_bytes(bits//8).hex()))
        elif isinstance(item, list):
            for i2 in item:
                if isinstance(i2, int):
                    b.append(str(i2))
                elif isinstance(i2, str):
                    b.append(i2)
        else:
            b.append(str("00"))
        
    return "".join(b)
            



def compile(files: list[str]):
    code = binify(files)
    data = to_binary_array(code[1], code[2])
    code = to_binary_array(code[0], code[2])   
    return (code, data)

print(compile(["test.biasm"]))