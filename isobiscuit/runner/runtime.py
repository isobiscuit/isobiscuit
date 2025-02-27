import binascii
import io
import zipfile


def hex_to_zipfile(zip):
    zip_bytes = binascii.unhexlify(zip)
    return io.BytesIO(zip_bytes)

def mount_zip_vfs(hex_string):
    zip_file = hex_to_zipfile(hex_string)  # Hex -> ZIP (In-Memory)
    
    return zipfile.ZipFile(zip_file, "r")
        


def start_biscuit(data_sector, code_sector, mem_sector, other_sector, zip):
    #zip = mount_zip_vfs(zip)
    print("RUNTIME IS IN DEVELOPING, here are the biscuit informations")
    print("DATA_SECTOR")
    print(data_sector)
    print("CODE_SECTOR")
    print(code_sector)
    print("MEM_SECTOR")
    print(mem_sector)
    print("OTHER_SECTOR")
    print(other_sector)
    print("VFS")
    print(str(str(binascii.unhexlify(zip))[2:][:-1]).replace("\\x", ""))