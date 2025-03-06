import requests
import os




def remove(lib: str, biscuit_name, path="."):
    os.remove(f"{path}/{biscuit_name}/code/lib/{lib}.biasm")

def update(url: str, biscuit_name, path="."):
    install(url, biscuit_name, path, force=True)




def install(url: str, biscuit_name, path=".", force=False): # mylib#github:user/repo
    
    _ = url.split("#")
    lib = _[0]
    try:
        source = _[1]
    except IndexError:
        (url_lib, url_require, lib) = from_biscuit_store(lib)
        download_biasm(url_lib, lib, biscuit_name, path)
        install_requirements(url_require, biscuit_name, path)
        return
    _install(source, lib, biscuit_name, path, force)




def _install(source: str, lib: str, biscuit_name, path=".", force=False): # example {source: 'github:user/repo', lib: 'coolnicelib'}
    if os.path.exists(f"{path}/{biscuit_name}/code/lib/{lib}.biasm"):
        if not force:
            print(f"[INFO] Package '{lib}' is already installed. Use 'bfetcher -u {biscuit_name} {lib}#{source}' to fetch the latest version.")
            return
    print(f"Install {lib}...")
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
    install_requirements(url_require, biscuit_name, path)

def download_biasm(url, lib_name,biscuit_name: str, path="."):
    res = requests.get(url)
    if res.status_code == 200:
        with open(f"{path}/{biscuit_name}/code/lib/{lib_name}.biasm", "wb") as f:
            f.write(res.content)
            f.close()

def install_requirements(url, biscuit_name, path):
    print(f"[INFO] Fetching requirements of `{url}`")
    res = requests.get(url)

    if res.status_code == 200:
        try: 
            data = res.json()
        except ValueError:
            print(f"Can not install requirements {url}. You have to install it manuelly")
            return
    if data["require"] != []:
        print(f"Requirements found: {", ".join(data["require"])}")
    else:
        print(f"No requirements found")
    for i in data["require"]:
        install(i, biscuit_name, path)



def from_biscuit_store(lib):
    url_lib =       f"https://raw.githubusercontent.com/isobiscuit/store/master/lib_{lib}.biasm"
    url_require =   f"https://raw.githubusercontent.com/isobiscuit/store/master/require_{lib}.json"
    return (url_lib, url_require, lib)


def from_github(user, repo, lib):
    url_lib =       f"https://raw.githubusercontent.com/{user}/{repo}/master/lib_{lib}.biasm"
    url_require =   f"https://raw.githubusercontent.com/{user}/{repo}/master/require_{lib}.json"
    return (url_lib, url_require, lib)