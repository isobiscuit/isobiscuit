

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
            "build", 
            "build/debug",
            #"tests", 
            "docs", 
            "scripts", 
            "config",
            "bin",
            "fs",
        ],
        "files": {
            "biscuit.yaml": {
                "name": name,
                "version": "0.1.0",
                "entrypoint": "code/main.basm"
            },
            "code/main.biasm": "; Main.biasm",
            #"tests/test1.btest": "",
            "docs/README.md": f"# {name}",
            "scripts/build.sh": "#!/bin/bash\necho 'Building Biscuit...'\n",
            "scripts/run.sh": "#!/bin/bash\necho 'Running Biscuit...'\n",
            "scripts/clean.sh": "#!/bin/bash\necho 'Cleaning build...'\n",
            "config/env.json": "{}",
            "config/settings.yaml": {
                "memory_size": "16MB"
            }
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


def run_biscuit(biscuit: str, path=".", debug=False):
    if biscuit.endswith(".biscuit"):
        biscuit = biscuit
    else:
        biscuit = biscuit+".biscuit"
    run(biscuit, debug=debug)


def install_lib(biscuit, url, path="."):
    installFunc(url, biscuit, path)

def main():
    debug = sys.argv[-1] == "-d"
    action = sys.argv[1]
    if action == "init":
        init_biscuit(sys.argv[2])
    if action == "build":
        build_biscuit(sys.argv[2], debug=debug)
    if action == "run":
        run_biscuit(sys.argv[2], debug=debug)
    if action == "install":
        install_lib(sys.argv[2], sys.argv[3])
if __name__ == "__main__":
    main()