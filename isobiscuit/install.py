





def main():
    from .installer import installFunc, remove, update
    import sys
    if sys.argv[1] == "-u":
        update(sys.argv[3], sys.argv[2])
    elif sys.argv[1] == "-R":
        remove(sys.argv[3], sys.argv[2])
    else:
        installFunc(sys.argv[2], sys.argv[1])



if __name__ == "__main__":
    main()