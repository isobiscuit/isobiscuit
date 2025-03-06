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

## Hardware Addresses
|Hardware Address|Name|Description|
|--------|-------------|-----------------------------------------------|
0xFFFF0000|Terminal Color|Change the terminal color|










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
