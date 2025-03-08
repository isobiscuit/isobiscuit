





def main():
    from .installer import installFunc, remove, update
    import sys
    import os
    biscuit = sys.argv[1]
    args = sys.argv[1:]
    in_biscuit_folder = False
    if os.path.exists("biscuit.yml"):
        biscuit = "."
        args = sys.argv[0:]
        in_biscuit_folder = True
    if sys.argv[1] == "-u":
        update(biscuit, args[0])
    elif sys.argv[1] == "-R":
        remove(biscuit, args[0])
    else:
        installFunc(biscuit, args[0])



if __name__ == "__main__":
    main()