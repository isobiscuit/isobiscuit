import colorama
import time
import socket


colorama.init()
hardware_memory_addresses = [
    0xFFFF0000
]

class Engine:
    def __init__(self, data_sector: dict,
                  code_sector: dict[int, tuple[str|int]],
                  mem_sector: dict,
                  debug=False
                ):
        self.debug = debug
        self.ret_pcs = []
        self.stack = []
        self.register = {
            0x10: False,
            0x11: False,
            0x12: False,
            0x13: False,
            0x14: False,
            0x15: False,
            0x16: False,
            0x17: False,
            0x18: False,
            0x19: False,
            0x1a: False,
            0x1b: False,
            0x1c: False,
            0x1d: False,
            0x1e: False,
            0x1f: False,
            0x20: False,
            0x21: False,
            0x22: False,
            0x23: False,
            0x24: False,
            0x25: False,
            0x26: False,
            0x27: False,
            0x28: False,
            0x29: False,
            
            0x2A: None,
            0x2B: None,
            0x2C: None,
            0x2D: None,
            0x2E: None,
            0x2F: None,
            0x30: None,
            0x31: None,
            0x32: None,
            0x33: None,
            0x34: None,
            0x35: None,
            0x36: None,
            0x37: None,
            0x38: None,
            0x3A: None,
            0x3B: None,
            
            
        }

        self._code_sector = code_sector
        self._data_sector = data_sector
        self.memory = {
            0xFFFF0000: None
        }
        self.memory.update(mem_sector)
        self.memory.update(data_sector)
        self.memory.update(code_sector)
        self.in_cmp_mode = False
        self.flags = {
            'ZF': 0,
            'CF': 0,
            'SF': 0,
            'OF': 0
        }
        self.pc = 0
        self.code_addresses = list(code_sector.keys())
        self.code_len = len(self.code_addresses)
        self.mode = 0x12

        self.hardware = Hardware(debug)
    def run(self):
        try:
            while self.pc < self.code_len:
                address = self.code_addresses[self.pc]
                op = self.memory[address]
                if self.debug:
                    print(f"[Execute] [Address:{hex(address)}] {op}")
                self.execute(op)
                self.pc += 1
                if self.pc >= self.code_len:
                    break
        except KeyError as e:
            print(f"[ERROR] Key Error: {e}")
            print(f"Memory: {self.memory}")
            print(f"Code addresses: {self.code_addresses}")
            print(f"Code Sector: {self._code_sector}")
            print(f"Data Sector: {self._data_sector}")
            print(f"Program Counter: {self.pc}")
            raise e
    def execute(self, op: tuple):
        
        opcode: str = op[0]
        if opcode == '1b':
            r1 = op[1]
            r2 = op[2]
            result = self.register[r1] + self.register[r2]
            self.register[r1] = result
        elif opcode == '1c':
            r1 = op[1]
            r2 = op[2]
            result = self.register[r1] - self.register[r2]
            self.register[r1] = result
        elif opcode == '1d':
            r1 = op[1]
            r2 = op[2]
            result = self.register[r1] * self.register[r2]
            self.register[r1] = result
        elif opcode == '1e':
            r1 = op[1]
            r2 = op[2]
            result = self.register[r1] / self.register[r2]
            self.register[r1] = result
        elif opcode == '1f':
            r1 = op[1]
            r2 = op[2]
            result = self.register[r1] % self.register[r2]
            self.register[r1] = result
        elif opcode == '20':
            r1 = op[1]
            r2 = op[2]
            result = self.register[r1] ** self.register[r2]
            self.register[r1] = result


        elif opcode == '2a':
            r1 = op[1]
            r2 = op[2]
            result = self.register[r1] & self.register[r2]
            self.register[r1] = result
        elif opcode == '2b':
            r1 = op[1]
            r2 = op[2]
            result = self.register[r1] | self.register[r2]
            self.register[r1] = result
        elif opcode == '2c':
            r1 = op[1]
            r2 = op[2]
            result = self.register[r1] ^ self.register[r2]
            self.register[r1] = result
        elif opcode == '2d':
            r1 = op[1]
            result = ~self.register[r1]
            self.register[r1] = result
        
        elif opcode == '2e':
            r1 = op[1]
            imm = op[2]
            result = self.register[r1] << imm
            self.register[r1] = result

        elif opcode == '2f':
            r1 = op[1]
            imm = op[2]
            result = self.register[r1] >> imm
            self.register[r1] = result
        
        
        elif opcode == '40':
            r1 = op[1]
            mem_addr = op[2]
            self.register[r1] = self.memory[mem_addr]
        elif opcode == '41':
            r1 = op[1]
            mem_addr = op[2]
            self.memory[mem_addr] = self.register[r1]
        elif opcode == '42':
            r1 = op[1]
            r2 = op[2]
            self.cmp(r1, r2)

        elif opcode == '43':
            addr = op[1]
            self.jump(addr)
        elif opcode == '44':
            if self.flags['ZF'] == 1:
                addr = op[1]
                self.jump(addr)
        elif opcode == '45':
            if self.flags['ZF'] == 0:
                addr = op[1]
                self.jump(addr)
        elif opcode == '46':
            if self.flags['ZF'] == 0 and self.flags['SF'] == self.flags['OF']:
                addr = op[1]
                self.jump(addr)
        elif opcode == '47':
            if self.flags['SF'] != self.flags['OF']:
                addr = op[1]
                self.jump(addr)
        elif opcode == '48':
            r1 = op[1]
            r2 = op[2]
            self.register[r1] = self.register[r2]
        elif opcode == '49':
            interrupt = op[1]
            self.interrupt(interrupt)
        elif opcode == '4a':
            mode = op[1]
            self.change_mode(mode)
        elif opcode == '4b':
            addr = op[1]
            self.call(addr)
        elif opcode == '4c':
            self.ret()

    
    def change_mode(self, mode: int):
        print("[INFO] mode changing is in developing")
        self.mode = mode



    def interrupt(self, interrupt):
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










































































































    def call(self, address):
        self.ret_pcs.append(self.pc)
        self.jump(address)
    def ret(self):
        pc = self.ret_pcs.pop()
        self.pc = pc





    def cmp(self, r1, r2):
        val1 = self.register[r1]
        val2 = self.register[r2]
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
        self.inet_connection = None
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
        print(color, end="")
    def internet(self):
        action = self.hardware_memory[0xFFFF_0100]
        if action == None:
            return
        else:
            if action == 0x00: # Listen
                fam  = self.hardware_memory[0xFFFF_0101]
                kind = self.hardware_memory[0xFFFF_0102]
                host = self.hardware_memory[0xFFFF_0103]
                port = self.hardware_memory[0xFFFF_0104]
                if host == None:return
                if fam == 0x00: # Inet:
                    fam = socket.AF_INET
                else:return
                if kind == 0x00: # UPD
                    kind = socket.SOCK_DGRAM
                elif kind == 0x01: # TCP
                    kind = socket.SOCK_STREAM
                else:return
                sock = socket.socket(fam, kind)
                sock.bind((socket.gethostbyname(host), port))
                self.inet_connection[port] = sock
            elif action == 0x01: # Connect
                fam  = self.hardware_memory[0xFFFF_0101]
                kind = self.hardware_memory[0xFFFF_0102]
                host = self.hardware_memory[0xFFFF_0103]
                port = self.hardware_memory[0xFFFF_0104]
                if host == None:return
                if fam == 0x00: # Inet:
                    fam = socket.AF_INET
                else:return
                if kind == 0x00: # UPD
                    kind = socket.SOCK_DGRAM
                elif kind == 0x01: # TCP
                    kind = socket.SOCK_STREAM
                else:return
                sock = socket.socket(fam, kind)
                sock.connect((socket.gethostbyname(host), port))
                self.inet_connection[port] = sock
            elif action == 0x02: #send
                port = self.hardware_memory[0xFFFF_0104]
                message = self.hardware_memory[0xFFFF_0105]
                sock: socket.socket = self.inet_connection[port]
                
                sock.send(bytes(message))
            elif action == 0x03: # recv
                port = self.hardware_memory[0xFFFF_0104]
                bufsize: int = self.hardware_memory[0xFFFF_0106]
                sock = self.inet_connection[port]
                msg = sock.recv(bufsize)
                self.hardware_memory[0xFFFF_0107] = msg
            elif action == 0x04: # exit
                port = self.hardware_memory[0xFFFF_0104]
                self.inet_connection[port].close()
        self.hardware_memory[0xFFFF_0100] = None
                
        
        
