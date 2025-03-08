import time
from .codes import MODES, OPCODES, REGISTERS, get_address
import glob


add_later_ops = [
    "load",
    "store",
    "jmp",
    "je",
    "jne",
    "jg",
    "jl",
    "call"
]


def parse(files: list[str], debug=False):
    code = ""
    for _ in files:
        for file in glob.glob(_, recursive=True):
            with open(file, "r") as f:
                code += f.read() + "\n"
    code = code.replace("\t", " ")
    code = code.replace("  ", " ")
    code = code.replace("   ", " ")
    code = code.replace("  ", " ")
    code = code.replace("\n\n", "\n")
    code = code.removeprefix(" ")
    _code = code.split("\n")
    code = ""
    for line in _code:
        if line != "":
            if line.startswith(" "):
                code += line[1:]+"\n"
            if line.startswith(";;"):
                pass
            else:
                code+=line+"\n"
    code = code[:-1]
    if debug:
        print(f"parse code: {code}")
    cmds=[]
    for line in code.split("\n"):
        
        line = line.split(" ")
        if line[0] == "org":
            cmds.append([line[0], line[1]])
        elif line[0] == "mov":
            cmds.append([line[0], line[1], line[2]])
        
        elif line[0] == "mode":
            cmds.append(["mode", line[1]])
        elif line[0] == "int":
            cmds.append(["int", line[1]])
        

        elif line[0] == "jmp":
            cmds.append(["jmp", line[1]])
        elif line[0] == "load":
            cmds.append(["load", line[1], line[2]])
        elif line[0] == "store":
            cmds.append(["store", line[1], line[2]])
        elif line[0] == "cmp":
            cmds.append(["cmp", line[1], line[2]])
        elif line[0] == "je":
            cmds.append(["je", line[1]])
        elif line[0] == "jne":
            cmds.append(["jne", line[1]])
        elif line[0] == "jg":
            cmds.append(["jg", line[1]])
        elif line[0] == "jl":
            cmds.append(["jl", line[1]])
        elif line[0] == "call":
            cmds.append(["call", line[1]])
        elif line[0] == "ret":
            cmds.append(["ret"])
        elif line[0].startswith("0x"):
            cmds.append([line[0]])
        elif line[0].endswith("h"):
            cmds.append([f"0x{line[0][:-1]}"])








        elif line[0] == "add":
            cmds.append(["add", line[1], line[2]])

        elif line[0] == "sub":
            cmds.append(["sub", line[1], line[2]])

        elif line[0] == "mul":
            cmds.append(["mul", line[1], line[2]])

        elif line[0] == "div":
            cmds.append(["div", line[1], line[2]])

        elif line[0] == "mod":
            cmds.append(["mod", line[1], line[2]])
        elif line[0] == "exp":
            cmds.append(["exp", line[1], line[2]])
        


        elif line[0] == "and":
            cmds.append(["and", line[1], line[2]])
        elif line[0] == "or":
            cmds.append(["or", line[1], line[2]])
        elif line[0] == "xor":
            cmds.append(["xor", line[1], line[2]])
        elif line[0] == "not":
            cmds.append(["not", line[1]])
        elif line[0] == "shl":
            cmds.append(["shl", line[1], line[2]])
        elif line[0] == "shr":
            cmds.append(["shr", line[1], line[2]])
        










        elif line[0].endswith(":"):
            cmds.append(["PROC", line[0][:-1]])
    if debug:
        print(f"Parsed cmds: {cmds}")
    return cmds







def binify(files: list[str], debug=False):
    cmds = parse(files, debug)
    #print(cmds)
    codes = {}
    data = {}    
    procs = {}
    add_later = []
    counter = 0x0
    for cmd in cmds:
        if debug:
            print(cmd)
        if cmd[0] == "org":
            new =   int(cmd[1], 16) - counter
            for i in range(0, new):
                codes[counter] = [0x03]
                counter+=1
            continue

        if cmd[0] == "PROC":
            procs[cmd[1]] = counter
            continue

        if str(cmd[0]).startswith("0x'"):
            s1 = str(cmd[0][3:])
            s2 = str(s1[:-1])
            l1 = s2.split(",")
            l2 = [0x01]
            for i in l1:
                l2.append(int(i, 16))
            l2.append(0x02)
            data[counter] = l2
            codes[counter] = [0x03]
        elif str(cmd[0]).startswith("0x"):
            data[counter] = int(cmd[0], 16)
            codes[counter] = [0x03]
        if cmd[0] == "cmp":
            codes[counter] = [OPCODES["cmp"], REGISTERS[cmd[1]], REGISTERS[cmd[2]]]
        if cmd[0] == "mov":

            codes[counter] = [OPCODES["mov"], REGISTERS[cmd[1]], REGISTERS[cmd[2]]]

        if cmd[0] == "ret":
            codes[counter] = [OPCODES["ret"]]
        if cmd[0] == "int":
            codes[counter] = [OPCODES["int"], int(cmd[1], 16)]


        if cmd[0] == "mode":
            codes[counter] = [OPCODES["mode"], MODES[cmd[1]]]


        if cmd[0] == "add":
            codes[counter] = [OPCODES["add"], REGISTERS[cmd[1]], REGISTERS[cmd[2]]]


        if cmd[0] == "sub":
            codes[counter] = [OPCODES["sub"], REGISTERS[cmd[1]], REGISTERS[cmd[2]]]


        if cmd[0] == "mul":
            codes[counter] = [OPCODES["mul"], REGISTERS[cmd[1]], REGISTERS[cmd[2]]]


        if cmd[0] == "div":
            codes[counter] = [OPCODES["div"], REGISTERS[cmd[1]], REGISTERS[cmd[2]]]


        if cmd[0] == "mod":
            codes[counter] = [OPCODES["mod"], REGISTERS[cmd[1]], REGISTERS[cmd[2]]]


        if cmd[0] == "exp":
            codes[counter] = [OPCODES["exp"], REGISTERS[cmd[1]], REGISTERS[cmd[2]]]


        if cmd[0] == "and":
            codes[counter] = [OPCODES["and"], REGISTERS[cmd[1]], REGISTERS[cmds[2]]]
        if cmd[0] == "or":
            codes[counter] = [OPCODES["or"], REGISTERS[cmd[1]], REGISTERS[cmds[2]]]
        if cmd[0] == "xor":
            codes[counter] = [OPCODES["xor"], REGISTERS[cmd[1]], REGISTERS[cmds[2]]]
        
        if cmd[0] == "not":
            codes[counter] = [OPCODES["not"], REGISTERS[cmd[1]]]

        if cmd[0] == "shl":
            codes[counter] = [OPCODES["shl"], REGISTERS[cmd[1]], cmd[2]]
        if cmd[0] == "shr":
            codes[counter] = [OPCODES["shr"], REGISTERS[cmd[1]], cmd[2]]
        

        
        if cmd[0] in add_later_ops:
            codes[counter] = []
            add_later.append([counter, cmd])

        
        counter+=1
    

    for i in add_later:
        address = i[0]
        cmd = i[1]
        if debug:
            print(f"resolve proc: [{cmd}: {address}]")
        if cmd[0] == "load":
            codes[address] = [OPCODES["load"], REGISTERS[cmd[1]], get_address(cmd[2], procs)]
        if cmd[0] == "store":
            codes[address] = [OPCODES["store"], REGISTERS[cmd[1]], get_address(cmd[2], procs)]

        if cmd[0] == "jmp":
            codes[address] = [OPCODES["jmp"], get_address(cmd[1], procs)]


        if cmd[0] == "je":
            codes[address] = [OPCODES["je"], get_address(cmd[1], procs)]



        if cmd[0] == "jne":
            codes[address] = [OPCODES["jne"], get_address(cmd[1], procs)]



        if cmd[0] == "jg":
            codes[address] = [OPCODES["jg"], get_address(cmd[1], procs)]



        if cmd[0] == "jl":
            codes[address] = [OPCODES["jl"], get_address(cmd[1], procs)]
        if cmd[0] == "call":
            codes[address] = [OPCODES["call"], get_address(cmd[1], procs)]


    return (codes, data, counter)    


