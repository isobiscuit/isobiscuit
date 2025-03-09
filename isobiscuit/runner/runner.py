from . import reader
from . import runtime



def run(file: str, debug=False):
    if file.endswith(".biscuit.biscuit"):
        file = file[:-8]
    if not file.endswith(".biscuit"):
        file = file+".biscuit"
    biscuit         = reader.read(file)
    _runtime        = runtime.start_biscuit(file, *biscuit, debug=debug)