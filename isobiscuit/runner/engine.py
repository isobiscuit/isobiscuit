import colorama
import time
import socket


colorama.init()
hardware_memory_addresses = [
    0xFFFF0000,
    0xFFFF0100,
    0xFFFF0101,
    0xFFFF0102,
    0xFFFF0103,
    0xFFFF0104,
    0xFFFF0105,
    0xFFFF0106,
    0xFFFF0107,
]

class Engine:
    def __init__(self, data_sector, code_sector, mem_sector, debug=False):
        self.hardware = Hardware(debug)
        self.debug = debug
        self.register = {i: 0 for i in range(0x10, 0x3C)}
        self.memory = {**data_sector, **code_sector}
        self.flags = {'ZF': 0, 'CF': 0, 'SF': 0, 'OF': 0}
        self.pc = 0
        self.code_addresses = list(code_sector.keys())
        self.code_len = len(self.code_addresses)
        self.ret_pcs = []
        self.OPCODES = {
            '1b': self.add, '1c': self.sub, '1d': self.mul, '1e': self.div,
            '1f': self.mod, '20': self.pow, '2a': self.and_op, '2b': self.or_op,
            '2c': self.xor, '2d': self.not_op, '2e': self.shl, '2f': self.shr,
            '40': self.load, '41': self.store, '42': self.cmp, '43': self.jmp,
            '44': self.je, '45': self.jne, '46': self.jg, '47': self.jl,
            '48': self.mov, '49': self.interrupt, '4a': self.change_mode,
            '4b': self.call, '4c': self.ret
        }
        for i in hardware_memory_addresses:
            self.memory[i] = None

    def run(self):
        try:
            while self.pc < self.code_len:
                address = self.code_addresses[self.pc]
                op = self.memory[address]
                if self.debug:
                    print(f"[Execute] [Address:{hex(address)}] {op}")
                self.execute(op)
                self.pc += 1
        except KeyError as e:
            print(f"[ERROR] Key Error: {e}")
            raise e

    def execute(self, op):
        opcode: str = op[0]
        if opcode in self.OPCODES:
            self.OPCODES[opcode](op) 
        else:
            raise ValueError(f"Unknown opcode: {opcode}")

    def add(self, op): self.register[op[1]] += self.register[op[2]]
    def sub(self, op): self.register[op[1]] -= self.register[op[2]]
    def mul(self, op): self.register[op[1]] *= self.register[op[2]]
    def div(self, op): self.register[op[1]] //= self.register[op[2]]
    def mod(self, op): self.register[op[1]] %= self.register[op[2]]
    def pow(self, op): self.register[op[1]] **= self.register[op[2]]

    def and_op(self, op): self.register[op[1]] &= self.register[op[2]]
    def or_op(self, op): self.register[op[1]] |= self.register[op[2]]
    def xor(self, op): self.register[op[1]] ^= self.register[op[2]]
    def not_op(self, op): self.register[op[1]] = ~self.register[op[1]]
    def shl(self, op): self.register[op[1]] <<= op[2]
    def shr(self, op): self.register[op[1]] >>= op[2]

    def load(self, op): self.register[op[1]] = self.memory[op[2]]
    def store(self, op): self.memory[op[2]] = self.register[op[1]]

    def jmp(self, op): self.jump(op[1])
    def je(self, op):  # Jump if equal
        if self.flags['ZF']: self.jump(op[1])
    def jne(self, op):  # Jump if not equal
        if not self.flags['ZF']: self.jump(op[1])
    def jg(self, op):  # Jump if greater
        if not self.flags['ZF'] and self.flags['SF'] == self.flags['OF']: self.jump(op[1])
    def jl(self, op):  # Jump if less
        if self.flags['SF'] != self.flags['OF']: self.jump(op[1])

    def mov(self, op): self.register[op[1]] = self.register[op[2]]

    
    def change_mode(self, op):
        mode = op[1]
        print("[INFO] mode changing is in developing")
        self.mode = mode



    def interrupt(self, op):
        interrupt = op[1]
        if interrupt == 0x45:
            self.biscuit_call()
        elif interrupt == 0x80:
            self.syscall()






    def biscuit_call(self):
        call = self.register[0x2f]
        if call == 0x00:
            arg1 = self.register[0x30]
            exit(arg1)
        elif call == 0x01:
            hardware_memory = {}
            for i in hardware_memory_addresses:
                if self.debug:
                    print(f"[UPDATE] Updating Hardware address: {i}")
                hardware_memory[i] = self.memory[i]
            result = self.hardware.update(hardware_memory)
            self.memory.update(result)
        elif call == 0x02:
            arg1 = self.register[0x30]/1000
            time.sleep(arg1)
        elif call == 0x03:
            arg1 = self.register[0x30]
            
            result = input(arg1)
            self.register[0x2f] = result

        elif call == 0x04:
            arg1 = self.register[0x30]
            arg2 = self.register[0x31]
    
            if arg1 == 0x01:
                print(arg2)
        elif call == 0x05:
            print(f"Memory: {self.memory}")
            print(f"Stack: {self.stack}")
            print(f"Flags: {self.flags}")
            print(f"Program Counter: {self.pc}")
            print(f"Mode: {self.mode}")
            print(f"Code Sector Index: {self.code_addresses}")
            


    def syscall(self):
        #syscall = self.register[0x2f]
        print("[INFO] Syscalls are in developing")










































































































    def call(self, op):
        self.ret_pcs.append(self.pc)
        self.jump(op[1])
    def ret(self, op):
        pc = self.ret_pcs.pop()
        self.pc = pc





    def cmp(self, op):
        r1 = op[1]
        r2 = op[2]
        val1 = self.register[r1]
        val2 = self.register[r1]
        if isinstance(val1, str) or isinstance(val2, str):
            if val1 == val2:
                self.flags['ZF'] = 1
            else:
                self.flags['ZF'] = 0
            return
        result = val1 - val2
        
        if result == 0:
            self.flags['ZF'] = 1
        else:
            self.flags['ZF'] = 0
        
        if result < 0:
            self.flags['SF'] = 1
        else:
            self.flags['SF'] = 0
        
        if self.register[r1] < self.register[r2]:
            self.flags['CF'] = 1
        else:
            self.flags['CF'] = 0
        
        
        if ((self.register[r1] < 0 and self.register[r2] > 0 and result > 0) or
            (self.register[r1] > 0 and self.register[r2] < 0 and result < 0)):
            self.flags['OF'] = 1
        else:
            self.flags['OF'] = 0


    def update_register(self, register: int, value):
        if register > 0xf and register < 0x2a:
            self.register[register] = bool(value)
        else:
            self.register[register] = value
    def jump(self, address):
        self.pc = self.code_addresses.index(address)-1


    def _update_1bit_register(self, register: int, value: bool):
        register[register] = value
    
    def _update_register(self, register: int, value):
        register[register] = value


    

class Hardware:
    def __init__(self, debug):
        self.hardware_memory = {}
        self.debug = debug
        self.inet_connection = dict[int, socket.socket]()
    def update(self, hardware_memory): #Hardware memory is the memory of the engine with 0xFFFF####
        self.hardware_memory = hardware_memory
        self.update_color()
        self.internet()

        return self.hardware_memory

    def update_color(self):
        # Change color of terminal
        # Colors are hexadezimal
        # 0xFFFF0000 Color
        color = self.hardware_memory[0xFFFF_0000]


        match color:
            case 0x0:
                color = colorama.Fore.RESET
            case 0x1:
                color = colorama.Fore.WHITE
            case 0x2:
                color = colorama.Fore.BLACK
            case 0x3:
                color = colorama.Fore.YELLOW
            case 0x4:
                color = colorama.Fore.RED
            case 0x5:
                color = colorama.Fore.BLUE
            case 0x6:
                color = colorama.Fore.GREEN
            case 0x7:
                color = colorama.Fore.MAGENTA
            case 0x8:
                color = colorama.Fore.CYAN
            case 0x9:
                color = colorama.Fore.LIGHTYELLOW_EX
            case 0xa:
                color = colorama.Fore.LIGHTBLACK_EX
            case 0xb:
                color = colorama.Fore.LIGHTCYAN_EX
            case 0xc:
                color = colorama.Fore.LIGHTMAGENTA_EX
            case 0xd:
                color = colorama.Fore.LIGHTGREEN_EX
            case 0xe:
                color = colorama.Fore.LIGHTWHITE_EX
            case 0xf:
                color = colorama.Fore.LIGHTRED_EX
            case _: return
        print(color, end="")
    def internet(self):
        action = self.hardware_memory[0xFFFF_0100]
        if action == None:
            return
        else:
            port = int(self.hardware_memory[0xFFFF_0104])
            if action == 0x00: # Listen
                fam  = self.hardware_memory[0xFFFF_0101]
                kind = self.hardware_memory[0xFFFF_0102]
                host = self.hardware_memory[0xFFFF_0103]
                if host == None:return
                if fam == 0x00: # Inet:
                    fam = socket.AF_INET
                else:
                    if self.debug:
                        print(f"Invalid family of socket: {fam}")
                    return
                if kind == 0x00: # UPD
                    kind = socket.SOCK_DGRAM
                elif kind == 0x01: # TCP
                    kind = socket.SOCK_STREAM
                else:
                    if self.debug:
                        print(f"Invalid kind of socket: {kind}")
                    return
                sock = socket.socket(fam, kind)
                sock.bind((socket.gethostbyname(host), port))
                self.inet_connection[port] = sock
            elif action == 0x01: # Connect
                fam  = self.hardware_memory[0xFFFF_0101]
                kind = self.hardware_memory[0xFFFF_0102]
                host = self.hardware_memory[0xFFFF_0103]
                if host == None:return
                if fam == 0x00: # Inet:
                    fam = socket.AF_INET
                else:
                    if self.debug:
                        print(f"Invalid family of socket: {fam}")
                    return
                if kind == 0x00: # UPD
                    kind = socket.SOCK_DGRAM
                elif kind == 0x01: # TCP
                    kind = socket.SOCK_STREAM
                else:
                    if self.debug:
                        print(f"Invalid kind of socket: {kind}")
                    return
                sock = socket.socket(fam, kind)
                sock.connect((socket.gethostbyname(host), port))
                self.inet_connection[port] = sock
            elif action == 0x02: #send
                message = self.hardware_memory[0xFFFF_0105]
                sock: socket.socket = self.inet_connection[port]
                
                sock.send(bytes(message, encoding="utf8"))
            elif action == 0x03: # recv
                bufsize: int = self.hardware_memory[0xFFFF_0106]
                sock = self.inet_connection[port]
                msg = sock.recv(bufsize)
                self.hardware_memory[0xFFFF_0107] = msg
            elif action == 0x04: # exit
                
                self.inet_connection[port].close()
        self.hardware_memory[0xFFFF_0100] = None
                
        
        
