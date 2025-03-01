from .binify import binify
import struct
import binascii

def data_to_binary_array(d: dict[str, int|list], counter):
    b = []
    
    for i in range(counter):
        if isinstance(d.get(i), int):
            bits = d[i].bit_length()
            
            bytes_required = (bits + 7) // 8
            
            if bytes_required <= 4:
                b.append(0x04)
                bits = 32
            else:
                b.append(0x05)
                bits = 64
            
            b.extend(list(d[i].to_bytes(bits // 8, byteorder='big')))
        
        elif isinstance(d.get(i), list):
            for elem in d[i]:
                b.append(elem)
        else:
            b.append(0x00)
    return bytes(bytearray(b)).hex()

def code_to_binary_array(d: dict[str, int|list|str], counter):
    b = []
    
    for i in range(0, counter):
        item = d.get(i)
        
        if isinstance(item, list):
            for i2 in item:
                
                if isinstance(i2, int):
                    _ = str(hex(i2)[2:].zfill(2))
                    b.append(_)
                elif isinstance(i2, str):
                    _ = i2.zfill(8)
                    b.append(_)
        else:
            b.append("00")
        
    return "".join(b)
            



def compile(files: list[str], debug=False):
    code = binify(files, debug)
    data = data_to_binary_array(code[1], code[2])
    code = code_to_binary_array(code[0], code[2])   
    return (code, data)
