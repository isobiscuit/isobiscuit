

from pathlib import Path
import os
import yaml
from .compiler import build
from .runner import run
from .installer import installFunc
import sys
import glob



"""Initialize Biscuit Project"""
def init_biscuit(name, path="."):
    BISCUIT_STRUCTURE = {
        "dirs": [
            "code",
            "code/lib",
            #"tests", 
            "docs", 
            "config",
            "bin",
            "fs",
        ],
        "files": {
            "biscuit.yaml": {
                "name": name,
            },
            "code/main.biasm": "; Main.biasm",
            #"tests/test1.btest": "",
            "docs/README.md": f"# {name}",
            
        }
    }


    if os.path.exists(name):
        return
    
    
    os.makedirs(name)
    
    for dir_name in BISCUIT_STRUCTURE["dirs"]:
        os.makedirs(os.path.join(name, dir_name))

    for file_name, content in BISCUIT_STRUCTURE["files"].items():
        file_path = os.path.join(name, file_name)
        with open(file_path, "w") as file:
            if isinstance(content, dict):
                yaml.dump(content, file)
            else:
                file.write(content)

"""Build Biscuit"""
def build_biscuit(project_name: str, path=".", debug=False):
    project_name = Path(project_name).resolve().name
    data_sector = ""
    code_sector = ""
    memory_sector = ""
    other_sector = ""
    files: list[str] = [
        f"{path}/{project_name}/biscuit.yaml"
        
    ]
    biasm_files: list[str] = [
        f"{path}/{project_name}/code/**/*.biasm",
        
    ]


    files_fs = os.listdir(f"{path}/{project_name}/fs")
    for file in files_fs:
        files.append(f"{path}/{project_name}/fs/{file}")

    files_docs = os.listdir(f"{path}/{project_name}/docs")
    for file in files_docs:
        files.append(f"{path}/{project_name}/docs/{file}")

    files_scripts = os.listdir(f"{path}/{project_name}/scripts")
    for file in files_scripts:
        files.append(f"{path}/{project_name}/scripts/{file}")

    files_config = os.listdir(f"{path}/{project_name}/config")
    for file in files_config:
        files.append(f"{path}/{project_name}/config/{file}")
    


    build.build(
        f"{path}/{project_name}",
        biasm_files,
        files,
        debug
    )


    pass

from .runner.reader import read
import binascii
import io
def extract_zip(biscuit: str, path="."):
    if biscuit.endswith(".biscuit"):
        biscuit = biscuit
    else:
        biscuit = biscuit+".biscuit"
    (data_sector, code_sector, mem_sector, other_sector, zip) = read(f"{path}/{biscuit}")
    zip = binascii.unhexlify(zip)
    chunk_size = 1024
    stream = io.BytesIO(zip)

    with open(f'{biscuit[:-8]}.zip', 'wb') as f:
        while (chunk := stream.read(chunk_size)):
            f.write(chunk)


def run_biscuit(biscuit: str, path=".", debug=False):
    if biscuit.endswith(".biscuit"):
        biscuit = biscuit
    else:
        biscuit = biscuit+".biscuit"
    run(biscuit, debug=debug)


def install_lib(biscuit, url, path="."):
    installFunc(url, biscuit, path)

def main():
    biscuit = sys.argv[2]
    args = sys.argv[2:]
    debug = sys.argv[-1] == "-d"
    action = sys.argv[1]
    if action == "init":
        init_biscuit(biscuit)
    if action == "build":
        build_biscuit(biscuit, debug=debug)
    if action == "run":
        run_biscuit(biscuit, debug=debug)
    if action == "install":
        install_lib(biscuit, args[0])
    if action == "extract":
        extract_zip(biscuit)
if __name__ == "__main__":
    main()