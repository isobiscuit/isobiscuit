import binascii
import zipfile
import os
import io


def createBiscuitFile(biscuit_file):
    with open(f'{biscuit_file}.biscuit', 'a') as f:
        f.write("bisc") #Magic Bytes
        f.write(binascii.unhexlify(bytes(0x0001))) # Version
        f.write(binascii.unhexlify(0x00000000000000000000)) # Zero Bytes

def writeHex(biscuit_file, hex_string: str):
    with open(f'{biscuit_file}.biscuit', 'a') as f:
        f.write(binascii.unhexlify(hex_string))



def writeSizeInformation(biscuit_file, data_in_hex: str):
    l = len(data_in_hex) * 4
    l = str(hex(l)[2:])
    txt = ""
    for i in range(32 - len(l)):
        txt+="0"
    txt += l
    writeHex(biscuit_file, txt)


def writeSectors(biscuit_file, data_sector, code_sector, memory_sector, other_sector):
    writeSizeInformation(biscuit_file, data_sector)
    writeSizeInformation(biscuit_file, code_sector)
    writeSizeInformation(biscuit_file, memory_sector)
    writeSizeInformation(biscuit_file, other_sector)
    writeHex(biscuit_file, data_sector)
    writeHex(biscuit_file, code_sector)
    writeHex(biscuit_file, memory_sector)
    writeHex(biscuit_file, other_sector)





def addFilesToBiscuit(biscuit_file, files: list[str]):
    zip_buf = io.BytesIO()
    with zipfile.ZipFile(zip_buf, "w", zipfile.ZIP_DEFLATED) as zipf:
        for file in files:
            zipf.write(os.path.abspath(file))
    zip_data = zip_buf.getvalue()
    with open(f"{biscuit_file}.biscuit", "a") as f:
        f.write(zip_data)

    





def writeBiscuit(biscuit_file, data_sector, code_sector, memory_sector, other_sector, files: list[str]):
    createBiscuitFile(biscuit_file)
    writeSectors(biscuit_file, data_sector, code_sector, memory_sector, other_sector)
    addFilesToBiscuit(biscuit_file, files)
