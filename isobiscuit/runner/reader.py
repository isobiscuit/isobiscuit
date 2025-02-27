import binascii
from .magic import MAGIC

def read_biscuit_as_hex(filepath):
    with open(filepath, "rb") as f:
        data = f.read()
    return binascii.hexlify(data).decode("utf-8")

def check_header(biscuit: str):
    if not biscuit.startswith(MAGIC):
        raise ValueError("This is not a Biscuit or the file was manipulated")
    biscuit = biscuit[32:]
    data_sector_len   = int(int(biscuit[:32], 16) / 8)*2
    biscuit = biscuit[32:]
    code_sector_len   = int(int(biscuit[:32], 16) / 8)*2
    biscuit = biscuit[32:]
    mem_sector_len    = int(int(biscuit[:32], 16) / 8)*2
    biscuit = biscuit[32:]
    other_sectors_len = int(int(biscuit[:32], 16) / 8)*2
    biscuit = biscuit[32:]
    
    return (
        biscuit,
        data_sector_len,
        code_sector_len,
        mem_sector_len,
        other_sectors_len
    )

def get_sectors(biscuit, data_len, code_len, mem_len, other_len):
    data_sector = biscuit[:data_len]
    biscuit = biscuit[data_len:]
    code_sector = biscuit[:code_len]
    biscuit = biscuit[code_len:]
    mem_sector = biscuit[:mem_len]
    biscuit = biscuit[mem_len:]
    other_sector = biscuit[:other_len]
    biscuit = biscuit[other_len:]

    zip = biscuit
    return (
        data_sector,
        code_sector,
        mem_sector,
        other_sector,
        zip
    )
    
    





def read(filepath):
    biscuit = read_biscuit_as_hex(filepath)
    
    (biscuit, data_len, code_len, mem_len, other_len) = check_header(biscuit)
    biscuit = get_sectors(biscuit, data_len, code_len, mem_len, other_len)
    return biscuit