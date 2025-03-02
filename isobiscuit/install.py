





def main():
    from .installer import installFunc
    import sys
    installFunc(sys.argv[2], sys.argv[1])



if __name__ == "__main__":
    main()