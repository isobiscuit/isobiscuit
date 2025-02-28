import binascii
import io
import zipfile
from .parser import parse_data_sector

def hex_to_zipfile(zip):
    zip_bytes = binascii.unhexlify(zip)
    return io.BytesIO(zip_bytes)

def mount_zip_vfs(hex_string):
    zip_file = hex_to_zipfile(hex_string)  # Hex -> ZIP (In-Memory)
    
    return zipfile.ZipFile(zip_file, "r")
        
def parse_biscuit(data_sector, code_sector, mem_sector, other_sector):
    data_sector = parse_data_sector(data_sector)

    return (data_sector, code_sector, mem_sector, other_sector)

def start_biscuit(data_sector, code_sector, mem_sector, other_sector, zip):
    #zip = mount_zip_vfs(zip)
    (data_sector, code_sector, mem_sector, other_sector) = parse_biscuit(data_sector, code_sector, mem_sector, other_sector)
    print("RUNTIME IS IN DEVELOPING, HERE ARE THE BISCUIT INFORMATIONS")
    print("DATA_SECTOR")
    print(data_sector)
    print("CODE_SECTOR")
    print(code_sector)
    print("VIRTUAL FILE SYSTEM")
    print(zip)