import os
import yaml
from .compiler import writeBiscuit





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
def build_biscuit(project_name, path="."):
    data_sector = ""
    code_sector = ""
    memory_sector = ""
    other_sector = ""
    files: list[str] = [
        f"{path}/{project_name}/biscuit.yaml"
        
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
    


    writeBiscuit(
        f"{path}/{project_name}",
        data_sector,
        code_sector,
        memory_sector,
        other_sector,
        files,
    )


    pass


