[Back to README](./README.md)
# Biscuit Assembly (BiASM)
BiASM is compiled with a compiler, and the compiled code (BBin) is stored in the code sector within the .biscuit file.\
BiASM is similar to normal assembly but has a few differences:
 - You can't load a number directly into a register with `mov`, you have to use procedures for that, and then use the `load` command. \
 The `mov` command can only load from one register to another

 - if you enter a hexadecimal number `0x42` or a string `0x'41,73,63,69,69,20,48,65,78'`, then this will be loaded into the data sector. You don't need to use a `jmp` command
    - If you want a really byte string the use: `b0x'...'` this will not encode
 - With the `mode` command you can change the mode, e.g. from biscuit to linux (This feature is currently in development)

 - you don't need a separator with ',' in the command, the separator is the space


 
## Commands

|Command| Args | Description|
|-------|-------------------------|--------------------------------------------|
|add|Register 1, Register 2|register 1 + register 2 and store it in register 1|
|sub|Register 1, Register 2|register 1 - register 2 and store it in register 1|
|mul|Register 1, Register 2|register 1 * register 2 and store it in register 1|
|div|Register 1, Register 2|register 1 / register 2 and store it in register 1|
|mod|Register 1, Register 2|register 1 % register 2 and store it in register 1|
|exp|Register 1, Register 2|register 1<sup>register 2</sup> and store it in register 1|
|and|Register 1, Register 2|Insert description!|
|or|Register 1, Register 2|Insert description!|
|xor|Register 1, Register 2|Insert description!|
|not|Register 1|Insert description!|
|shl|Register 1, Imm|Insert description!|
|shr|Register 1, Imm|Insert description!|
|load|Register, MEM_ADDRESS|Load Memory address value into register, the mem_address can also be a procedur|
|store|Register, MEM_ADDRESS|Store register value into memory address, the mem_address can also be a procedur|
|cmp|Register 1, Register 2|Compare Register 1 and register 2 then you can use the jmp commands|
|jmp|ADDRESS|Jump to the address|
|je|ADDRESS|Jump if equals|
|jne|ADDRESS|Jump if not equals|
|jg|ADDRESS|Jump if greater|
|jl|ADDRESS|Jump if less|
|mov|Register 1, Register 2| Copy value of Register 2 in register 1|
|int|Interrupt|Interrupt something, for example: 0x45|
|mode|MODE|change mode of biscuit|
|call|Address|Call the address and jump back with ret|
|ret|Nothing|Return|
|push|Register|Push value from Register into the stack
|pop|Register|Pop value from stack into Register
|swap|Register1, Register2
|dup|Nothing
|halt|Nothing
|rand|Register, Int
|inc|Register
|dec|Register
|abs|Register
|neg|Register
## Registers


|Register Name|
|-|
|a|
|b|
|c|
|d|
|e|
|f|
|g|
|h|
|i|
|j|
|k|
|l|
|m|
|n|
|o|
|p|
|q|
|r|
|s|
|t|
|u|
|v|
|w|
|x|
|y|
|z|
|ax|
|bx|
|cx|
|dx|
|ix|
|eax|
|ebx|
|ecx|
|edx|
|eix|
|rax|
|rbx|
|rcx|
|rdx|
|rix|
|ip|
|sp|


## Modes ( In developing! This will not work yet)
|Mode Name|Description
|-|-|
|biscuit|This is the standard|
|linux|Load linux syscalls
