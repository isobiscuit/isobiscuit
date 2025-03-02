REGISTERS = {
    "a": 0x10,
    "b": 0x11,
    "c": 0x12,
    "d": 0x13,
    "e": 0x14,
    "f": 0x15,
    "g": 0x16,
    "h": 0x17,
    "i": 0x18,
    "j": 0x19,
    "k": 0x1a,
    "l": 0x1b,
    "m": 0x1c,
    "n": 0x1d,
    "o": 0x1e,
    "p": 0x1f,
    "q": 0x20,
    "r": 0x21,
    "s": 0x22,
    "t": 0x23,
    "u": 0x24,
    "v": 0x25,
    "w": 0x26,
    "x": 0x27,
    "y": 0x28,
    "z": 0x29,
    "ax": 0x2a,
    "bx": 0x2b,
    "cx": 0x2c,
    "dx": 0x2d,
    "ix": 0x2e,
    "eax": 0x2f,
    "ebx": 0x30,
    "ecx": 0x31,
    "edx": 0x32,
    "eix": 0x33,
    "rax": 0x34,
    "rbx": 0x35,
    "rcx": 0x36,
    "rdx": 0x37,
    "rix": 0x38,
    "ip": 0x39,
    "sp": 0x3a,
    
}

OPCODES = {
    "add": 0x1b,
    "sub": 0x1c,
    "mul": 0x1d,
    "div": 0x1e,
    "mod": 0x1f,
    "exp": 0x20,
    "and": 0x2a,
    "or": 0x2b,
    "xor": 0x2c,
    "not": 0x2d,
    "shl": 0x2e,
    "shr": 0x2f,
    "load": 0x40,
    "store": 0x41,
    "cmp": 0x42,
    "jmp": 0x43,
    "je": 0x44,
    "jne": 0x45,
    "jg": 0x46,
    "jl": 0x47,
    "mov": 0x48,
    "int": 0x49,
    "mode": 0x4a,
    "call": 0x4b,
    "ret": 0x4c
        
}

MODES = {
    "biscuit": 0x12,
    "linux": 0x13,
}

def get_address(s: str, procs: dict):
    if s.startswith("0x"):
        return hex(int(s[2:], 16))[2:].zfill(8)
    if s.endswith("h"):
        return hex(int(s[:-1], 16))[2:].zfill(8)
    
    return hex(procs[s])[2:].zfill(8)
    
    
