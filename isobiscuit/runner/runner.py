from . import reader
from . import runtime



def run(file: str):
    biscuit         = reader.read(file)
    _runtime        = runtime.start_biscuit(*biscuit)