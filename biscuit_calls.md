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
