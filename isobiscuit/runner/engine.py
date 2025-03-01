
import time



class Engine:
    def __init__(self, data_sector: dict,
                  code_sector: dict[int, tuple[str|int]],
                  mem_sector: dict
                ):
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
        self.memory: dict = mem_sector
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
    def run(self):
        try:
            while self.pc < self.code_len:
                op = self.memory[self.code_addresses[self.pc]]
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
            r1 = op[2]
            mem_addr = op[1]
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
        elif opcode == '4A':
            mode = op[1]
            self.change_mode(mode)

    
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
            pass
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
            


    def syscall(self):
        #syscall = self.register[0x2f]
        print("[INFO] Syscalls are in developing")
















































































































    def cmp(self, r1, r2):
        result = self.register[r1] - self.register[r2]
        
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
        self.pc = self.code_addresses.index(address)


    def _update_1bit_register(self, register: int, value: bool):
        register[register] = value
    
    def _update_register(self, register: int, value):
        register[register] = value


    

