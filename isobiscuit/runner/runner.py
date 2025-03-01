from . import reader
from . import runtime



def run(file: str, debug=False):
    biscuit         = reader.read(file)
    _runtime        = runtime.start_biscuit(*biscuit, debug=debug)