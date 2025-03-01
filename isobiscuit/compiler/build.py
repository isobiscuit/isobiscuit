import binascii
import zipfile
import os
import io
import glob
from ..biasm import compile as compileBiASM


def createBiscuitFile(biscuit_file):
    try:
        os.remove(f"{biscuit_file}.biscuit")
    except:
        pass
    with open(f'{biscuit_file}.biscuit', 'w+') as f:
        f.write("")
        f.write("bisc") #Magic Bytes
        f.write(str(binascii.unhexlify('0001').decode("utf-8"))) # Version
        f.write(str(binascii.unhexlify('00000000000000000000').decode("utf-8"))) # Zero Bytes

def writeHex(biscuit_file, hex_string: str):
    with open(f'{biscuit_file}.biscuit', 'ab') as f:
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
        for _ in files:
            for file in glob.glob(_):
                zipf.write(file)
    zip_data = zip_buf.getvalue()
    with open(f"{biscuit_file}.biscuit", "ab") as f:
        f.write(binascii.unhexlify(zip_data.hex()))

    





def writeBiscuit(biscuit_file, data_sector, code_sector, memory_sector, other_sector, files: list[str]):
    createBiscuitFile(biscuit_file)
    writeSectors(biscuit_file, data_sector, code_sector, memory_sector, other_sector)
    addFilesToBiscuit(biscuit_file, files)


def build(out_file, biasm_files: list[str], fs_files: list[str], debug=False):
    (code, data) = compileBiASM(biasm_files, debug)
    writeBiscuit(out_file, data, code, "", "", fs_files)