[Back to Readme](./README.md)

# Biscuit Calls
Biscuit calls are interrupts to the biscuit engine.
You can make a Biscuit Call with `int 0x45`



|Call ID|Name|Description|
|---|------------|------------------------|
|0x00|BISC_EXIT|Stop the biscuit|
|0x01|BISC_HARDWARE|This will update the hardware, e. g. you write something into a hardware address (`0xFFFF####`) and this will update it|
|0x02|BISC_SLEEP|Wait the time `ebx` in miliseconds|
|0x03|BISC_INPUT|Input from the console, wait for input. The result will be in `eax`. ebx is the memory address for the string|
|0x04|BISC_WRITE|Write something|
|0x05|BISC_DEBUG|Print all information for debugging|
|0x06|BISC_WRITE_FILE|Write in a file (ebx), the text is (ecx)|
|0x07|BISC_READ_FILE|Read a file (ebx)|
|0x08|BISC_SPLIT|Split the engine in two threads, the new thread has the flag ZF=1, so you can use ´je´ to jump to an address that is only for the new thread| 
|0x09|BISC_STR_CHAR_BY_INDEX|Get an character from a string (eax) at index (ebx) and put result to eax 
## Hardware Addresses
|Hardware Address|Name|Description|
|--------|-------------|-----------------------------------------------|
0xFFFF0000|Terminal Color|Change the terminal color|
0xFFFF0100|Socket Action|Choice action of socket[port]|
0xFFFF0101|Address Family|The address family of the socket|
0xFFFF0102|Socket kind|The connection way of socket|
0xFFFF0103|host|the host as string|
0xFFFF0104|Port|the port as int|
0xFFFF0105|Message|the message as string|
0xFFFF0106|Bufsize|the bufsize for receiving messages|
0xFFFF0107|Socket output|The recived message from socket|


## Colors

|Color Hex|Color Name|
|----|---------------|
|0x00|RESET
|0x01|WHITE
|0x02|BLACK
|0x03|YELLOW
|0x04|RED
|0x05|BLUE
|0x06|GREEN
|0x07|MAGENTA
|0x08|CYAN
|0x09|LIGHTYELLOW
|0x0a|LIGHTBLACK
|0x0b|LIGHTCYAN
|0x0c|LIGHTMAGENTA
|0x0d|LIGHTGREEN
|0x0e|LIGHTWHITE
|0x0f|LIGHTRED

## Socket Actions
|Action Hex|Action Name|
|-|-|
|0x00|Listen and bind|
|0x01|Connect|
|0x02|send|
|0x03|recv|
|0x04|exit|

## Socket Address Families
|Familiy hex|Family Name|
|-|-|
|0x00|Inet|

## Socket Kinds
|Kind Hex|Kind Name|
|-|-|
|0x00|UDP|
|0x01|TCP|


