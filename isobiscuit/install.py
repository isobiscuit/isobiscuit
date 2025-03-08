





def main():
    from .installer import installFunc, remove, update
    import sys
    import os
    biscuit = sys.argv[1]
    biscuit_with_params = sys.argv[2]
    args_with_params = sys.argv[2:]
    args = sys.argv[1:]
    in_biscuit_folder = False
    if os.path.exists("biscuit.yml"):
        biscuit = "."
        biscuit_with_params = "."
        args = sys.argv[0:]
        args_with_params = sys.argv[1:]
        in_biscuit_folder = True
        
    if sys.argv[1] == "-u":
        update(biscuit_with_params, args_with_params[0])
    elif sys.argv[1] == "-R":
        remove(biscuit_with_params, args_with_params[0])
    else:
        installFunc(biscuit, args[0])



if __name__ == "__main__":
    main()