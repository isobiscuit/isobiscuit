[Back to README](./README.md)
# Biscuit File Format
## Header
First line must be like this:\
62 69 73 63 00 01 00 00 00 00 00 00 00 00 00 00\
Let me explain:
 - the first 4 bytes are the magic bytes: "bisc"
 - then in the next 2 bytes comes the version: 0x0001
 - and then only zeros come until we have the 16 bytes full

## size information
you have 16 bytes to specify in bytes how big a sector should be, in bits.
so 16*4 is 64, so 64 bytes are needed for the size information.
The 16-bit size information is given in this order:
Data, Code, Memory, Other Sectors

Example:\
00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00\
00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 20\
00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00\
00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00

## Sectors
There are 4 sectors: Data, Code, Memory and Other sectors.
The other sectors sector contains sectors that are not relevant to the code, e.g. debug.\
The sectors are valid up to their permitted size, if this value is exceeded, you end up in other sectors
the order of the sectors is:
 - Data
 - Code
 - Memory
 - Other sectors

## FS
you just have to place the contents of the .zip file of the fs at the end of the file