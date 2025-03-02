import requests







def install(url: str, biscuit_name, path="."): # mylib#github:user/repo
    print(f"Install {url}...")
    _ = url.split("#")
    lib = _[0]
    source = _[1]
    _install(source, lib, biscuit_name, path)



def _install(source: str, lib: str, biscuit_name, path="."): # example {source: 'github:user/repo', lib: 'coolnicelib'}
    _ = source.split(":")
    host = _[0]
    url_lib = ""
    url_require = ""
    if host == "github":
        _ = _[1].split("/")
        user = _[0]
        repo = _[1]
        (url_lib, url_require, lib) = from_github(user, repo, lib)
    else:
        return
    
    download_biasm(url_lib, lib, biscuit_name, path)
    

def download_biasm(url, lib_name,biscuit_name: str, path="."):
    res = requests.get(url)
    if res.status_code == 200:
        with open(f"{path}/{biscuit_name}/code/lib/{lib_name}.biasm", "wb") as f:
            f.write(res.content)
            f.close()

def install_requirements(url, biscuit_name, path):
    res = requests.get(url)

    if res.status_code == 200:
        try: 
            data = res.json()
        except ValueError:
            print(f"Can not install requirements {url}. You have to install it manuelly")
            return
    for i in data["require"]:
        install(i, biscuit_name, path)

def from_github(user, repo, lib):
    url_lib = f"https://raw.githubusercontent.com/{user}/{repo}/master/lib_{lib}.biasm"
    url_require = f"https://raw.githubusercontent.com/user/repository/branch/require_{lib}.json"
    return (url_lib, url_require, lib)